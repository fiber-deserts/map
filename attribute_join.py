import osmium
import geopandas
import pathlib

building_attributes = geopandas.read_file("buildings_joined.gpkg", ignore_geometry=True)
print(building_attributes)
print(building_attributes.dtypes)


way_attributes = geopandas.read_file("ways_joined.gpkg", ignore_geometry=True)
print(way_attributes)
print(way_attributes.dtypes)

found = building_attributes[building_attributes["osm_id"] == 139432]

print("found")
print(found)
print(found["BB-DBA"].array[0])


p = pathlib.Path("final.osm.pbf")
p.unlink(missing_ok=True)
writer = osmium.SimpleWriter(str(p))

class JoinHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.count = 0

    def join(self, o, node=False):
        if self.count % 1_000_000 == 0:
            print(self.count)
        self.count += 1

        # if o.id == 139406 or o.id == 139432 or o.id == 30173192 or o.id == 0:
        #     print(o, o.id)
        #     for t in o.tags:
        #         print(t)
        #     return o
        # return o

        if self.count < 25_000_000 or not o.tags:
            return o

        if node:
            found = building_attributes[building_attributes["osm_id"] == o.id]
        else:
            found = building_attributes[building_attributes["osm_way_id"] == o.id]
        if found.empty:
            found = way_attributes[way_attributes["osm_id"] == o.id]
        if found.empty:
            return o

        # if len(found) > 1:
        #     print(found)
        #     raise RuntimeError()

        newtags = []
        for t in o.tags:
            newtags.append((t.k, t.v))

        try:
            newtags.append(("broadband:block-count", str(len(found["BB-DBA"].array))))
            newtags.append(("broadband:best-dba", str(found["BB-DBA"].array[0])))
            newtags.append(("broadband:best-tech", str(found["BB-TECH"].array[0])))
            newtags.append(("broadband:fiber", str(int(min(found["BB-FIBER"].array)))))
            newtags.append(("broadband:fiber-provider", str(found["BB-F-PROV"].array[0])))
            newtags.append(("broadband:fiber-to-the-home", str(int(min(found["BB-FTTH"].array)))))
        except ValueError:
            print(found)
            return o
        # print(i, o, newtags)
        return o.replace(tags=newtags)

    def node(self, n):
        writer.add_node(self.join(n, node=True))

    def way(self, w):
        writer.add_way(self.join(w, node=False))

    def relation(self, r):
        writer.add_relation(self.join(r, node=False))


h = JoinHandler()
h.apply_file("washington-latest.osm.pbf")

writer.close()
