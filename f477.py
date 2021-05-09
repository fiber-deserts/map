import csv

with open('Area_Table_June_2020_V1.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    types = {}
    i = 0
    for row in reader:
        t = row["type"]
        if t not in types:
            types[t] = 0
        types[t] += 1
        if i < 10:
            print(row)
        i += 1

print(i, types)
