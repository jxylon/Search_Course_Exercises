import jieba
import re
from termcolor import colored
from sklearn.feature_extraction.text import CountVectorizer
import ex6.ex6 as ex6

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
            i += len(search)
        else:
            i += step
    return index_list


def len_word(key_word_dict, i):
    for j in key_word_dict.keys():
        if final_words_posi[i] in key_word_dict[j]:
            return len(j)
    return MAXLEN


def make_summary(final_words_posi, key_words_posi, MAXLEN):
    """
    自动生成文章摘要

    """
    # 如果关键词不在文章中，直接返回
    if not final_words_posi:
        return 'Error!Key Words Not In Article.', 0
    score_list = []
    for i in range(len(final_words_posi)):
        t_score = []
        for j in range(i, len(final_words_posi)):
            if final_words_posi[i] + MAXLEN > final_words_posi[j] + len_word(key_words_posi, j):
                t_score.append(final_words_posi[j])
            else:
                break
        weight_t = 0
        for j in t_score:
            for key, value in key_words_posi.items():
                if j in value:
                    weight_t += weight[key]
        score_list.append([weight_t, final_words_posi[i]])
    max_score = score_list[0][0]
    max_position = score_list[0][1]
    for i in score_list:
        if i[0] > max_score:
            max_score = i[0]
            max_position = i[1]
    # 移动摘要中非完整部分
    summary = article[max_position:max_position + MAXLEN]
    return summary, max_position


def highlihgt(summary, input_set):
    i = 0
    while (i < len(summary)):
        flag = 0
        for j in input_set:
            if (summary[i:i + len(j)] == j):
                print(colored(summary[i:i + len(j)], 'red'), end='')
                i += len(j)
                flag = 1
        if (flag == 0):
            print(summary[i], end='')
            i += 1


if __name__ == '__main__':
    # 读取文件，替换标点符号
    with open('article.txt', 'r') as file:
        article = file.read()
    r = '[\s!’"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~，。；《》\n“”]+'
    cut_article = re.sub(r, '', article)
    # 分词得到文章单词元组
    input_search = input()
    input_set = set([x for x in jieba.cut(input_search)])
    words_set = [x for x in jieba.cut(article)]
    # 词频作为权重
    tfidf_dict=ex6.tfidf(words_set)
    weight = {}
    # 词在文章中出现位置
    key_words_posi = {}
    for i in input_set:
        if i in words_set:
            key_words_posi[i] = boyer_Moore(i, article)
        if(i in tfidf_dict.keys()):
            weight[i] = tfidf_dict[i]
        else:
            weight[i] = 0
    # 词在文章中出现位置
    final_words_posi = []
    # 二维列表降为一维
    none = [final_words_posi.extend(i) for i in key_words_posi.values()]
    # 排序
    final_words_posi.sort()
    # 生成自动摘要
    MAXLEN = 50
    summary, max_position = make_summary(final_words_posi, key_words_posi, MAXLEN)
    # 移动摘要中非完整部分
    end_flag = ['。', '！', '；', '.', '!', ';', '\n', ',', '，']
    while (summary[-1] not in end_flag):
        for i in range(MAXLEN - 1, -1, -1):
            if summary[i] in end_flag:
                idx = final_words_posi.index(max_position)
                final_words_posi[idx] = max_position - (MAXLEN - i) - MAXLEN
                final_words_posi.sort()
                break
        summary, max_position = make_summary(final_words_posi, key_words_posi, MAXLEN)
    highlihgt(summary, input_set)
