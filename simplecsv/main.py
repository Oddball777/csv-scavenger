import pandas as pd
from collections import Counter
from tssplit import tssplit  # type: ignore
from typing import Optional


def _determine_format(lines: list[str]) -> tuple[str, int]:
    formats: list[tuple[str, int]] = []
    for line in lines:
        for delim in [";", ",", " ", "\t", "\n", "\r", "\r\n"]:
            num_of_columns = len(line.strip().split(delim))
            if num_of_columns > 1:
                formats.append((delim, num_of_columns))
    counter = Counter(formats)
    try:
        format: tuple[str, int] = counter.most_common(1)[0][0]
    except IndexError:
        raise IndexError(
            "No delimiter found. Currently supported delimiters are the comma, ;, \\t, \\n, \\r, \\r\\n, and whitespace."
        )
    return format


def _determine_header_start_last(
    format: tuple[str, int], lines: list[str]
) -> tuple[Optional[int], Optional[int], Optional[int]]:
    header_line = None
    last_line = None

    step = len(lines) // 100 if len(lines) > 100 else 1
    for i, line in enumerate(lines):
        if i % step == 0:
            num_of_columns = len(
                tssplit(line.strip(), quote='"', delimiter=format[0], escape="")  # type: ignore
            )
            if num_of_columns == format[1] and header_line == None:
                header_line = i
            elif num_of_columns != format[1] and header_line != None:
                last_line = i
                break
    if last_line == None:
        last_line = len(lines) - 1
    first_line: Optional[int] = header_line + 1 if header_line != None else None
    return header_line, first_line, last_line


def read_csv(file_path: str) -> pd.DataFrame:
    with open(file_path, "r") as file:
        lines = file.readlines()

    format = _determine_format(lines)

    header_row, data_start_row, data_end_row = _determine_header_start_last(
        format, lines
    )

    if header_row == None or data_start_row == None or data_end_row == None:
        raise ValueError("Probleeeem")

    data = pd.read_csv(  # type: ignore
        file_path,
        sep=format[0],
        skiprows=data_start_row - 1,
        nrows=data_end_row - data_start_row,
        engine="python",
    )

    if len(data) == 0:
        raise ValueError(
            f"CSV data is not in a recognized format. Detected delimiter is: {format[0]}"
        )

    return data


if __name__ == "__main__":
    data_people = read_csv("simplecsv/example_csvs/people.csv")
    data_faithful = read_csv("simplecsv/example_csvs/faithful.csv")
    data_orgs = read_csv("simplecsv/example_csvs/orgs.csv")
    data_other = read_csv("simplecsv/example_csvs/other.csv")
    data_bla = read_csv("simplecsv/example_csvs/bla.csv")
    data_not_data = read_csv("simplecsv/example_csvs/not_data.csv")
    print(data_not_data)
