# encoding='utf-8'
from termcolor import colored
import os


def read_article():
    """
    读取文件

    """
    with open('article1.txt', 'r') as f:
        article1 = f.read()
    with open('article2.txt', 'r') as f:
        article2 = f.read()
    return article1, article2


def split_artilce(article: str, k: int):
    """
    切分文章得到shingle

    """
    article_list = []
    for i in range(len(article) - k + 1):
            article_list.append(article[i:i + k])
    return article_list


def highlight(article, intersection, k: int):
    """
    高亮显示

    """
    printed = []
    for i in range(len(article) - k + 1):
        if (article[i:i + k] in intersection):
            flag = 1
        else:
            flag = 0
        for j in range(i, i + k):
            if (j not in printed and flag == 0):
                print(article[j], end='')
                printed.append(j)
            elif (j not in printed and flag == 1):
                print(colored(article[j], color='red'), end='')
                printed.append(j)
    print()


def shingle(article1, article2, n, k):
    """
    实现shingle算法

    """
    article1_list = split_artilce(article1, k)
    article2_list = split_artilce(article2, k)
    intersection = list(set(article1_list).intersection(set(article2_list)))
    union = list(set(article1_list).union(set(article2_list)))
    jaccard = len(intersection) / len(union)
    # 步骤2 两个文本高亮显示
    if n == 2:
        print('article1: ')
        highlight(article1, intersection, k)
        print('article2: ')
        highlight(article2, intersection, k)
    # 步骤1 输出jaccard系数
    print("jaccard = %.2f " % jaccard)
    return jaccard


def dir_compare(k: int):
    with open('article1.txt', 'r') as f:
        article = f.read()
    path = u'D:\搜索引擎\exercise\ex4'
    for dirpath, dirname, filename in os.walk(path):
        for file in filename:
            if(file[-3:] == 'txt'):
                with open(dirpath+'\\'+file) as f:
                    print(dirpath+'\\'+file, end=' : ')
                    article_cmp=f.read()
                    shingle(article,article_cmp,1,k)

if __name__ == '__main__':
    print('输入k值')
    k = input()
    print('步骤1 比较两个字符串')
    print('输入两个字符串')
    print('str1:', end=' ')
    str1 = input()
    print('str2:', end=' ')
    str2 = input()
    shingle(str1, str2, 1, int(k))
    print('步骤2 比较两个文本')
    article1, article2 = read_article()
    shingle(article1, article2, 2, int(k))
    print('步骤3 比较给定文本和文件夹中文件的相似度')
    dir_compare(int(k))
