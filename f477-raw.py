import csv

techcodes = {
    "10": "asymmetric-xdsl",
    "11": "adsl2/2+",
    "12": "vdsl",
    "20": "symmetric-xdsl",
    "30": "other-copper",
    "40": "cable-other",
    "41": "cable-docsis<2",
    "42": "cable-docsis3.0",
    "43": "cable-docsis3.1",
    "50": "fiber",
    "60": "satellite",
    "70": "fixed-wireless",
    "90": "power-line",
    "0": "other",
}

blocks = {}

with open("fbd_us_with_satellite_jun2020_v1_fixed.csv", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    try:
        for row in reader:
            bc = row[9]
            if bc not in blocks:
                blocks[bc] = []
            blocks[bc].append(row)

    except UnicodeDecodeError as e:
        print(csvfile.tell())

# print()
# print(providers)
# # print()
# # print(hocos)
# print()
# print(speeds)

print("loaded data")

with open("fastest-by-block.csv", "w") as csvfile:
    fieldnames = [
        "census_block",
        "broadband:fastest-dba",
        "broadband:fastest-tech",
        "broadband:up",
        "broadband:down",
        "broadband:fiber",
        "broadband:total",
        "broadband:ftth",
        "broadband:fiber-provider"
    ]
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()
    i = 0
    for bc in blocks:
        print(blocks[bc])
        i += 1
        break
        # providers = {}
        # hocos = {}
        # speeds = {}
        #             t = row["TechCode"]
        #     if t not in types:
        #         types[t] = 0
        #     types[t] += 1
        #     if t not in speeds:
        #         speeds[t] = {"up": {}, "down": {}}
        #     down = float(row["MaxAdDown"])
        #     if down not in speeds[t]["down"]:
        #         speeds[t]["down"][down] = 0
        #     speeds[t]["down"][down] += 1
        #     up = float(row["MaxAdUp"])
        #     if up not in speeds[t]["up"]:
        #         speeds[t]["up"][up] = 0
        #     speeds[t]["up"][up] += 1

        #     p = row["DBAName"].lower().replace(" ", "-").replace(",", "")

        #     bc = row["BlockCode"]
        #     if bc not in blocks:
        #         blocks[bc] = {
        #             "broadband:up": -1,
        #             "broadband:down": -1,
        #             "census_block": bc,
        #             "broadband:total": -1,
        #             "broadband:fiber": False,
        #             "broadband:ftth": False
        #         }
        #     if (up + down) > blocks[bc]["broadband:total"]:
        #         blocks[bc]["broadband:fastest-dba"] = p
        #         blocks[bc]["broadband:down"] = down
        #         blocks[bc]["broadband:fastest-tech"] = techcodes[t]
        #         blocks[bc]["broadband:up"] = up
        #         blocks[bc]["broadband:total"] = up + down
        #     if bc == "530319503005005":
        #         print(row)
        #     if t == "50":
        #         blocks[bc]["broadband:fiber"] = True
        #         blocks[bc]["broadband:ftth"] = blocks[bc]["broadband:ftth"] or row["Consumer"] == "1"
        #         blocks[bc]["broadband:fiber-provider"] = row["ProviderName"].lower().replace(" ", "-").replace(",", "")

        #     # h = row["HocoNum"]
        #     # if h not in hocos:
        #     #     hocos[h] = set()
        #     # hocos[h].add(row["HocoFinal"])
        #     if i < 10:
        #         print(row)
        #     elif i < 1000000:
        #         # print(row)
        #         pass
        #     elif i % 1000000 == 0:
        #         print(i)
        #     else:
        #         # break
        #         pass
        #     i += 1

        writer.writerow(blocks[bc])

