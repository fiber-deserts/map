import geopandas

blocks = geopandas.read_file("washington_census.shp")
print(blocks)
print(blocks.dtypes)

# buildings = geopandas.read_file(
#     "washington-buildings.gpkg",
#     ignore_fields=[
#         "aeroway",
#         "historic",
#         "land_area",
#         "landuse",
#         "man_made",
#         "military",
#         "other_tags",
#         "office",
#         "place",
#         "amenity",
#         "admin_level",
#         "barrier",
#         "craft",
#         "geological",
#         "leisure",
#         "natural",
#         "shop",
#         "sport",
#         "tourism",
#         "boundary"
#     ],
# )
# print(buildings)
# print(buildings.dtypes)

# buildings["osm_id"] = buildings["osm_id"].fillna("0").astype("int64")
# buildings["osm_way_id"] = buildings["osm_way_id"].fillna("0").astype("int64")
# print(buildings)
# print(buildings.dtypes)

# blocks.to_crs(buildings.crs, inplace=True)

# buildings_with_service = geopandas.sjoin(buildings, blocks, how="inner", op="intersects")
# print(buildings_with_service)
# print(buildings_with_service.dtypes)

# buildings_with_service.to_file("buildings_joined.gpkg", driver="GPKG")

# del buildings
# del buildings_with_service

ways = geopandas.read_file(
    "washington-ways.gpkg",
    ignore_fields=[
        "other_tags",
        "z_order",
        "man_made",
        "barrier",
        "aerialway",
        "waterway"
    ],
)

ways["osm_id"] = ways["osm_id"].fillna("0").astype("int64")
# ways["osm_way_id"] = ways["osm_way_id"].fillna("0").astype("int64")
print(ways)
print(ways.dtypes)

blocks.to_crs(ways.crs, inplace=True)

ways_with_service = geopandas.sjoin(ways, blocks, how="inner", op="intersects")
print(ways_with_service)
print(ways_with_service.dtypes)

ways_with_service.to_file("ways_joined.gpkg", driver="GPKG")
