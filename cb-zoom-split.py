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
blocks["BLOCKID10"] = blocks["BLOCKID10"].astype("uint64")
print(blocks)
print(blocks.dtypes)
print(blocks.crs)

tracts = blocks.copy(deep=False)
blank_tract = 10000
tracts["BLOCKID10"] = tracts["BLOCKID10"].map(lambda x: (x // blank_tract) * blank_tract)
print(blocks)
tracts = tracts.dissolve(by="BLOCKID10", aggfunc="sum", as_index=False)

print("tracts")
print(tracts)
print(tracts.dtypes)

counties = tracts.copy(deep=False)
blank_county = 1000000 * blank_tract
counties["BLOCKID10"] = counties["BLOCKID10"].map(lambda x: (x // blank_county) * blank_county)
counties = counties.dissolve(by="BLOCKID10", aggfunc="sum", as_index=False)

print(counties)
print(counties.dtypes)

state = counties.copy(deep=False)
blank_state = blank_county * 1000
state["BLOCKID10"] = state["BLOCKID10"].map(lambda x: (x // blank_state) * blank_state)
state = state.dissolve(by="BLOCKID10", aggfunc="sum", as_index=False)

print(state)
print(state.dtypes)

for zoom in range(0, 14):
    print(zoom)
    min_area = (19.1 ** 2) * ((14 - zoom) ** 2)
    big_enough = counties["pixel_area"] >= min_area
    too_small = counties["BLOCKID10"][counties["pixel_area"] < min_area]
    print(too_small)
    print()
    print("BIG")
    print(big_enough.all())
    print()
    print(counties["BLOCKID10"][big_enough])
    break

# wa.to_file("washington_census.shp")
