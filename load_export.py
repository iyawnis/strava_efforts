import csv

with open("export.csv", "r") as f:
    reader = csv.reader(f)
    columns = next(reader)
    print(columns)
