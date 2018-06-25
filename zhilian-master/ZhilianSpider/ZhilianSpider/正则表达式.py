# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import re
line = 'booooobbbbboobbby123'
regex_str ="^b.*"
# 字符串必须以b开头   .表示可以使任意字符， * 表示可以重复任意多次
regex_str1 ="^b.*3$"
# 3$  字符串必须以  3  结尾

regex_str2 =".*(b.*b).*"
# 正则表达式的贪婪匹配，从后后面开始匹配 结果为bb
regex_str3 =".*?(b.*?b).*"
# 加?会强制进行顺序匹配

regex_str4 =".*(b.+b).*"
# + 前面的字符最少出现一次

regex_str5 =".*(b.{2}b).*"
# {2} 前面的字符最少出现2次

regex_str6 =".*(b.{2,4}b).*"
# {2,5}要求中间的字符出现最少两次，最多四次

regex_str7 ="([abcd]ooooobbbbboobbby123)"
# [abcd] 要求必须是中括号里面元素的任意一个

regex_str8 ="(1[48357][0-9]{9})"
# [48357]  中间必须是这么多元素中任意一个，[0-9]{9}  0-9 任意元素出现9次

regex_str9 ="(1[48357][^1]{9})"
# [^1]{9} 字符不等于1 ，出现9次都可以


line2 = "你好"
regex_str10 = "(你\S好)"
# \s 代表中间有一个空格  \S 只要不为空格都可以

regex_str11 = "(你\w好)"
# [A-Z] [a-z] [0-9] 还有下划线  \w表示在这里面任意元素都符合
# \W 表示出\w的任何都可以

line3 = "study in 南京大学"

regex_str12 = "([\u4E00-\u9FA5]+)"
# [\u4E00-\u9FA5] 表示一个汉字


regex_str13 = ".*?([\u4E00-\u9FA5]+大学)"
# 不加问号，按照原来的贪婪匹配会只截取三个字


line4 = "XXX出生于2001年6月1日"
line4 = "XXX出生于2001/6/1"
line4 = "XXX出生于2001-6-1"
line4 = "XXX出生于2001-06-01"
line4 = "XXX出生于2001-6"
regex_str14 = ".*出生于(\d{4}[年/-]\d{1,2}([月/-]\d{1,2}|[月/-]$|$))"
# \d+表示出现任意数字，包括大小


a =  re.match(regex_str14,line4)
if a:
    print(a.group(1))
    # group 会从re.match函数中提取括号里面的内容