# CSV-Scavenger

CSV-Scavenger is a simple CSV parser for Python which can detect the delimiter automatically and can parse CSV files with quoted fields. It can also detect the header row and the start and end of the data rows automatically. For most use cases, you can simply call ```sv.read_csv(filename)``` and get a pandas DataFrame back.

See the ```csv-scavenger/example_csvs``` directory for some example CSV files which are parsed correctly by CSV-Scavenger.

## Installation

```text
pip install csv-scavenger
```

## Usage

```python
import scavenger as sv

# Read a CSV file into a pandas DataFrame
df = sv.read_csv('data.csv')
```
