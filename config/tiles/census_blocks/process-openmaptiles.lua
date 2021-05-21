-- Data processing based on openmaptiles.org schema
-- https://openmaptiles.org/schema/
-- Copyright (c) 2016, KlokanTech.com & OpenMapTiles contributors.
-- Used under CC-BY 4.0

-- Enter/exit Tilemaker
function init_function()
end
function exit_function()
end

-- Implement Sets in tables
function Set(list)
	local set = {}
	for _, l in ipairs(list) do set[l] = true end
	return set
end

-- Meters per pixel if tile is 256x256
ZRES5  = 4891.97
ZRES6  = 2445.98
ZRES7  = 1222.99
ZRES8  = 611.5
ZRES9  = 305.7
ZRES10 = 152.9
ZRES11 = 76.4
ZRES12 = 38.2
ZRES13 = 19.1


node_keys = {}
-- function node_function(node)
-- end


-- function way_function(way)
-- end

-- function attribute_function(attr, layer)
-- 	return {}
-- end

-- ==========================================================
-- Common functions

-- Set minimum zoom level by area
function SetMinZoomByArea(way)
	local area=way:Area()
	if     area>ZRES5^2  then way:MinZoom(6)
	elseif area>ZRES6^2  then way:MinZoom(7)
	elseif area>ZRES7^2  then way:MinZoom(8)
	elseif area>ZRES8^2  then way:MinZoom(9)
	elseif area>ZRES9^2  then way:MinZoom(10)
	elseif area>ZRES10^2 then way:MinZoom(11)
	elseif area>ZRES11^2 then way:MinZoom(12)
	elseif area>ZRES12^2 then way:MinZoom(13)
	else                      way:MinZoom(14) end
end

-- ==========================================================
-- Lua utility functions

function split(inputstr, sep) -- https://stackoverflow.com/a/7615129/4288232
	if sep == nil then
		sep = "%s"
	end
	local t={} ; i=1
	for str in string.gmatch(inputstr, "([^"..sep.."]+)") do
		t[i] = str
		i = i + 1
	end
	return t
end

