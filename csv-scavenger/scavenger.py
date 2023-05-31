import pandas as pd
from collections import Counter
from tssplit import tssplit  # type: ignore
from typing import Optional


def _determine_format(lines: list[str]) -> tuple[str, int]:
    formats: list[tuple[str, int]] = []
    step = len(lines) // 100 if len(lines) > 100 else 1
    for i, line in enumerate(lines):
        if i % step == 0:
            for delim in [";", ",", " ", "\t", "\n", "\r", "\r\n"]:
                num_of_columns = len(line.strip().split(delim))
                if num_of_columns > 1:
                    formats.append((delim, num_of_columns))
    counter = Counter(formats)
    try:
        csv_format: tuple[str, int] = counter.most_common(1)[0][0]
    except IndexError:
        raise IndexError(
            "No delimiter found. Currently supported delimiters are the comma, ;, \\t, \\n, \\r, \\r\\n, and whitespace."
        )
    return csv_format


def _determine_header_start_last(
    csv_format: tuple[str, int], lines: list[str]
) -> tuple[Optional[int], Optional[int], Optional[int]]:
    header_line = None
    last_line = None

    for i, line in enumerate(lines):
        num_of_columns = len(
            tssplit(line.strip(), quote='"', delimiter=csv_format[0], escape="")  # type: ignore
        )
        if num_of_columns == csv_format[1] and header_line == None:
            header_line = i
        elif num_of_columns != csv_format[1] and header_line != None:
            last_line = i
            break
    if last_line == None:
        last_line = len(lines)
    first_line: Optional[int] = header_line + 1 if header_line != None else None
    return header_line, first_line, last_line


def read_csv(file_path: str) -> pd.DataFrame:
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")

    csv_format = _determine_format(lines)

    header_row, data_start_row, data_end_row = _determine_header_start_last(
        csv_format, lines
    )

    if header_row == None or data_start_row == None or data_end_row == None:
        raise ValueError("Could not determine header and data rows.")

    data = pd.read_csv(  # type: ignore
        file_path,
        sep=csv_format[0],
        skiprows=data_start_row - 1,
        nrows=data_end_row - data_start_row,
        engine="python",
    )

    if len(data) == 0:
        raise ValueError(
            f"CSV data is not in a recognized format. Detected delimiter is: {csv_format[0]}"
        )

    return data


if __name__ == "__main__":
    data_people = read_csv("csv-scavenger/example_csvs/people.csv")
    data_faithful = read_csv("csv-scavenger/example_csvs/faithful.csv")
    data_orgs = read_csv("csv-scavenger/example_csvs/orgs.csv")
    data_health = read_csv("csv-scavenger/example_csvs/health.csv")
    data_multimeter = read_csv("csv-scavenger/example_csvs/multimeter.csv")
    print(data_health)
