# A Crusader's Christmas (UCP3 plugin)

The Christmas calendar by Krarilotus as a plugin for the Unofficial Crusader Patch 3: 21 single-player scenario maps for Stronghold Crusader 1.41 (not Extreme). One door opens per day from 1 December. The player text is in `locale/description-en.md`.

## Contents
| Path | What |
|---|---|
| `definition.yml` | Plugin definition and dependencies |
| `init.lua` | Registers `maps/<language>` with the files module (`registerExtraMapDirectory`, Crusader only), and gives the trail the German maps when the map language is German |
| `options.yml` | Option **Map language** (`en`/`de`) and the **Door pages** (a launcher CustomMenu) |
| `config.yml` | Suggested settings converted from the UCP2 calendar: ucp2-legacy, startResources, aiSwapper |
| `maps/en`, `maps/de` | The maps (`Door01–21.map`, `Türchen01–21.map`) and `availability.json` with the day each map is listed from |
| `doors/DoorNN/` | Door intro per language (`DoorNN_<lang>.html`) and the overview picture (`DoorNN_preview.jpg`) |
| `menu/` | The door pages (HTML, CSS, JS) |
| `resources/ai/hard/<Lord>/` | The author's AI for each of the 16 lords (v1.2.1: AIC, lord strength, start troops), used through AI Swapper |
| `resources/ai/normal/`, `resources/ai/story/` | The same AI with smaller attack waves and raids, slower recruiting and weaker lords; made by `tools/build_ai_tiers.py` |
| `trail/` | The calendar as a trail of Custom Skirmish Trails (the Warchest trail): trail settings, one scenario mission per door, German texts; made by `tools/build_trail.py` |
| `locale/` | Option and page texts, and the description |

## Players coming from the UCP2 calendar
The UCP2 version of the calendar copied its maps into the game's maps folder. Remove the old Door01.map … Door21.map and Türchen01.map … Türchen21.map files from that folder. Otherwise the old copies are listed from the first day on, all at once, and may be played instead of the maps of this plugin.

## Notes for authors
- **Dates.** `maps/*/availability.json` lists each map with its first day (format of the files module 1.5.0). The door pages use the same days (door N on 2026-12-N). To change the year, change both.
- **Testing a date.** The files module's setting `map-availability-date: YYYY-MM-DD` makes that day count as today, both for the in-game map list and for the door pages. A small test plugin can suggest it:
  ```yaml
  config-sparse:
    modules:
      files:
        config:
          map-availability-date:
            contents:
              suggested-value: "2026-12-05"
  ```
- **Translations.** A door intro in another launcher language goes into `doors/DoorNN/DoorNN_<lang>.html` (language codes as in the launcher: de, en, fr, ru, hu, tr, ch, es, fa). Missing languages fall back to English. Persian (`fa`) is shown right to left.
- **Playing on a difficulty.** The preset plugins in `../presets/` (Story, Normal, Hard) form the launcher family "A Crusader's Christmas: difficulty" (launcher 1.0.17). Among the available extensions the family is one entry; activating it activates Hard unless another member is chosen. An active preset is an ordinary plugin in the active list and must stay above the calendar there, so that its suggestions win over the calendar's own (Hard). Without a preset the calendar uses Hard. For an older launcher, revert the commit that adds the family and activate one preset by hand. A preset chooses the AI and suggests the Custom Skirmish Trails difficulty (`custom-skirmish-trails.difficulty`, for missions with a `unit_limit`; no door has one yet). Saved games load with any of them; the game doesn't save AI values, so a loaded game plays with the preset that is active then.
- **AI and difficulty.** `config.yml` selects `resources/ai/hard/<Lord>` in AI Swapper for the AIC, the lord and the start troops. Normal and Story are made from Hard by `tools/build_ai_tiers.py` with the factors at its top; running it again overwrites hand edits of `resources/ai/normal` and `resources/ai/story`, so tune the factors there, or stop using the script once you edit the files by hand. In the Hard AI (and so in the other two), three recruitment groups don't add up to 100 as AIC Loader documents: Frederick's RecruitProb*Strong (110), Nizar's RecruitProb*Default (110) and Wazir's RecruitProb*Weak (90).
- **Trail.** The doors are also the Warchest trail of Custom Skirmish Trails (Skirmish, then the Warchest trail). `tools/build_trail.py` writes `trail/` from `maps/*/availability.json` and the start gold in each map; run it after changing doors or dates, and `--check` tells whether the files are up to date. It requires door N to open N-th and `init.lua`'s DOORS to be the number of doors. The trail starts a door only from its date (files 1.5.0) and moves on when the door is won. Its briefing points to the door pages; after loading, the game shows the map's own briefing.
- The UCP2 files of the calendar (`maps_en`, `maps_de`, `scenarios`, `UCP`) stay in the repository root unchanged.
