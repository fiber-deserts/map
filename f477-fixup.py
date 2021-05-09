import csv

with open("fbd_us_with_satellite_jun2020_v1.csv", mode="rb") as csvfile:
    with open("fbd_us_with_satellite_jun2020_v1_fixed.csv", mode="wb") as out:
        i = 0
        while True:
            b = csvfile.read(1000)
            if not b:
                break
            if b"\xf3" in b:
                b = b.replace(b"\xf3", "ó".encode("utf-8"))
            if b"\xe9" in b:
                b = b.replace(b"\xe9", "é".encode("utf-8"))
            try:
                b.decode("utf-8")
                out.write(b)
            except UnicodeDecodeError as error:
                print(b)
                print(error)
                print(i)
                break

            # print(i, )
            i += 1
    # csvfile.seek(0)
    # reader = csv.DictReader(csvfile)
    # types = {}
    # i = 0
    # try:
    #     for row in reader:
    #         t = row["TechCode"]
    #         if t not in types:
    #             types[t] = 0
    #         types[t] += 1
    #         if i < 10:
    #             print(row)
    #         i += 1
    # except UnicodeDecodeError as e:
    #     print(csvfile.tell())

print(i, types)
