import re

# line = 'booooooooobby123'
# regex_str = "^b.*3$"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     print("yes")

# 正则表达式是反向匹配的, default = greedy, 因为右边的b多，所以从右边开始匹配
# line = 'booooooooobby123'
# regex_str = ".*(b.*b).*"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # bb
#     print(match_obj.group(1))

# 非贪婪
# line = 'booooooooobby123'
# regex_str = ".*?(b.*b).*"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # booooooooobb
#     print(match_obj.group(1))

# 非贪婪
# line = 'booooooooobby123'
# regex_str = ".*?(b.*?b).*"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # booooooooob
#     print(match_obj.group(1))

# +
# line = 'booooooooobbby123'
# regex_str = ".*(b.+b).*"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # bbb
#     print(match_obj.group(1))

# {2,}
# line = 'booooooooobaaaooobbbaaby123'
# regex_str = ".*(b.{3,}b).*"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # bbaab
#     print(match_obj.group(1))

# | 或
# line = 'bobby123'
# regex_str = "((bobby|boobby)123)"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # 只提取有括号的
#     # bobby123
#     print(match_obj.group(1))

# [] 任意一个
# line = 'bobby123'
# regex_str = "([abcd]obby123)"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # 只提取有括号的
#     # bobby123
#     print(match_obj.group(1))

# [0-9] 区间
# line = '18782902222'
# regex_str = "(1[48357][0-9]{9})"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # 只提取有括号的
#     # bobby123
#     print(match_obj.group(1))

# [^1] 不等于1

# /s 空格
# /S 表示只要不为空格都可以
# line = "你 好"
# regex_str = "(你\s好)"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # 只提取有括号的
#     # 你 好
#     print(match_obj.group(1))

# /w = [A-Za-z0-9_]
# /W与/w相反
# line = "你S好"
# regex_str = "(你[A-Za-z0-9_]好)"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # 只提取有括号的
#     # 你S好
#     print(match_obj.group(1))

# line = "你S好"
# regex_str = "(你\w好)"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # 只提取有括号的
#     # 你S好
#     print(match_obj.group(1))


#[\u4E00-\u9FA5] 含义是汉字
# ? 取消贪婪
# line = "study in 南京大学"
# regex_str = ".*?([\u4E00-\u9FA5]+大学)"
# match_obj = re.match(regex_str, line)
# if match_obj:
#     # 只提取有括号的
#     # 你S好
#     print(match_obj.group(1))


# \d 代表数字
line = "xxx出生与2001年6月1日"
line = "xxx出生与2001/6/1"
line = "xxx出生与2001-6-1"
line = "xxx出生与2001-06-01"
line = "xxx出生与2001-06"
regex_str = ".*出生与(\d{4}[年/-]\d{1,2}([月/-]\d{1,2}|[月/-]$|$))"
match_obj = re.match(regex_str, line)
if match_obj:
    # 只提取有括号的
    # 你S好
    print(match_obj.group(1))



