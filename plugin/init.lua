-- Lists the calendar maps in the chosen language (Custom Scenarios -> Play a Map).
-- The files module shows each map from the date in that folder's availability.json on.
local MAP_LANGUAGES = { en = true, de = true }

return {
  enable = function(self, config)
    local language = type(config) == "table" and config["map-language"] or nil
    if not MAP_LANGUAGES[language] then
      language = "en"
    end
    modules.files:registerExtraMapDirectory("ucp/plugins/ChristmasCalendar/maps/" .. language, "crusader")
  end,
  disable = function(self, config) end,
}
