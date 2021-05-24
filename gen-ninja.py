import pathlib

print("pool mem_heavy")
print("  depth = 1")
print()
print("rule basemap")
print("  command = ../tilemaker/tilemaker --input $in --output $out --config config/tiles/basemap/config-openmaptiles.json --process config/tiles/basemap/process-openmaptiles.lua")
print("  pool = mem_heavy")
print()
print("rule tile-join")
print("  command = tile-join -o $out $in")
print("  pool = mem_heavy")
print()
print("rule dissolve-census-blocks")
print("  command = python cb-zoom-split.py $in")
print("  pool = mem_heavy")
print()
print("rule census-tiles")
print("  command = ../tilemaker/tilemaker --output $out --config $in --process config/tiles/census_blocks/process-openmaptiles.lua")
print("  pool = mem_heavy")
print()
print("rule gen-census-config")
print("  command = jinja -D state_code $state_code $in > $out")
print()

osm_root = pathlib.Path("data/osm/")
basemap_root = pathlib.Path("gen/basemap")
all_basemap = []
for p in osm_root.glob("*-latest.osm.pbf"):
    state = p.name.rsplit("-", maxsplit=1)[0]
    if state == "us":
        continue
    out = basemap_root / (state + ".mbtiles")
    all_basemap.append(str(out))
    print(f"build {out}: basemap {p}")

print()
all_basemap = " ".join(all_basemap)
print(f"build gen/basemap/us-basemap.mbtiles: tile-join {all_basemap}")
print()

census_block_root = pathlib.Path("data/census_block_shapes")
all_census_tiles = []
for p in census_block_root.glob("*pophu.shp"):
    state_code = p.name.rsplit("_")[1]
    out = f"gen/census_blocks/{state_code}-blocks.shp gen/census_blocks/{state_code}-tracts.shp gen/census_blocks/{state_code}-counties.shp gen/census_blocks/{state_code}-state.shp"
    print(f"build {out}: dissolve-census-blocks {p}")
    census_config = f"gen/census_blocks/{state_code}-config.json"
    print(f"build {census_config}: gen-census-config config/tiles/census_blocks/config-openmaptiles.json.jinja")
    print(f"  state_code = {state_code}")
    tile_out = f"gen/census_blocks/{state_code}.mbtiles"
    all_census_tiles.append(tile_out)
    print(f"build {tile_out}: census-tiles {census_config}")
    print()

all_census_tiles = " ".join(all_census_tiles)
print(f"build gen/census_blocks/us-census.mbtiles: tile-join {all_census_tiles}")
print()

print("build census: phony gen/census_blocks/us-census.mbtiles")
print("build basemap: phony gen/basemap/us-basemap.mbtiles")
