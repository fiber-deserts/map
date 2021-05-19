import geopandas

blocks = geopandas.read_file("washington_census.shp")
print(blocks)
print(blocks.dtypes)

process_ways = False
process_buildings = True

if process_buildings:
    buildings = geopandas.read_file(
        "Microsoft-Washington.geojson"
    )
    print(buildings)
    print(buildings.dtypes)

    blocks.to_crs(buildings.crs, inplace=True)

    buildings_with_service = geopandas.sjoin(buildings, blocks, how="inner", op="intersects")
    print(buildings_with_service)
    print(buildings_with_service.dtypes)

    buildings_with_service.to_file("buildings_joined.gpkg", driver="GPKG")

    del buildings
    del buildings_with_service

if process_ways:
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
