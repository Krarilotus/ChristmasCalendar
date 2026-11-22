# A Crusader's Christmas (UCP3 plugin)

The Christmas calendar by Krarilotus as a plugin for the Unofficial Crusader Patch 3: 21 single-player scenario maps for Stronghold Crusader 1.41 (not Extreme). One door opens per day from 1 December. The player text is in `locale/description-en.md`.

## Contents
| Path | What |
|---|---|
| `definition.yml` | Plugin definition and dependencies |
| `init.lua` | Registers `maps/<language>` with the files module (`registerExtraMapDirectory`, Crusader only) |
| `options.yml` | Option **Map language** (`en`/`de`) and the **Door pages** (a launcher CustomMenu) |
| `config.yml` | Suggested settings converted from the UCP2 calendar: ucp2-legacy, startResources, aiSwapper |
| `maps/en`, `maps/de` | The maps (`Door01–21.map`, `Türchen01–21.map`) and `availability.json` with the day each map is listed from |
| `doors/DoorNN/` | Door intro per language (`DoorNN_<lang>.html`) and the overview picture (`DoorNN_preview.jpg`) |
| `menu/` | The door pages (HTML, CSS, JS) |
| `resources/ai/<Lord>/` | The calendar's AI personality (AIC) for each of the 16 lords, used through AI Swapper |
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
- **AI.** `config.yml` selects `resources/ai/<Lord>` in AI Swapper for the AIC, the lord and the start troops. The folders only contain an AIC, so the lord and start troops are reset to the game's own values, as they were in the UCP2 calendar.
- The UCP2 files of the calendar (`maps_en`, `maps_de`, `scenarios`, `UCP`) stay in the repository root unchanged.
