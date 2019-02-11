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
line = 'booooooooobby123'
regex_str = ".*?(b.*?b).*"
match_obj = re.match(regex_str, line)
if match_obj:
    # booooooooob
    print(match_obj.group(1))

