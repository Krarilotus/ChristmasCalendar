"""Builds the calendar's trail files for Custom Skirmish Trails from the plugin's own data.

usage: python tools/build_trail.py [--check]

Reads, from plugin/:
  maps/en/availability.json, maps/de/availability.json   the doors and their dates
  maps/en/DoorNN.map             each door's starting gold for the player (section 1058)
  init.lua, menu/doors.js        their door counts (DOORS, DOOR_COUNT), which must match
Writes, into plugin/trail/:
  calendar-trail.json            trail settings: Warchest trail, title, door positions
  calendar-trail.csv             one scenario mission per door (English texts)
  texts/german.json              the German texts
The trail's briefing names the door and points to its door page in the launcher; the map's own
text shows in the game's briefing after loading. With --check it only compares (line endings
aside) and exits 1 when a file would change or the data doesn't fit together.
"""
import csv
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
        "briefing": ["Door {n} of A Crusader's Christmas.", "",
                     "The story, an overview of the map and hints",
                     "are on this door's page in the launcher:",
                     "the plugin's options, Door pages."],
    },
    "de": {
        "trail_title": "Weihnachtskreuzzug",
        "trail_summary": "Jeden Tag ein Türchen, ab dem 1. Dezember",
        "trail_locked_text": "Dieses Türchen öffnet sich am {date}.",
        "mission": "Türchen {n}",
        "briefing": ["Türchen {n} des Weihnachtskreuzzugs.", "",
                     "Die Geschichte, eine Übersicht der Karte und",
                     "Hinweise stehen auf der Seite dieses Türchens",
                     "im Launcher: Optionen des Plugins, Türchen."],
    },
}
LINES = 8
GOLD = 15  # section 1058 holds the starting goods as ints; index 15 is gold


def map_section(path, wanted):
    """The data of section `wanted` of a .map file (layout as in sourcehold-maps). Only
    uncompressed sections are read; compressed ones would need the game's DCL decoder."""
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
            if compressed[i] == 1:
                raise SystemExit("%s: section %d is compressed; this tool reads only uncompressed ones" % (path, wanted))
            return buf[pos:pos + lengths[i]]
        pos += lengths[i]
    raise SystemExit("%s: no section %d" % (path, wanted))


def start_gold(path):
    return struct.unpack_from("<I", map_section(path, 1058), GOLD * 4)[0]


def schedule(language):
    with open(os.path.join(ROOT, "maps", language, "availability.json"), encoding="utf-8") as handle:
        return json.load(handle)["maps"]


def doors():
    """The doors in date order; door N must be the N-th, with its map in both languages."""
    english, german = schedule("en"), schedule("de")
    result = []
    for name, date in sorted(english.items(), key=lambda item: item[1]):
        number = int(re.search(r"(\d+)$", name).group(1))
        result.append({"name": name, "number": number, "date": date})
    for index, door in enumerate(result, start=1):
        german_name = "Türchen%02d" % door["number"]
        if door["number"] != index:
            raise SystemExit("door %s is mission %d of the trail; init.lua gives German maps by door number"
                             % (door["name"], index))
        if german.get(german_name) != door["date"]:
            raise SystemExit("%s: no German map with the same date in maps/de/availability.json" % german_name)
        for language, map_name in (("en", door["name"]), ("de", german_name)):
            if not os.path.exists(os.path.join(ROOT, "maps", language, map_name + ".map")):
                raise SystemExit("missing map maps/%s/%s.map" % (language, map_name))
    for path, pattern, what in ((os.path.join(ROOT, "init.lua"), r"local DOORS = (\d+)", "init.lua's DOORS"),
                                (os.path.join(ROOT, "menu", "doors.js"), r"const DOOR_COUNT = (\d+);", "doors.js's DOOR_COUNT")):
        with open(path, encoding="utf-8") as handle:
            declared = re.search(pattern, handle.read())
        if declared is None or int(declared.group(1)) != len(result):
            raise SystemExit("%s must be %d, the number of doors" % (what, len(result)))
    return result


def briefing(language, number):
    lines = [line.format(n=number) for line in TEXTS[language]["briefing"]]
    return (lines + [""] * LINES)[:LINES]


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
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(header)
    german = {"trail_title": TEXTS["de"]["trail_title"], "trail_summary": TEXTS["de"]["trail_summary"],
              "trail_locked_text": TEXTS["de"]["trail_locked_text"], "missions": {}}
    for index, door in enumerate(entries, start=1):
        gold = start_gold(os.path.join(ROOT, "maps", "en", door["name"] + ".map"))
        writer.writerow([door["name"], TEXTS["en"]["mission"].format(n=door["number"]), "scenario", 1, 0, gold]
                        + briefing("en", door["number"]))
        mission = {"mission_name": TEXTS["de"]["mission"].format(n=door["number"])}
        for line, text in enumerate(briefing("de", door["number"]), start=1):
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
        if old is None or old.replace("\r\n", "\n") != text:
            changed.append(name)
            if not check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8", newline="") as handle:
                    handle.write(text)
    print(("would change: " if check else "written: ") + (", ".join(changed) or "nothing"))
    return 1 if check and changed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
