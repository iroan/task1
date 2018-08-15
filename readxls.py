import xlrd

sheets = xlrd.open_workbook('activity.xls')
table = sheets.sheet_by_name('新服')
rows = table.nrows


def get_row_contents(acticity_id):
    for item in range(2, table.nrows):
        if acticity_id == table.row_values(item)[0]:
            return table.row_values(item)


def handle_open_type_1(row_data):
    pass


def handle_open_type_2(row_data):
    print('*' * 80)
    pass


def is_open(row_data):
    if row_data[6] == 2:
        handle_open_type_2(row_data)


if __name__ == '__main__':
    row_data = get_row_contents(1)
    is_open(row_data)
