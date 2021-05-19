import csv
import json
import pathlib

root = pathlib.Path("blocks") 
with open("fbd_us_with_satellite_jun2020_v1_fixed.csv", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    i = 0
    try:
        for row in reader:
            if i % 1000000 == 0:
                print(i)
            bc = row[9]
            if bc == "BlockCode":
                continue
            state = bc[:2]
            county = bc[2:5]
            tract = bc[5:11]
            block = bc[-4:]
            tract_dir = root / state / county / tract
            tract_dir.mkdir(parents=True, exist_ok=True)
            block_file = tract_dir / (block + ".json")
            if block_file.is_file():
                with block_file.open() as f:
                    info = json.load(f)
            else:
                info = {"f477": []}
            info["f477"].append(row)

            with block_file.open("w") as f:
                json.dump(info, f)
            i += 1

    except UnicodeDecodeError as e:
        print(csvfile.tell())
