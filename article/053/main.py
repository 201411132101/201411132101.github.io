# 参考文献排序建议, 可能有 bug
import re
import os


# 从包含名字的特殊字符串中提取名字
# 输入 str, 返回 str
def extract_name(my_str):
    # 先匹配多个作者的情况 (有and)
    my_match = re.match(r'.+ and [A-Za-z]{1,2}\. .+?,', my_str)
    # 再匹配1个作者的情况 (无and)
    if my_match is None:
        my_match = re.match(r'.+?,', my_str)
        # print('yes')

    name = re.sub(r'[A-Za-z\-]{1,2}\.|,|and', '', my_match.group())
    new_name = name.replace('  ', ' ')
    while len(new_name) != len(name):
        name = new_name
        new_name = name.replace('  ', ' ')

    # print(name)
    return name


# 处理参考文献
with open('reference.txt', 'r', encoding='utf-8') as file_reference:
    # 读取文件
    s = file_reference.read()

    # 处理特殊符号
    list_del = ['\n', '¨', '’', '˘', 'ˇ', '´']
    for part_list_del in list_del:
        s = s.replace(part_list_del, '')

    s = s.replace('ı', 'i')
    # print(s)

    # 分割参考文献
    # 按 id 分割字符串, 只匹配括号内长度小于等于 8 的
    list_id = re.findall(r'\[[0-9a-zA-Z]{1,8}]', s)
    list_text = re.split(r'\[[0-9a-zA-Z]{1,8}]', s)
    del list_text[0]
    # print(list_id)
    # print(list_text)

    # 处理包含名字的字符串
    list_short = [0] * len(list_text)
    for i in range(len(list_text)):
        list_short[i] = extract_name(list_text[i])

    # 组合后再排序
    list_sorted = sorted(zip(list_id, list_text, list_short), key=lambda x: x[2])
    # print(list_sorted)

# 输出排序信息
with open('sorted.txt', 'w', encoding='utf-8') as file_sorted:
    for this_tuple in list_sorted:
        file_sorted.write(this_tuple[0])
        file_sorted.write(this_tuple[1] + '\n')

# 输出错误
with open('wrong.txt', 'w', encoding='utf-8') as file_wrong:
    count_wrong = 0
    if list_sorted[0][0] != list_id[0]:
        file_wrong.write(list_sorted[0][0] + "应该在首位\n")
        count_wrong += 1
    if list_sorted[-1][0] != list_id[-1]:
        file_wrong.write(list_sorted[-1][0] + '应该在末尾\n')
        count_wrong += 1

    for i in range(1, len(list_sorted) - 1):
        if list_sorted[i][0] != list_id[i]:
            file_wrong.write(list_sorted[i][0])
            file_wrong.write('应该在' + list_sorted[i - 1][0] + '和' + list_sorted[i + 1][0] + '之间\n')
            count_wrong += 1

    print(count_wrong, 'wrong')

# 输出警告
with open('warning.txt', 'w', encoding='utf-8') as file_warning:
    count_warning = 0

    index = 0
    while index < len(list_sorted) - 1:
        if list_sorted[index][2] == list_sorted[index + 1][2]:
            index_right = index + 2
            while index_right < len(list_sorted) and list_sorted[index][2] == list_sorted[index_right][2]:
                index_right += 1

            # 输出结果
            for i in range(index, index_right):
                file_warning.write(list_sorted[i][0] + ' ')
            file_warning.write('的作者有相同的姓氏, 排序可能有误\n')

            index = index_right
            count_warning += 1
        else:
            index += 1

    print(count_warning, 'warning')

# os.system("pause")
