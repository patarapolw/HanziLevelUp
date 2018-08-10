import csv
from pathlib import Path

import pyexcel_xlsxwx


def convert(filename):
    filename_path = Path(filename)
    data = {
        filename_path.stem: []
    }

    with open(filename_path, newline='') as f:
        reader = csv.reader(f)
        data[filename_path.stem].append(next(reader))
        for row in reader:
            true_row = []
            for item in row:
                if item.isdigit():
                    true_row.append(int(item))
                elif item.replace('.', '', 1).isdigit():
                    true_row.append(float(item))
                else:
                    true_row.append(item)

            data[filename_path.stem].append(true_row)

    pyexcel_xlsxwx.save_data(str(filename_path.with_suffix('.xlsx')), data, config={'format': None})


if __name__ == '__main__':
    convert('../CJKhyperradicals/database/chinese/hanzi_dict.csv')
