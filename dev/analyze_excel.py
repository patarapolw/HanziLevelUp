import pyexcel


def max_width(sheet_name):
    data = dict()
    for record in pyexcel.iget_records(file_name='../user/HanziLevelUp.xlsx', sheet_name=sheet_name):
        for k, v in record.items():
            data.setdefault(k, []).append(len(str(v)))

    pyexcel.free_resources()

    for k, v in data.items():
        data[k] = max(v)

    return data


if __name__ == '__main__':
    print(max_width('hanzi'))
    print(max_width('vocab'))
    print(max_width('sentences'))
