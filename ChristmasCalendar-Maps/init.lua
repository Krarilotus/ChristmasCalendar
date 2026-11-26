-- Lists the calendar maps of one difficulty (Custom Scenarios -> Load a Map): maps-story/ for
-- Story, maps-hard/ for Hard, maps/ otherwise. The files module shows each map from the date in
-- the folder's availability.json on.
-- With the calendar active, the difficulty's trail plays the same maps and starts a door only from
-- that date.
local FOLDERS = { story = "maps-story", hard = "maps-hard" }

return {
  enable = function(self, config)
    local difficulty = type(config) == "table" and config.difficulty or nil
    local folder = FOLDERS[difficulty] or "maps"
    modules.files:registerExtraMapDirectory("ucp/plugins/ChristmasCalendar-Maps/" .. folder, "extreme")
  end,
  disable = function(self, config) end,
}
