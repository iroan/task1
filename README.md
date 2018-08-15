# 任务
## 输入
活动编号,可能的参数,开放类型为:
1. 开服
1. 建角时间
1. 固定轮换

## 处理
实现读取一个xls文件,分析调用参数,返回是否已经开服(开启服务)
## 输出
是否已经开服
## 提交形式
http接口

# 实现
1. 实现函数功能
1. 开启http服务,提供访问接口

# 问题分析
1. 处理的字段信息:`['活动编号', '系统编号', '名字', '顺序', '开启时间', '关闭时间', '开放类型', '持续时间', '活动图标', '开服多少天后开启', '开服多少天后开启', '轮数', '间隔']
`,`['id', 'systemid', 'name', 'seq', 'begin', 'end', 'open_type', 'continued_time', 'icon', 'days_later', 'days_later2', 'int', 'int']
`
1. 只处理`新服`sheet分内容
1. 根据输入参数`id`获取改行的数据
1. 处理该行数据,需要处理的内容
    1. 判断`开放类型`,(7种类型中对号入座)
    1. 如果是`1,开服`,判断输入参数是否在`开启时间`,`关闭时间`之间
    1. 如果是`2,固定开服`,判断输入参数是否在`开启时间`,`关闭时间`之间