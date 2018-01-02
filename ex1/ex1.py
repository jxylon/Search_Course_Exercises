# encoding='utf-8'
from termcolor import colored
import datetime


def brute_force(search, str):
    """
    暴力匹配字符串

    """
    i, count = 0, 0
    index_list = []
    while (i <= (len(str) - len(search))):
        j = 0
        while (j != len(search)):
            if (search[j] == str[i + j]):
                j += 1
            else:
                break
        if (j == len(search)):
            count += 1
            index_list.append(i)
            print(colored(str[i:i + j], color='red'), end='')
            i += len(search) - 1
        else:
            print(str[i], end='')
        i += 1
    # 输出剩余的部分
    if (i >= (len(str) - len(search))):
        print(str[i:])
    if count != 0:
        print('\n%s 出现次数: %d' % (search, count))
        print('下标分别为:', index_list)
    else:
        print('\n%s 没有出现在文本中' % search)


# 坏字符跳转
def bad_move(bad_word, search, bad_i):
    # 如果"坏字符"不包含在搜索词之中，则上一次出现位置为 -1。
    if (bad_word not in search):
        index = -1
    else:
        # 搜索词中的上一次出现位置
        index = search.find(bad_word)
    # 后移位数 = 坏字符的位置 - 搜索词中的上一次出现位置
    return bad_i - index


# 好后缀跳转
def good_move(search, bad_i):
    good_suffix = search[bad_i + 1:]
    # 好后缀在搜索字符串中只出现了一次
    good_step = -1
    for i in range(len(good_suffix), 0, -1):
        # 搜索字符串的前i个字符和好后缀的后 len(good_suffix)-i 个字符相同，则找到
        if (search[0:i] == good_suffix[len(good_suffix) - i:]):
            good_step = i - 1
    # 后移位数 = 好后缀的位置 - 搜索词中的上一次出现位置
    return len(search) - good_step - 1


# 跳转函数
def step_func(search, str):
    index_i = 0
    for i in range(len(search) - 1, -1, -1):
        if (search[i] != str[i]):
            index_i = i
            break
    bad_step = bad_move(str[index_i], search, index_i)
    if (index_i != (len(search) - 1)):
        good_step = good_move(search, index_i)
    else:
        good_step = 0
    # 每次后移这两个规则之中的较大值。
    return max(bad_step, good_step)


def boyer_Moore(search, str):
    i, count, step = 0, 0, 1
    index_list = []
    while (i <= (len(str) - len(search))):
        j = len(search)
        for j in range(len(search) - 1, -1, -1):
            if (search[j] == str[i + j]):
                continue
            else:
                step = step_func(search, str[i:i + len(search) + 1])
                # j=1 防止 search和str比较到最后一个字符串，但是没有匹配成功
                j = 1
                break
        if (j == 0):
            count += 1
            index_list.append(i)
            print(colored(str[i:i + len(search)], color='red'), end='')
            i += len(search)
        else:
            print(str[i:i + step], end='')
            i += step
    # 输出剩余的部分
    if (i >= (len(str) - len(search))):
        print(str[i:])
    if count != 0:
        print('\n%s 出现次数: %d' % (search, count))
        print('下标分别为:', index_list)
    else:
        print('\n%s 没有出现在文本中' % search)


def split_way(search_word, article):
    article_row = article.split('\n')
    index_list = []
    count, i = 0, 0
    for row in article_row:
        #print('    ', end='')
        article_list = row.split(' ')
        for word in article_list:
            i += 1
            if word == search_word:
                index_list.append(i)
                count += 1
                print(colored(word, 'red'), end=' ')
            else:
                print(word, end=' ')
        print(end='')
    if count != 0:
        print('\n%s 出现次数: %d' % (search_word, count))
        print('下标分别为:', index_list)
    else:
        print('\n%s 没有出现在文本中' % search_word)


def match_num(str):
    prefix, posfix = [], []
    for i in range(1, len(str)):
        prefix.append(str[0:i])
        posfix.append(str[i:len(str)])
    list = [l for l in prefix if l in posfix]
    if (len(list) == 0):
        return 0
    else:
        list_first = list[0]
        return len(list_first)


def match_table(search):
    list = []
    for i in range(1, len(search) + 1):
        str = search[0:i]
        list.append(match_num(str))
    return list


def kmp(search, str):
    i, count, step = 0, 0, 1
    index_list = []
    # 部分匹配表
    match_list = match_table(search)
    while (i <= (len(str) - len(search))):
        j = 0
        while (j < len(search)):
            if (search[j] == str[i + j]):
                j += 1
                continue
            elif (j == 0):
                step = 1
                break
            else:
                step = j - match_list[j - 1]
                break
        if (j == len(search)):
            count += 1
            index_list.append(i)
            print(colored(str[i:i + len(search)], color='red',attrs=['bold']), end='')
            i += len(search)
        else:
            print(str[i:i + step], end='')
            i += step
    # 输出剩余的部分
    if (i >= (len(str) - len(search))):
        print(str[i:])
    if count != 0:
        print('\n%s 出现次数: %d' % (search, count))
        print('下标分别为:', index_list)
    else:
        print('\n%s 没有出现在文本中' % search)


if __name__ == '__main__':
    with open('article.txt', 'r') as f:
        article = f.read()
    print('输入你要搜索的字符串:')
    search_word = input()
    print('暴力匹配')
    starttime = datetime.datetime.now()
    brute_force(search_word, article)
    endtime = datetime.datetime.now()
    print('time=%.3lf ms\n' % (((endtime - starttime).microseconds) / 1e3))

    print('KMP算法')
    starttime = datetime.datetime.now()
    kmp(search_word, article)
    endtime = datetime.datetime.now()
    print('time=%.3lf ms\n' % (((endtime - starttime).microseconds)/1e3))

    print('BM算法')
    starttime = datetime.datetime.now()
    boyer_Moore(search_word, article)
    endtime = datetime.datetime.now()
    print('time=%.3lf ms\n' % (((endtime - starttime).microseconds) / 1e3))

    print('分单词方法')
    starttime = datetime.datetime.now()
    split_way(search_word, article)
    endtime = datetime.datetime.now()
    print('time=%.3lf ms\n' % (((endtime - starttime).microseconds) / 1e3))
