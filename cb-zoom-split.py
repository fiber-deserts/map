import geopandas
import sys

blank_tract = 10000
blank_county = 1000000 * blank_tract
blank_state = blank_county * 1000

def output_shapes(shapes, fn):
    shapes["block"] = shapes["BLOCKID10"] % blank_tract
    shapes["tract"] = (shapes["BLOCKID10"] // blank_tract) % 1000000
    shapes["county"] = (shapes["BLOCKID10"] // blank_county) % 1000
    shapes["state"] = (shapes["BLOCKID10"] // blank_state)
    del shapes["BLOCKID10"]
    print(shapes)
    print(shapes.dtypes)
    shapes.to_file(fn)


blocks = geopandas.read_file(sys.argv[1])

state_code = sys.argv[1].split("_")[-2]
del blocks["PARTFLG"]
del blocks["STATEFP10"]
del blocks["COUNTYFP10"]
del blocks["TRACTCE10"]
del blocks["BLOCKCE"]
blocks["equal_area"] = blocks["geometry"].to_crs(epsg=2163).area
blocks["BLOCKID10"] = blocks["BLOCKID10"].astype("int64")

tracts = blocks.copy(deep=True)
tracts["BLOCKID10"] = tracts["BLOCKID10"].map(lambda x: (x // blank_tract) * blank_tract).astype("int64")
tracts = tracts.dissolve(by="BLOCKID10", aggfunc="sum", as_index=False)

counties = tracts.copy(deep=True)
counties["BLOCKID10"] = counties["BLOCKID10"].copy().map(lambda x: (x // blank_county) * blank_county).astype("int64")
counties = counties.dissolve(by="BLOCKID10", aggfunc="sum", as_index=False)

state = counties.copy(deep=True)
state["BLOCKID10"] = state["BLOCKID10"].map(lambda x: (x // blank_state) * blank_state).astype("int64")
state = state.dissolve(by="BLOCKID10", aggfunc="sum", as_index=False)

output_shapes(blocks, f"gen/census_blocks/{state_code}-blocks.shp")
output_shapes(tracts, f"gen/census_blocks/{state_code}-tracts.shp")
output_shapes(counties, f"gen/census_blocks/{state_code}-counties.shp")
output_shapes(state, f"gen/census_blocks/{state_code}-state.shp")
