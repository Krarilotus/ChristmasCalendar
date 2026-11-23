-- Lists the calendar maps in the chosen language (Custom Scenarios -> Play a Map) and gives the
-- calendar trail the same maps. The files module shows each map from the date in that folder's
-- availability.json on, and the trail starts a door only from that date.
local MAP_LANGUAGES = { en = true, de = true }
local DOORS = 21

return {
  enable = function(self, config)
    local language = type(config) == "table" and config["map-language"] or nil
    if not MAP_LANGUAGES[language] then
      language = "en"
    end
    modules.files:registerExtraMapDirectory("ucp/plugins/ChristmasCalendar/maps/" .. language, "crusader")

    -- the trail's mission data names the English maps
    local trails = modules["custom-skirmish-trails"]
    if language == "de" and trails ~= nil and trails.setMissionMap ~= nil then
      for door = 1, DOORS do
        trails:setMissionMap("Warchest", door, string.format("Türchen%02d", door))
      end
    end
  end,
  disable = function(self, config) end,
}
