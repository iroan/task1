import xlrd
import config
from datetime import datetime
from datetime import timedelta

sheets = xlrd.open_workbook('activity.xls')
table = sheets.sheet_by_name('新服')
rows = table.nrows


def get_row_contents(acticity_id):
    for item in range(2, table.nrows):
        if acticity_id == table.row_values(item)[0]:
            return table.row_values(item)


def handle_open_type_2(row_data, check_time):
    '''
    如果days_later存在,需要根据默认的开服时间来计算
    如果days_later为空,直接返回True
    '''
    if row_data[9] == '':
        return True
    else:
        open_time = timedelta(days=int(row_data[9]))
        start_time = str2date(config.OPEN_TYPE2_DEFAULT_VALUE)
        check_time = str2date(check_time)
        # print('{},{}'.format(check_time, open_time + start_time))
        if check_time > open_time + start_time:
            return True

def str2date(str_time, format='%Y%m%d%H%M%S'):
    return datetime.strptime(str_time, format).date()


def handle_open_type_1(row_data, check_time):
    '''
    实现方法:
        1. 把所有有关时间的数据(字符串)都转换为datetime数据类型
        1. 比较时间
    :param row_data:
    :param check_time:
    :return:
    '''
    start_time = row_data[4]
    if start_time == '':
        start_time = str2date(config.OPEN_TYPE_DEFAULT_VALUE)
    else:
        start_time = str2date(str(int(start_time)))

    if row_data[9] == '':
        open_time = timedelta()
    else:
        open_time = timedelta(days=int(row_data[9]))

    during_time = timedelta(days=row_data[7])
    tmp = str2date(check_time)
    down = start_time + open_time
    up = during_time + open_time + start_time

    if tmp >= down and tmp <= up:
        return True


def is_open(row_data, check_time):
    if row_data[6] == 1:
        return handle_open_type_1(row_data, check_time)
    if row_data[6] == 2:
        return handle_open_type_2(row_data, check_time)
    return False


def test2_2():
    print('in test2_2'.center(40, '*'))
    row_data = get_row_contents(32)
    print(is_open(row_data, '20180716000000'))
    print(is_open(row_data, '20180816000000'))


def test2_1():
    print('in test2_1'.center(40, '*'))
    row_data = get_row_contents(1)
    print(is_open(row_data, '20180716000000'))
    print(is_open(row_data, '20180717000000'))
    print(is_open(row_data, '20180718000000'))
    print(is_open(row_data, '20180719000000'))
    print(is_open(row_data, '20180720000000'))


def test1_1(row_data=get_row_contents(11)):
    print('in test1_1'.center(40, '*'))
    print(is_open(row_data, '20180702000000'))
    print(is_open(row_data, '20180703000000'))
    print(is_open(row_data, '20180704000000'))
    print(is_open(row_data, '20180705000000'))
    print(is_open(row_data, '20180706000000'))
    print(is_open(row_data, '20180707000000'))
    print(is_open(row_data, '20180708000000'))
    print(is_open(row_data, '20180709000000'))


def test1_2(row_data=get_row_contents(106)):
    print('in test1_2'.center(40, '*'))
    print(is_open(row_data, '20180716000000'))
    print(is_open(row_data, '20180717000000'))
    print(is_open(row_data, '20180718000000'))
    print(is_open(row_data, '20180719000000'))
    print(is_open(row_data, '20180720000000'))
    print(is_open(row_data, '20180721000000'))
    print(is_open(row_data, '20180722000000'))
    print(is_open(row_data, '20180723000000'))
    print(is_open(row_data, '20180724000000'))
    print(is_open(row_data, '20180725000000'))


def test1_3(row_data=get_row_contents(8)):
    print('in test1_3'.center(40, '*'))
    print(is_open(row_data, '20160407230000'))
    print(is_open(row_data, '20160408000000'))
    print(is_open(row_data, '20160408010000'))
    print(is_open(row_data, '20160402010000'))
    print(is_open(row_data, '20160403010000'))
    print(is_open(row_data, '20160507010000'))
    print(is_open(row_data, '20160508010000'))


if __name__ == '__main__':
    # test1_1()
    # test1_2()
    # test1_3()
    test2_1()
    test2_2()
