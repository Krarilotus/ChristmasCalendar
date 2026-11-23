"""Builds the calendar's trail files for Custom Skirmish Trails from the plugin's own data.

usage: python tools/build_trail.py [--check]

Reads, from plugin/:
  maps/en/availability.json      the doors and their dates (the single schedule)
  maps/en/DoorNN.map             each door's starting gold for the player (section 1058)
  doors/DoorNN/DoorNN_{en,de}.html  the start of each door's intro for the trail briefing
Writes, into plugin/trail/:
  calendar-trail.json            trail settings: Warchest trail, title, door positions
  calendar-trail.csv             one scenario mission per door (English texts)
  texts/german.json              the German texts
With --check it only compares and exits 1 when a file would change.
"""
import binascii
import csv
import html
import io
import json
import os
import re
import struct
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plugin")
TRAIL = os.path.join(ROOT, "trail")

# the first door positions follow the path on the game's own Warchest trail screen
WARCHEST_POSITIONS = [
    (50, 166), (81, 170), (132, 149), (178, 142), (248, 126), (308, 117), (376, 108),
    (444, 110), (500, 88), (558, 102), (565, 126), (623, 143), (643, 180), (676, 230),
    (712, 311), (578, 308), (495, 251), (480, 181), (454, 138), (363, 135), (301, 174),
    (360, 215), (390, 272), (438, 342), (297, 412), (250, 376), (98, 379), (228, 292),
    (184, 245), (65, 219),
]

TEXTS = {
    "en": {
        "trail_title": "A Crusader's Christmas",
        "trail_summary": "One door a day, from 1 December",
        "trail_locked_text": "This door opens on {date}.",
        "mission": "Door {n}",
    },
    "de": {
        "trail_title": "Weihnachtskreuzzug",
        "trail_summary": "Jeden Tag ein Türchen, ab dem 1. Dezember",
        "trail_locked_text": "Dieses Türchen öffnet sich am {date}.",
        "mission": "Türchen {n}",
    },
}
LINE_WIDTH = 52
LINES = 8

# --- the start gold, from the door's map file ---------------------------------------------

LITLEN = bytes([11, 124, 8, 7, 28, 7, 188, 13, 76, 4, 10, 8, 12, 10, 12, 10, 8, 23, 8, 9, 7, 6, 7, 8, 7, 6,
                55, 8, 23, 24, 12, 11, 7, 9, 11, 12, 6, 7, 22, 5, 7, 24, 6, 11, 9, 6, 7, 22, 7, 11, 38, 7, 9,
                8, 25, 11, 8, 11, 9, 12, 8, 12, 5, 38, 5, 38, 5, 11, 7, 5, 6, 21, 6, 10, 53, 8, 7, 24, 10, 27,
                44, 253, 253, 253, 252, 252, 252, 13, 12, 45, 12, 45, 12, 61, 12, 45, 44, 173])
LENLEN = bytes([2, 35, 36, 53, 38, 23])
DISTLEN = bytes([2, 20, 53, 230, 247, 151, 248])
BASE = (3, 2, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 40, 72, 136, 264)
EXTRA = (0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8)


def huffman(rep):
    lengths = []
    for byte in rep:
        lengths.extend([byte & 15] * ((byte >> 4) + 1))
    counts = [0] * 14
    for length in lengths:
        counts[length] += 1
    offsets = [0] * 14
    for length in range(1, 13):
        offsets[length + 1] = offsets[length] + counts[length]
    symbols = [0] * len(lengths)
    for symbol, length in enumerate(lengths):
        if length:
            symbols[offsets[length]] = symbol
            offsets[length] += 1
    return counts, symbols


LIT, LEN, DIST = huffman(LITLEN), huffman(LENLEN), huffman(DISTLEN)


def explode(data):
    """PKWARE DCL decompression (the format of .map sections), after Mark Adler's blast.c."""
    state = {"pos": 0, "buf": 0, "cnt": 0}

    def bits(need):
        while state["cnt"] < need:
            state["buf"] |= data[state["pos"]] << state["cnt"]
            state["pos"] += 1
            state["cnt"] += 8
        value = state["buf"] & ((1 << need) - 1)
        state["buf"] >>= need
        state["cnt"] -= need
        return value

    def decode(table):
        counts, symbols = table
        code = first = index = 0
        for length in range(1, 14):
            code |= bits(1) ^ 1
            if code < first + counts[length]:
                return symbols[index + code - first]
            index += counts[length]
            first = (first + counts[length]) << 1
            code <<= 1
        raise ValueError("bad code")

    coded, dict_bits = bits(8), bits(8)
    out = bytearray()
    while True:
        if bits(1):
            symbol = decode(LEN)
            length = BASE[symbol] + bits(EXTRA[symbol])
            if length == 519:
                return bytes(out)
            shift = 2 if length == 2 else dict_bits
            dist = (decode(DIST) << shift) + bits(shift) + 1
            for _ in range(length):
                out.append(out[-dist])
        else:
            out.append(decode(LIT) if coded else bits(8))


def map_section(path, wanted):
    """The data of section `wanted` of a .map file (layout as in sourcehold-maps)."""
    with open(path, "rb") as handle:
        buf = handle.read()
    pos = 8 + struct.unpack_from("<I", buf, 4)[0]          # magic, preview
    pos += 4 + struct.unpack_from("<I", buf, pos)[0]        # description
    for _ in range(4):                                      # U1..U4
        pos += 4 + struct.unpack_from("<I", buf, pos)[0]
    pos += 4
    directory_size, _, count = struct.unpack_from("<III", buf, pos)
    slots = 150 if struct.unpack_from("<I", buf, pos + 12)[0] >= 161 else 100
    table = pos + 32
    lengths = struct.unpack_from("<%dI" % slots, buf, table + 4 * slots)
    indices = struct.unpack_from("<%dI" % slots, buf, table + 8 * slots)
    compressed = struct.unpack_from("<%dI" % slots, buf, table + 12 * slots)
    pos += directory_size
    for i in range(count):
        if indices[i] == wanted:
            raw = buf[pos:pos + lengths[i]]
            if compressed[i] != 1:
                return raw
            usize, csize, crc = struct.unpack_from("<III", raw, 0)
            data = explode(raw[12:12 + csize])
            if len(data) != usize or binascii.crc32(data) != crc:
                raise ValueError("%s: section %d checksum" % (path, wanted))
            return data
        pos += lengths[i]
    raise ValueError("%s: no section %d" % (path, wanted))


def start_gold(path):
    # section 1058 holds the starting goods as ints; index 15 is gold
    return struct.unpack_from("<I", map_section(path, 1058), 15 * 4)[0]

# --- intros ---------------------------------------------------------------------------------


def intro_lines(path):
    """The intro's first paragraph(s) without hints, wrapped into the briefing's 8 lines."""
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    text = re.sub(r"(?is)<details.*?</details>", " ", text)
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    words = text.split()
    lines, current = [], ""
    for word in words:
        if len(current) + 1 + len(word) > LINE_WIDTH:
            lines.append(current)
            current = word
            if len(lines) == LINES:
                break
        else:
            current = (current + " " + word).strip()
    else:
        if current:
            lines.append(current)
    if len(lines) == LINES and len(" ".join(lines)) < len(" ".join(words)):
        last = lines[-1]
        lines[-1] = (last[:LINE_WIDTH - 1].rsplit(" ", 1)[0] + " …") if len(last) >= LINE_WIDTH - 1 else last + " …"
    return (lines + [""] * LINES)[:LINES]

# --- build ----------------------------------------------------------------------------------


def doors():
    with open(os.path.join(ROOT, "maps", "en", "availability.json"), encoding="utf-8") as handle:
        schedule = json.load(handle)["maps"]
    result = []
    for name, date in sorted(schedule.items(), key=lambda item: item[1]):
        number = int(re.search(r"(\d+)$", name).group(1))
        result.append({"name": name, "number": number, "date": date})
    return result


def build():
    files = {}
    entries = doors()
    if len(entries) > len(WARCHEST_POSITIONS):
        raise SystemExit("more doors than trail positions")
    settings = {
        "$schema": "https://github.com/gynt/ucp-extension-custom-skirmish-trails/resources/trail-settings.schema.json",
        "trail_type": "Warchest",
        "trail_title": TEXTS["en"]["trail_title"],
        "trail_summary": TEXTS["en"]["trail_summary"],
        "trail_locked_text": TEXTS["en"]["trail_locked_text"],
        "trail_text_files": "texts/",
        "trail_mission_positions": [{"x": x, "y": y} for x, y in WARCHEST_POSITIONS[:len(entries)]],
    }
    files["calendar-trail.json"] = json.dumps(settings, ensure_ascii=False, indent=2) + "\n"

    header = ["map_name", "mission_name", "mission_kind", "num_players", "player1", "gold_player_1"] + [
        "text_description_line_%02d" % line for line in range(1, LINES + 1)]
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\r\n")
    writer.writerow(header)
    german = {"trail_title": TEXTS["de"]["trail_title"], "trail_summary": TEXTS["de"]["trail_summary"],
              "trail_locked_text": TEXTS["de"]["trail_locked_text"], "missions": {}}
    for index, door in enumerate(entries, start=1):
        folder = os.path.join(ROOT, "doors", "Door%02d" % door["number"])
        gold = start_gold(os.path.join(ROOT, "maps", "en", door["name"] + ".map"))
        lines_en = intro_lines(os.path.join(folder, "Door%02d_en.html" % door["number"]))
        lines_de = intro_lines(os.path.join(folder, "Door%02d_de.html" % door["number"]))
        writer.writerow([door["name"], TEXTS["en"]["mission"].format(n=door["number"]), "scenario", 1, 0, gold]
                        + lines_en)
        mission = {"mission_name": TEXTS["de"]["mission"].format(n=door["number"])}
        for line, text in enumerate(lines_de, start=1):
            mission["text_description_line_%02d" % line] = text
        german["missions"][str(index)] = mission
    files["calendar-trail.csv"] = out.getvalue()
    files[os.path.join("texts", "german.json")] = json.dumps(german, ensure_ascii=False, indent=2) + "\n"
    return files


def main(argv):
    check = "--check" in argv
    changed = []
    for name, text in build().items():
        path = os.path.join(TRAIL, name)
        old = open(path, encoding="utf-8", newline="").read() if os.path.exists(path) else None
        if old != text:
            changed.append(name)
            if not check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8", newline="") as handle:
                    handle.write(text)
    print(("would change: " if check else "written: ") + (", ".join(changed) or "nothing"))
    return 1 if check and changed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
