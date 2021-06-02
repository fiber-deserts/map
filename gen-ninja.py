import pathlib

print("pool mem_heavy")
print("  depth = 1")
print()
print("rule basemap")
print("  command = ../tilemaker/tilemaker --input $in --output $out --config config/tiles/basemap/config-openmaptiles.json --process config/tiles/basemap/process-openmaptiles.lua")
print("  pool = mem_heavy")
print()
print("rule tile-join")
print("  command = tile-join --force -o $out $in")
print("  pool = mem_heavy")
print()
print("rule dissolve-census-blocks")
print("  command = python cb-zoom-split.py $in")
print("  pool = mem_heavy")
print()
print("rule gpkg-join-single-layer")
print("  command = rm -f $out && ogrmerge.py -single -f GPKG -nln $layer_name -o $out $in")
print()
print("rule gpkg-join-layers")
print("  command = rm -f $out && ogrmerge.py -f GPKG -o $out $in")
#print("  pool = mem_heavy")
print()
print("rule unzip")
print("  command = unzip -d $$(dirname $out) $in")
print()
print("rule convert")
print("  command = ogr2ogr $out $in")
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
all_census_gpkg = {"states": [],
                   "counties": [],
                   "tracts": [],
                   "blocks": []}
for p in census_block_root.glob("*pophu.shp"):
    state_code = p.name.rsplit("_")[1]
    out = []
    for tier in all_census_gpkg:
        fn = f"gen/census_blocks/{state_code}-{tier}.gpkg"
        all_census_gpkg[tier].append(fn)
        out.append(fn)
    out = " ".join(out)
    print(f"build {out}: dissolve-census-blocks {p}")

print()

tier_fns = []
for tier in all_census_gpkg:
    fn = f"gen/census_blocks/us-{tier}.gpkg"
    tier_fns.append(fn)
    inputs = " ".join(all_census_gpkg[tier])
    print(f"build {fn}: gpkg-join-single-layer {inputs}")
    print(f"  layer_name = {tier}")
    print()
tier_fns = " ".join(tier_fns)
print(f"build gen/census_blocks/us-census.gpkg: gpkg-join-layers {tier_fns}")

print("build census: phony gen/census_blocks/us-census.gpkg")
print("build basemap: phony gen/basemap/us-basemap.mbtiles")


building_root = pathlib.Path("data/microsoft_buildings")
out = []
for p in building_root.glob("*geojson.zip"):
    parts = p.name.split(".")
    unzipped = "gen/buildings/" + ".".join(parts[:2])
    print(f"build {unzipped}: unzip {p}")
    geopackage = "gen/buildings/" + ".".join((parts[0], "gpkg"))
    print(f"build {geopackage}: convert {unzipped}")
    out.append(geopackage)

out = " ".join(out)
print(f"build gen/buildings/us-buildings.gpkg: gpkg-join-single-layer {out}")
print(f"  layer_name = buildings")

print("build buildings: phony gen/buildings/us-buildings.gpkg")
