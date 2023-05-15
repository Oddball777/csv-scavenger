import pandas as pd


def get_csv_info(file_path: str) -> pd.DataFrame:
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Find the middle row to determine the delimiter and format
    middle_row = lines[len(lines) // 2].strip()
    if "," in middle_row and ";" in middle_row:
        raise ValueError("Could not determine delimeter")
    if "," in middle_row:
        delimiter = ","
    elif ";" in middle_row:
        delimiter = ";"
    else:
        raise ValueError("Could not determine delimiter")

    number_of_columns = len(middle_row.split(delimiter))

    # Find the header row and data start/end rows
    header_row = None
    data_start_row = None
    data_end_row = None

    for i, line in enumerate(lines):
        if len(line.strip().split(delimiter)) == number_of_columns:
            if header_row == None:
                header_row = i
                data_start_row = i + 1
            data_end_row = i
        elif header_row != None:
            break

    if header_row == None or data_start_row == None or data_end_row == None:
        raise ValueError("Probleeeem")

    return pd.read_csv(  # type: ignore
        file_path,
        sep=delimiter,
        skiprows=data_start_row - 1,
        nrows=data_end_row - data_start_row + 1,
    )


data = get_csv_info("simplecsv/example_csvs/faithful.csv")
print(data)
