import xlrd
import config
sheets = xlrd.open_workbook('activity.xls')
table = sheets.sheet_by_name('新服')
rows = table.nrows

def get_row_contents(acticity_id):
    for item in range(2, table.nrows):
        if acticity_id == table.row_values(item)[0]:
            return table.row_values(item)


def handle_open_type_2(row_data, check_time):

    pass


def handle_open_type_1(row_data, check_time):
    start_time = row_data[4]
    tmp = int(check_time)
    if tmp > int(config.OPEN_TYPE_DEFAULT_VALUE):
        return True


def is_open(row_data, check_time):
    if row_data[6] == 1:
        handle_open_type_1(row_data, check_time)
    if row_data[6] == 2:
        handle_open_type_2(row_data, check_time)

    return False


if __name__ == '__main__':
    row_data = get_row_contents(32)
    is_open(row_data, '20180703000000')
