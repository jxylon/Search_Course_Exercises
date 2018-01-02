# -*- coding:utf-8 -*-
from termcolor import colored


def ex21():
    """
    为书名建立索引
    """
    with open('book.txt', 'r') as f:
        book = f.readlines()
    with open('stopwords.txt', 'r') as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    word_index = {}
    line_num = 0
    for l in book:
        line_num += 1
        if (line_num == 1):
            continue
        list = l.split('      ')
        list[1] = list[1].rstrip().strip('\n')
        index, l = list[0], list[1]
        l = l.split(' ')
        for i in range(0, len(l)):
            if ((l[i] not in word_index.keys()) and l[i] not in stopwords_list):
                word_index[l[i]] = []
                word_index[l[i]].append(index)
            elif (l[i] not in stopwords_list):
                word_index[l[i]].append(index)
    with open('index.txt', 'w') as f:
        f.writelines('关键词'.ljust(10) + '\t\t\t\t' + '书名索引'.ljust(10) + '\n')
    with open('index.txt', 'a') as f:
        for key, value in word_index.items():
            f.write(key.ljust(10) + '\t\t\t\t')
            for i in value:
                f.write(i.ljust(4))
            f.write('\n')

def writeindex(index_dict):
    with open('index_dict.txt','w') as f:
        for key,value in index_dict.items():
            f.write(key+':')
            for i in value:
                f.write(str(i)+' ')
            f.write('\n')

def ex22(search):
    """
    单文档中字符串的查找
    """
    index,article_list=[],[]
    with open('article.txt', 'r') as f:
        article = f.read()
    for l in article.split('\n'):
        for word in l.split(' '):
            article_list.append(word)
    word_index = {}
    for i in range(len(article_list)):
        if (article_list[i] not in word_index.keys()):
            word_index[article_list[i]] = []
            word_index[article_list[i]].append(i)
        else:
            word_index[article_list[i]].append(i)
    writeindex(word_index)
    if (search in word_index.keys()):
        index = word_index[search]
    else:
        print('未找到该单词')
        return 0
    print(index)
    for i in range(len(article_list)):
        if i in index:
            print(colored(article_list[i], color='red', attrs=['bold']),end=' ')
        else:
            print(article_list[i],end=' ')

if __name__ == '__main__':
    # ex21()
    print('输入你要搜索的字符串:')
    search_word = input()
    ex22(search_word)
