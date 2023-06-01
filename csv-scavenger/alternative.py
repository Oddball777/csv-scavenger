import csv
from collections import Counter

import pandas

with open("csv-scavenger/example_csvs/orgs copy.csv", "r", newline="") as csv_file:
    dialect = csv.Sniffer().sniff(csv_file.read(1024))
    csv_reader = csv.reader(csv_file, delimiter=dialect.delimiter)
    csv_file.seek(0)
    reader = csv.reader(csv_file, dialect)

    reader = list(reader)
    lengths = [len(row) for row in reader]
    counts = Counter(lengths)
    num_of_cols = counts.most_common(1)[0][0]

    for row in reader[::-1]:
        if len(row) != num_of_cols:
            reader.pop(reader.index(row))

# Determine if first row is header or start of data

df = pandas.DataFrame(reader)
df = df.infer_objects()

is_header = True
for item in df.iloc[0]:
    try:
        float(item)
        print("data")
        is_header = False
    except ValueError:
        print("header")
        break
if is_header:
    df.columns = df.iloc[0]
    df = df[1:]
print(df)
