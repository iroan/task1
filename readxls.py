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
    start_time = int(config.OPEN_TYPE_DEFAULT_VALUE)
    during_time = row_data[7] * 1000000
    tmp = int(check_time)
    if tmp >= start_time and tmp <= during_time + start_time:
        return True

def is_open(row_data, check_time):
    if row_data[6] == 1:
        return handle_open_type_1(row_data, check_time)
    if row_data[6] == 2:
        return handle_open_type_2(row_data, check_time)
    return False


def test_2():
    row_data = get_row_contents(11)
    print(is_open(row_data, '20180702000000'))

def test_1():
    row_data = get_row_contents(11)
    print(is_open(row_data, '20180702000000'))
    print(is_open(row_data, '20180703000000'))
    print(is_open(row_data, '20180704000000'))
    print(is_open(row_data, '20180705000000'))
    print(is_open(row_data, '20180706000000'))
    print(is_open(row_data, '20180707000000'))
    print(is_open(row_data, '20180708000000'))
    print(is_open(row_data, '20180709000000'))


if __name__ == '__main__':
    # test_1()
    test_2()
