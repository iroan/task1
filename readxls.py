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


def handle_open_type_6(row_data, check_time):
    '''
    处理方法:
        1. 根据开启时间,开启后多少天开启来计算真正的开启时间.real_open_time
        1. 如果check_time < real_open_time,返回None
        1. 判断check_time 是否在real_open_time和其与持续时间之内
    :param row_data:
    :param check_time:
    :return:
    '''
    pass
    open_time = None
    if row_data[4] == '':
        open_time = str2date(config.OPEN_TYPE6_DEFAULT_VALUE)
    else:
        open_time = str2date(row_data[4])
    offet = timedelta(days=int(row_data[9]))
    last_time = timedelta(days=int(row_data[7]))
    real_open_time = open_time + offet
    check_time = str2date(check_time)
    if check_time >= real_open_time and check_time < real_open_time + last_time:
        return True

def handle_open_type_5(row_data, check_time):
    '''
    处理方法:
        1. 穷举法失败(因为时间'不连续')
        1. 先判断是否大于开服时间(固定设置)和持续时间,不是返回false
        1. 在for循环中依照轮数和间隔比较
    :param row_data:
    :param check_time:
    :return:
    '''
    check_time = str2date(check_time)
    open_time = str2date(config.OPEN_TYPE5_DEFAULT_VALUE)
    if check_time < open_time:
        return

    offset = None
    if row_data[7] == '':
        return
    else:
        offset = timedelta(days=int(row_data[7]))

    times = int(row_data[11])
    space = timedelta(days=int(row_data[12]))
    start = open_time
    for _time in range(times):
        end = start + offset
        if check_time >= start and check_time < end:
            return True
        start += space
        start += offset


def handle_open_type_4(row_data, check_time):
    '''
    实现:
        1. 如果持续时间为空,那么大于建角时间,就返回True
        1. 如果持续时间不为空,那么大于建角时间与持续时间的和,就返回True
    :param row_data:
    :param check_time:
    :return:
    '''
    offset = timedelta()
    if row_data[7] != '':
        offset = timedelta(days=int(row_data[7]))
    start_time = str2date(config.OPEN_TYPE4_DEFAULT_VALUE)
    end_time = start_time + offset
    tmp = str2date(check_time)
    if tmp >= start_time and tmp < end_time:
        return True
def handle_open_type_3(row_data, check_time):
    '''
    实现:
        1. 如果days_later为空,只需要比较开始时间和关闭时间
        1. 如果days_later不为空,需要添加到开始时间比较
    :param row_data:
    :param check_time:
    :return:
    '''
    offset = timedelta()
    if row_data[9] != '':
        offset = timedelta(days=int(row_data[9]))
    start_time = str2date(str(int(row_data[4])))
    end_time = str2date(str(int(row_data[5])))
    tmp = str2date(check_time)

    # print('{},{},{}'.format(start_time, tmp , end_time))

    if tmp >= start_time and tmp < end_time + offset:
        return True

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
        if check_time >= open_time + start_time:
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

    if tmp >= down and tmp < up:
        return True


def is_open(row_data, check_time):
    if row_data[6] == 1:
        return handle_open_type_1(row_data, check_time)
    if row_data[6] == 2:
        return handle_open_type_2(row_data, check_time)
    if row_data[6] == 3:
        return handle_open_type_3(row_data, check_time)
    if row_data[6] == 4:
        return handle_open_type_4(row_data, check_time)
    if row_data[6] == 5:
        return handle_open_type_5(row_data, check_time)
    if row_data[6] == 6:
        return handle_open_type_6(row_data, check_time)
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


def test3_1(row_data=get_row_contents(3)):
    print('in test3_1'.center(40, '*'))
    print(is_open(row_data, '20180803000000'))
    print(is_open(row_data, '20180809000000'))
    print(is_open(row_data, '20180810000000'))
    print(is_open(row_data, '20180811000000'))
    print(is_open(row_data, '20180812000000'))
    print(is_open(row_data, '20180813000000'))
    print(is_open(row_data, '20180814000000'))

def test3_2(row_data=get_row_contents(6)):
    print('in test3_2'.center(40, '*'))
    print(is_open(row_data, '20170119000000'))
    print(is_open(row_data, '20170120000000'))
    print(is_open(row_data, '20170124000000'))
    print(is_open(row_data, '20170125000000'))
    print(is_open(row_data, '20170126000000'))
    print(is_open(row_data, '20170127000000'))


def test4_1(row_data=get_row_contents(2)):
    print('in test4_1'.center(40, '*'))
    print(is_open(row_data, '20180702000000'))
    print(is_open(row_data, '20180703000000'))
    print(is_open(row_data, '20180704000000'))
    print(is_open(row_data, '20180705000000'))
    print(is_open(row_data, '20180706000000'))
    print(is_open(row_data, '20180707000000'))

def test5_1(row_data=get_row_contents(77)):
    print('in test5_1'.center(40, '*'))
    print(is_open(row_data, '20180702000000'))

def test5_2(row_data=get_row_contents(79)):
    '''
    0703,2轮3天的将=间隔,每轮持续3天

    0703,F
    0703,T
    0704,T
    0705,T

    0706,F
    0707,F
    0708,F

    0709,T
    0710,T

    '''
    print('in test5_2'.center(40, '*'))
    assert is_open(row_data, '20180702000000') == None
    assert is_open(row_data, '20180703000000') == True
    assert is_open(row_data, '20180704000000') == True
    assert is_open(row_data, '20180705000000') == True
    assert is_open(row_data, '20180706000000') == None
    assert is_open(row_data, '20180707000000') == None
    assert is_open(row_data, '20180708000000') == None
    assert is_open(row_data, '20180709000000') == True
    assert is_open(row_data, '20180710000000') == True


def test6_1(row_data=get_row_contents(119)):
    print('in test6_1'.center(40, '*'))
    assert is_open(row_data, '20180702000000') == None
    assert is_open(row_data, '20180703000000') == None
    assert is_open(row_data, '20180704000000') == True
    assert is_open(row_data, '20180704000000') == True
    assert is_open(row_data, '20180704000000') == True
    assert is_open(row_data, '20180705000000') == True
    assert is_open(row_data, '20180706000000') == True
    assert is_open(row_data, '20180707000000') == True
    assert is_open(row_data, '20180709000000') == True
    assert is_open(row_data, '20180710000000') == True
    assert is_open(row_data, '20180711000000') == None
    assert is_open(row_data, '20180712000000') == None



if __name__ == '__main__':
    test1_1()
    test1_2()
    test1_3()

    test2_1()
    test2_2()

    test3_1()
    test3_2()

    test4_1()

    test5_1()
    test5_2()

    test6_1()