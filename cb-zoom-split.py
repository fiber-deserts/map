import geopandas
import sys

blocks = geopandas.read_file(sys.argv[1])
del blocks["PARTFLG"]
del blocks["STATEFP10"]
del blocks["COUNTYFP10"]
del blocks["TRACTCE10"]
del blocks["BLOCKCE"]
blocks["pixel_area"] = blocks["geometry"].to_crs(epsg=3857).area
blocks["equal_area"] = blocks["geometry"].to_crs(epsg=2163).area
blocks["BLOCKID10"] = blocks["BLOCKID10"].astype("int64")

tracts = blocks.copy(deep=True)
blank_tract = 10000
tracts["BLOCKID10"] = tracts["BLOCKID10"].map(lambda x: (x // blank_tract) * blank_tract).astype("int64")
tracts = tracts.dissolve(by="BLOCKID10", aggfunc="sum", as_index=False)

counties = tracts.copy(deep=True)
blank_county = 1000000 * blank_tract
counties["BLOCKID10"] = counties["BLOCKID10"].copy().map(lambda x: (x // blank_county) * blank_county).astype("int64")
counties = counties.dissolve(by="BLOCKID10", aggfunc="sum", as_index=False)

state = counties.copy(deep=True)
blank_state = blank_county * 1000
state["BLOCKID10"] = state["BLOCKID10"].map(lambda x: (x // blank_state) * blank_state).astype("int64")
state = state.dissolve(by="BLOCKID10", aggfunc="sum", as_index=False)

for zoom in range(0, 14):
    print(zoom)
    min_area = (30 ** 2) * ((14 - zoom) ** 2)
    big_enough = counties["pixel_area"] >= min_area
    if not big_enough.all():
        state.to_file(f"zoom{zoom:02d}.shp")
        continue
    shapes = geopandas.GeoDataFrame()
    for county in counties.itertuples():
        county_id = county.BLOCKID10
        match = tracts["BLOCKID10"].map(lambda x: county_id < x < (county_id + blank_county))
        county_tracts = tracts[match]
        big_enough = county_tracts["pixel_area"] >= min_area
        if not big_enough.all():
            shapes = shapes.append(county)
            continue
        for tract_id in county_tracts["BLOCKID10"]:
            tract = county_tracts[county_tracts["BLOCKID10"] == tract_id]
            match = blocks["BLOCKID10"].map(lambda x: tract_id < x < (tract_id + blank_tract))
            tract_blocks = blocks[match]
            #print(tract_blocks)
            big_enough = tract_blocks["pixel_area"] >= min_area
            if not big_enough.all():
                shapes = shapes.append(tract)
            else:
                shapes = shapes.append(tract_blocks)
    del shapes["pixel_area"]
    shapes["block"] = shapes["BLOCKID10"] % blank_tract
    shapes["tract"] = (shapes["BLOCKID10"] // blank_tract) % 1000000
    shapes["county"] = (shapes["BLOCKID10"] // blank_county) % 1000
    shapes["state"] = (shapes["BLOCKID10"] // blank_state)
    print(shapes)
    print(shapes.dtypes)
    shapes.to_file(f"zoom{zoom:02d}.shp")
