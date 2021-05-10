import geopandas

blocks = geopandas.read_file("washington_census.shp")
print(blocks)
print(blocks.dtypes)

buildings = geopandas.read_file(
    "washington-buildings.gpkg",
    ignore_fields=[
        "aeroway",
        "historic",
        "land_area",
        "landuse",
        "man_made",
        "military",
        "other_tags",
        "office",
        "place",
        "amenity",
        "admin_level",
        "barrier",
        "craft",
        "geological",
        "leisure",
        "natural",
        "shop",
        "sport",
        "tourism",
        "boundary"
    ],
)
print(buildings)
print(buildings.dtypes)

buildings["osm_id"] = buildings["osm_id"].fillna("0").astype("int64")
buildings["osm_way_id"] = buildings["osm_way_id"].fillna("0").astype("int64")
print(buildings)
print(buildings.dtypes)

blocks.to_crs(buildings.crs, inplace=True)

buildings_with_service = geopandas.sjoin(buildings, blocks, how="inner", op="intersects")
print(buildings_with_service)
print(buildings_with_service.dtypes)

buildings_with_service.to_file("buildings_joined.gpkg", driver="GPKG")
