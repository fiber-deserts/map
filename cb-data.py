import geopandas
import pandas

fastest = pandas.read_csv("fastest-by-block.csv")

shapes = {}
for i in range(53, 54):
    shapes[i] = geopandas.read_file(f"block_shapes/tabblock2010_{i:02d}_pophu.shp")


print(fastest)
print(fastest.dtypes)
wa = shapes[53]
wa["BLOCKID10"] = wa["BLOCKID10"].astype("int64")
print(wa)
print(wa.dtypes)
wa = wa.merge(fastest, left_on="BLOCKID10", right_on="census_block")
print(wa)
print(wa.dtypes)
wa.to_file("washington_census.shp")
