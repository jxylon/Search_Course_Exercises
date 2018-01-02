import os
import re
import math
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

word_list = []  # 单词列表
forward_index = {}  # 单词词典 正排索引项：文档编号，单词，出现次数，出现位置
reverse_index = {}  # 单词词典 倒排索引项：单词，文档编号，出现次数,出现的文档位置


def read_article():
    rootdir = 'D:/搜索引擎/exercise/ex6/article'
    file_list = os.listdir(rootdir)
    # 文件名按数字排序
    file_list = sorted(file_list, key=lambda x: int(re.sub('\D', '', x)))
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    article_list = []
    for i in range(len(file_list)):
        path = os.path.join(rootdir, file_list[i])
        if os.path.isfile(path):
            with open(path, 'r') as f:
                article = f.read()
                article = re.sub(r, ' ', article)
                article_list.append(article.lower())
    return article_list


def read_sentence():
    article_list = ["I'd like an apple, do you like?", "An apple a day keeps the doctor away",
                    "Never compare an apple to an orange", "I prefer scikit-learn, to Orange"]
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    for i in range(len(article_list)):
        article = re.sub(r, ' ', article_list[i])
        article_list.append(article.lower())
    return article_list


def make_reverse_index():
    for i in range(len(forward_index.keys())):
        doc_name = 'doc' + str(i)
        word_list = list(forward_index[doc_name].keys())
        for j in range(len(word_list)):
            word = word_list[j]
            count_times = forward_index[doc_name][word][0]
            count_position = forward_index[doc_name][word][1]
            if word not in reverse_index.keys():
                reverse_index.update({word: {doc_name: [count_times, count_position]}})
            else:
                reverse_index[word].update({doc_name: [count_times, count_position]})


def make_forwardindex(article_list: list):
    r = re.compile(r'[\s\n]')
    for i in range(len(article_list)):
        doc_name = 'doc' + str(i)
        if i not in forward_index.keys():
            forward_index.update({doc_name: {}})
        word = re.split(r, article_list[i])
        for j in range(len(word)):
            if word[j] == '':
                continue
            if word[j] not in forward_index[doc_name].keys():
                forward_index[doc_name].update({word[j]: [1, [j]]})
            else:
                forward_index[doc_name][word[j]][0] += 1
                forward_index[doc_name][word[j]][1].append(j)


def count_tfidf():
    tf_dict = {}
    idf_dict = {}
    doc_list = list(forward_index.keys())
    N = len(doc_list)
    for key in reverse_index.keys():
        tf_dict.update({key: []})
        for j in doc_list:
            if j not in reverse_index[key].keys():
                tf_dict[key].append(0)
            else:
                tf_dict[key].append(reverse_index[key][j][0])
        idf_dict.update({key: math.log(N / len(reverse_index[key].keys()) + 1)})
    for key in tf_dict:
        count_sum = sum(tf_dict[key])
        for j in range(len(tf_dict[key])):
            tf_dict[key][j] = tf_dict[key][j] / count_sum
    tf_df = pd.DataFrame(tf_dict, index=doc_list)
    idf_df = pd.DataFrame(idf_dict, index=[0])
    print(tf_df)


def tfidf(articlelist):
    """
    sklearn实现
    """
    vectoriezd = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectoriezd.fit_transform(articlelist))
    word = vectoriezd.get_feature_names()
    weight = tfidf.toarray()
    tfidfDict = {}
    for i in range(len(weight)):
        for j in range(len(word)):
            getWord = word[j]
            getValue = weight[i][j]
            if getValue != 0:
                if tfidfDict.__contains__(getWord):
                    tfidfDict[getWord] += float(getValue)
                else:
                    tfidfDict.update({getWord: getValue})
    return tfidfDict


def tfidf_dict(article_list: list):
    file_len = len(article_list)
    tf_list = list()
    idf_dic = dict()
    idf_temp = dict()
    for i, doc in enumerate(article_list):
        dic = dict()
        word_list = doc.split(' ')
        doc_len = len(word_list)
        for word in word_list:
            if word not in dic:
                dic[word] = 1
            else:
                dic[word] += 1
            if word not in idf_temp:
                idf_temp[word] = set()
                idf_temp[word].add(i)
        for word in dic:
            dic[word] = dic[word] / doc_len
        tf_list.append(dic)
    for key in idf_temp.keys():
        if key not in idf_dic:
            idf_dic[key] = math.log10(file_len / (len(idf_temp[key]) + 1))
    tfidf_list = []
    for i in range(len(tf_list)):
        dic = dict()
        for word in tf_list[i].keys():
            if word not in dic:
                dic[word] = tf_list[i][word] * idf_dic[word]
        tfidf_list.append(dic)
    with open('result.txt', 'w') as f:
        f.writelines('docname' + '\t\t' + 'word' + '\t\t' + 'tfidf' + '\n')
        for i in range(len(tfidf_list)):
            f.writelines('doc' + str(i + 1) + '\n')
            for word in tfidf_list[i]:
                f.writelines('\t\t\t' + str(word) + '\t\t\t' + str(tfidf_list[i][word]) + '\n')


if __name__ == '__main__':
    # 读取文件
    article_list = read_article()
    # 正排索引
    make_forwardindex(article_list)
    # # 倒排索引
    make_reverse_index()
    # 计算tfidf
    count_tfidf()
    # tfidf_dict(article_list)
    # tfidf(article_list)
