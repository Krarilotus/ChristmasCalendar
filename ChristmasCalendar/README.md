# A Crusader's Christmas (UCP3 plugin)

The Christmas calendar by Krarilotus as a plugin for the Unofficial Crusader Patch 3: 21 single-player scenario maps for Stronghold Crusader Extreme 1.41. One door opens per day from 1 December. The player text is in `locale/description-en.md`.

## Family
The calendar is the root of the difficulty family and has no settings of its own; it depends only on the maps. Each difficulty (`ChristmasCalendar-Story`, `-Normal`, `-Hard`) depends on the calendar and on the other plugins in the folders next to it, which are not family members, so that exactly one family plugin carries settings (launcher 1.0.17: a family member that applies settings, or depends directly on a plugin outside the family that does, counts as a choice, and two choices conflict). Maps, AI and Balance are each usable alone:

| Plugin | Owns |
|---|---|
| `ChristmasCalendar-Maps` | `maps/` (`Door01–21.map`, `availability.json` with the day each map is listed from), the maps of Normal and of the plugin alone; `maps-story/` and `maps-hard/`, the same for Story and Hard; `init.lua` registers the folder of the option `difficulty`, which each difficulty sets, with the files module (Extreme only) |
| `ChristmasCalendar-AI` | `resources/ai/hard/<Lord>/`, the author's AI for each of the 16 lords (v1.2.1: AIC, lord strength, start troops); `resources/ai/normal/`, `resources/ai/story/`, made by `tools/build_ai_tiers.py`; the AI Swapper choice (Hard), the AI options of ucp2-legacy and AIC Tactics |
| `ChristmasCalendar-Balance` | `resources/balance/calendar.json` for Rebalancer, spearmen running in Running Units, the bug fixes and troop options of ucp2-legacy |
| `ChristmasCalendar-Settings` | `config.yml`: startResources, the interface options of ucp2-legacy and the scenario modules |

## Contents
| Path | What |
|---|---|
| `definition.yml` | Plugin definition and dependencies |
| `doors/DoorNN/` | The overview picture of each released door (`DoorNN_preview.jpg`), shown on its door page; written by `tools/build_doors.py` |
| `locale/` | The description with the door grid, and the pages of the released doors (`<lang>.yml`, written by `tools/build_doors.py`) |

## Players coming from the UCP2 calendar
The UCP2 version of the calendar copied its maps into the game's maps folder. Remove the old Door01.map … Door21.map and Türchen01.map … Türchen21.map files from that folder. Otherwise the old copies are listed from the first day on, all at once, and may be played instead of the maps of this plugin.

## Notes for authors
- **Dates.** `ChristmasCalendar-Maps/maps/*/availability.json` lists each map with its first day (format of the files module 1.5.0).
- **Testing a date.** The files module's setting `map-availability-date: YYYY-MM-DD` makes that day count as today, for the in-game map list. A small test plugin can suggest it:
  ```yaml
  config-sparse:
    modules:
      files:
        config:
          map-availability-date:
            contents:
              suggested-value: "2026-12-05"
  ```
- **Door texts.** The launcher shows the door pages inside this plugin's description (a launcher with description pages): `locale/description-<lang>.md` links each door as `[N](#page:doorNN_story)`. The pages of all doors are kept in `tools/doors/ChristmasCalendar/`, which mirrors this plugin: each door's page is `doorNN_story` in `locale/<lang>.yml` (language codes as in the launcher: de, en, fr, ru, hu, tr, ch, es, fa), in markdown: the title, the picture `![…](doors/DoorNN/DoorNN_preview.jpg)`, the story, the links `[Hint K](#page:doorNN_hintK)` and the closing text. Each hint `doorNN_hintK` is its own page. Coloured names are links such as `[Emir](#color:#0000ff)`. The launcher removes every `&` from locale texts, so write characters such as ’ or … directly. A missing key falls back to English. A difficulty plugin can add a hint for a door: `tools/doors/ChristmasCalendar-<Difficulty>/locale/<lang>.yml` with `doorNN_hintK`; the hint shows where the calendar's `doorNN_story` links it. An optional `doorNN_video` block holds one markdown link, such as a let's play. It is added as the last line of the door's page, from English when a language has none, and an empty block shows nothing. The launcher opens it in the browser. Use a link without `&`, such as `https://youtu.be/<id>`. `tools/build_doors.py` copies the pages and files of doors 1 to `RELEASED_DOORS` (at its top) into the plugins and removes the others; the launcher hides a link to a page that doesn't exist, so each door appears with its update. `--check` tells whether the shipped files are up to date.
- **Releasing a door.** `tools/build_releases.py` builds one branch per door, `release/2.0.N`. The daily steps are under "Releasing doors" in the repository's `README.md`.
- **Playing on a difficulty.** The preset plugins `ChristmasCalendar-Story`, `-Normal` and `-Hard` form the launcher family "A Crusader's Christmas: difficulty" (launcher 1.0.17). The calendar is the family root. Choose Story, Normal, or Hard in Available. Normal is the family default. A preset brings in the calendar, `ChristmasCalendar-Settings`, `ChristmasCalendar-AI` and `ChristmasCalendar-Balance`, and stays above them in the active list, so that its suggestions win over the AI's own (Hard). Hard keeps the AI's choice. The calendar chosen without a preset brings no settings. Each preset sets its own trail, `trail/` in its folder, as the Extreme trail of Custom Skirmish Trails, and the maps of its difficulty (`ChristmasCalendar-Maps.difficulty`). The trail's `trail_id` keeps each difficulty's progress apart from the others and from the game's own. Saved games load with any of them; the game doesn't save AI values, so a loaded game plays with the preset that is active then.
- **AI and difficulty.** `ChristmasCalendar-AI/config.yml` selects `resources/ai/hard/<Lord>` in AI Swapper for the AIC, the lord and the start troops. In the launcher a lord is named "Rat (ez)" for Story, "Rat" for Normal and "Rat (hard)" for Hard; in game the lords keep their own names. Normal and Story are made from Hard by `tools/build_ai_tiers.py` with the factors at its top; running it again overwrites hand edits of `resources/ai/normal` and `resources/ai/story`, so tune the factors there, or stop using the script once you edit the files by hand. In the Hard AI (and so in the other two), three recruitment groups don't add up to 100 as AIC Loader documents: Frederick's RecruitProb*Strong (110), Nizar's RecruitProb*Default (110) and Wazir's RecruitProb*Weak (90).
- **Trail.** The doors are also the Extreme trail of Custom Skirmish Trails (Skirmish, then the Extreme trail). `tools/build_trail.py` writes the `trail/` of each difficulty from the Maps plugin's `availability.json`, the start gold in each map of that difficulty and the texts in `tools/trail/`, which every difficulty shares; `CHILDREN` at its top holds what differs: the maps folder, `trail_id`, `chickens` and `unit_limit`. It copies `availability.json` into `maps-story/` and `maps-hard/`; run it after changing doors or dates, and `--check` tells whether the files are up to date. It requires door N to open N-th. The trail starts a door only from its date (files 1.5.0) and moves on when the door is won. Its briefing shows a short brief cut from the door's story; after loading, the game shows the door's story, `scenario_briefing` of the mission file or of `texts/german.json`.
- **Editing a door.** Edit `tools/trail/missions/doorNN.json` (`mission_name`, `text_description`, `scenario_briefing`, or other keys of Trails' `mission.schema.json`), then run `tools/build_trail.py`; it keeps every value there and only adds missing ones. `unit_limit` and `players[0].gold` are set per difficulty. To give a difficulty its own map, replace its copy in `maps-story/`, `maps/` or `maps-hard/` and run the tool, which reads the start gold again.

### Troop limits

Each difficulty's `unit_limit` is in `CHILDREN` of `tools/build_trail.py`. Story has `formula 9900 40`, Extreme's skirmish limit: 9900 divided by the number of living lords, minus 40. Normal and Hard have `formula 2500 40`, near Crusader's limit. Scenario maps have no limit of their own, so `native` means no limit. `by_alive 8=400 4=800 1=3000` sets the limit at the listed numbers of living lords and interpolates between them.
