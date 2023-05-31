# SimpleCSV

SimpleCSV is a simple CSV parser for Python which can detect the delimiter automatically and can parse CSV files with quoted fields. It can also detect the header row and the start and end of the data rows automatically. For most use cases, you can simply call ```simplecsv.read_csv(filename)``` and get a pandas DataFrame back.

## Installation

```text
pip install simplecsv
```

## Usage

```python
import simplecsv

# Read a CSV file into a pandas DataFrame
data_1 = simplecsv.read_csv('data.csv')

# Read a CSV file into a list of lists
data_2 = simplecsv.read_csv('data.csv', as_list=True)

# Read a CSV file into a list of dicts
data_3 = simplecsv.read_csv('data.csv', as_dict=True)

# Read a CSV file into a list of namedtuples
data_4 = simplecsv.read_csv('data.csv', as_namedtuple=True)
```
