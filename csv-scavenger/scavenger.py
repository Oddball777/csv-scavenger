import pandas as pd
from collections import Counter
from tssplit import tssplit  # type: ignore
from typing import Optional


def _determine_format(lines: list[str]) -> tuple[str, int]:
    formats: list[tuple[str, int]] = []
    step = max(1, len(lines) // 100)
    for i in range(0, len(lines), step):
        line = lines[i]
        for delim in [";", ",", " ", "\t", "\n", "\r", "\r\n"]:
            num_of_columns = len(
                tssplit(line.strip(), quote='"', delimiter=delim, escape="")  # type: ignore
            )
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
    header_line = "undefined"
    last_line = "undefined"
    first_line = "undefined"

    for i, line in enumerate(lines):
        num_of_columns = len(
            tssplit(line.strip(), quote='"', delimiter=csv_format[0], escape="")  # type: ignore
        )
        if num_of_columns == csv_format[1] and header_line == "undefined":
            is_header = True
            for item in tssplit(
                line.strip(), quote='"', delimiter=csv_format[0], escape=""
            ):
                try:
                    float(item)
                    is_header = False
                    break
                except ValueError:
                    pass
            if is_header:
                header_line = i
                first_line = i + 1
            else:
                print("no header")
                header_line = "none"
                first_line = i
        elif num_of_columns != csv_format[1] and header_line != "undefined":
            last_line = i
            break

    if last_line == "undefined":
        last_line = len(lines)
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
    if (
        header_row == "undefined"
        or data_start_row == "undefined"
        or data_end_row == "undefined"
    ):
        raise ValueError("Could not determine header and data rows.")

    if header_row == "none":
        data = pd.read_csv(  # type: ignore
            file_path,
            sep=csv_format[0],
            skiprows=data_start_row - 1,
            nrows=data_end_row - data_start_row,
            engine="python",
            header=None,
        )
    else:
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
    print(data_multimeter)
