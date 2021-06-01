import geopandas
import sys

blank_tract = 10000
blank_county = 1000000 * blank_tract
blank_state = blank_county * 1000

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

blocks.set_index("BLOCKID10").to_file(f"gen/census_blocks/{state_code}-blocks.gpkg", driver="GPKG", layer="census_blocks", index=True)
tracts.set_index("BLOCKID10").to_file(f"gen/census_blocks/{state_code}-tracts.gpkg", driver="GPKG", layer="census_tracts", index=True)
counties = counties.set_index("BLOCKID10")
print(counties)
counties.to_file(f"gen/census_blocks/{state_code}-counties.gpkg", driver="GPKG", layer="census_counties", index=True)
state.set_index("BLOCKID10").to_file(f"gen/census_blocks/{state_code}-state.gpkg", driver="GPKG", layer="census_states", index=True)
