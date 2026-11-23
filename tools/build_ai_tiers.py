"""Builds the Normal and Story AI of the calendar from the Hard AI, and the difficulty presets.

usage: python tools/build_ai_tiers.py [--check]

plugin/resources/ai/hard/<Lord>/ is the author's AI (v1.2.1). Normal and Story are derived
from it by the factors below: only numbers change, never the units a lord uses, so every lord
keeps its character. They are starting points for the author to tune.

Writes:
  plugin/resources/ai/normal/<Lord>/, plugin/resources/ai/story/<Lord>/  character.json, meta.json
  presets/ChristmasCalendar-<Tier>/config.yml  the aiSwapper suggestions of each preset
With --check it only compares and exits 1 when a file would change.
"""
import json
import os
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
AI = os.path.join(REPO, "plugin", "resources", "ai")
PRESETS = os.path.join(REPO, "presets")
LORDS = ["Rat", "Snake", "Pig", "Wolf", "Saladin", "Caliph", "Sultan", "Richard", "Frederick",
         "Phillip", "Wazir", "Emir", "Nizar", "Sheriff", "Marshal", "Abbot"]
LABELS = {"story": "Story", "normal": "Normal", "hard": "Hard"}

# factor per tier; integer fields are rounded and never go below 0
SCALE = {
    "normal": {
        "AttForceBase": 0.8, "AttForceRandom": 0.8,      # size of the attack waves
        "RaidUnitsBase": 0.8, "RaidUnitsRandom": 0.8,    # size of raids
        "RecruitGoldThreshold": 1.25,                    # gold kept back before recruiting
    },
    "story": {
        "AttForceBase": 0.6, "AttForceRandom": 0.6,
        "RaidUnitsBase": 0.6, "RaidUnitsRandom": 0.6,
        "RecruitGoldThreshold": 1.5,
    },
}
# added to the waiting time between recruitments (higher is slower)
RECRUIT_INTERVAL_ADD = {"normal": 1, "story": 2}
RECRUIT_INTERVALS = ("RecruitInterval", "RecruitIntervalWeak", "RecruitIntervalStrong")
LORD_STRENGTH = {"normal": 0.85, "story": 0.7}
START_TROOPS = {"normal": 0.75, "story": 0.5}


def scaled(value, factor):
    return max(0, int(round(value * factor)))


def derive(character, tier):
    result = json.loads(json.dumps(character))
    aic = result["aic"]
    for field, factor in SCALE[tier].items():
        if isinstance(aic.get(field), int):
            aic[field] = scaled(aic[field], factor)
    for field in RECRUIT_INTERVALS:
        if isinstance(aic.get(field), int):
            aic[field] = aic[field] + RECRUIT_INTERVAL_ADD[tier]
    lord = result.get("lord")
    if isinstance(lord, dict) and isinstance(lord.get("StrengthMultiplier"), (int, float)):
        lord["StrengthMultiplier"] = round(lord["StrengthMultiplier"] * LORD_STRENGTH[tier], 2)
    troops = result.get("startTroops")
    if isinstance(troops, dict):
        for mode, units in troops.items():
            if isinstance(units, dict):
                for unit, count in units.items():
                    if isinstance(count, int):
                        units[unit] = scaled(count, START_TROOPS[tier])
    return result


def read_json(path):
    with open(path, encoding="utf-8-sig") as handle:
        return json.load(handle)


def tier_name(lord, tier):
    name = read_json(os.path.join(AI, "hard", lord, "meta.json"))["name"]
    return name if tier == "hard" else "%s (%s)" % (name, LABELS[tier])


def preset_config(tier):
    lines = ["meta:", "  version: 1.0.0", "config-sparse:", "  modules:", "    aiSwapper:", "      config:", "        ai:"]
    for lord in LORDS:
        lines.append("          %s:" % lord.lower())
        for part in ("aic", "lord", "startTroops"):
            lines += [
                "            %s:" % part,
                "              contents:",
                "                suggested-value:",
                "                  name: %s" % json.dumps(tier_name(lord, tier), ensure_ascii=False),
                "                  root: ucp/plugins/ChristmasCalendar/resources/ai/%s/%s/" % (tier, lord),
                "                  active: true",
            ]
    lines.append("  plugins: {}")
    return "\n".join(lines) + "\n"


def build():
    files = {}
    for lord in LORDS:
        character = read_json(os.path.join(AI, "hard", lord, "character.json"))
        meta = read_json(os.path.join(AI, "hard", lord, "meta.json"))
        for tier in ("normal", "story"):
            tier_meta = dict(meta)
            tier_meta["name"] = tier_name(lord, tier)
            tier_meta["description"] = ("%s difficulty of the Christmas Calendar for %s, derived from the hard AI"
                                        % (LABELS[tier], lord))
            base = os.path.join("plugin", "resources", "ai", tier, lord)
            files[os.path.join(base, "character.json")] = json.dumps(derive(character, tier), ensure_ascii=False, indent=2) + "\n"
            files[os.path.join(base, "meta.json")] = json.dumps(tier_meta, ensure_ascii=False, indent=2) + "\n"
    return files


def write(files, check):
    changed = []
    for name, text in files.items():
        path = os.path.join(REPO, name)
        old = open(path, encoding="utf-8", newline="").read() if os.path.exists(path) else None
        if old != text:
            changed.append(name)
            if not check:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8", newline="") as handle:
                    handle.write(text)
    return changed


def main(argv):
    check = "--check" in argv
    changed = write(build(), check)
    presets = {os.path.join("presets", "ChristmasCalendar-%s" % LABELS[tier], "config.yml"): preset_config(tier)
               for tier in ("story", "normal", "hard")}
    changed += write(presets, check)
    print(("would change: " if check else "written: ") + (", ".join(changed) if changed else "nothing"))
    return 1 if check and changed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
