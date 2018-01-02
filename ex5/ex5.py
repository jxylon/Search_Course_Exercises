import jieba
import datetime

def newlist(l):
    c = ['', '\n', '，', '?', '。', ':', '“', '‘', '！', '；', ' ', '\t']
    new = []
    for i in l:
        if i not in c and i not in new:
            new.append(i)
    return new


def cut(article):
    seg_list = jieba.cut(article, cut_all=True)
    # print('/'.join(seg_list))
    word_list = newlist([x for x in [x for x in seg_list]])
    for i in word_list:
        print(i, end='/')
    return word_list


def create_dict(article: str, maxlen):
    dict = []
    for i in range(len(article) - maxlen):
        for j in range(i + 1, i + maxlen):
            if (article[i:j] not in dict):
                dict.append(article[i:j])
    with open('dict.txt', 'w') as f:
        for i in dict:
            f.write(i + '\n')


def max_match(article, dict_list, maxlen):
    word_list = []
    idx, i = 0, 0
    while (idx < len(article)):
        for i in range(maxlen, 0, -1):
            word = article[idx:idx + i]
            if (i == 1):
                word_list.append(word)
            if word in dict_list:
                word_list.append(word)
                break
        idx += i
    return word_list


def tfidf(list1, list2):
    # list1待比较的，list2准确的
    len1 = len(list1)
    len2 = len(list2)
    print('\n最大匹配算法分词数:%d' % len(list1))
    print('jieba分词数%d:' % len(list2))
    same = len(set(list1).intersection(set(list2)))
    print('相同的词数%d:' % same)
    acc = same / len1
    pre = same / len2
    print('准确率:%.2f' % acc, '召回率:%.2f' % pre)


if __name__ == '__main__':
    maxlen = 4
    with open('article2.txt', 'r') as f:
        article = f.read()
    print('jieba分词')
    start=datetime.datetime.now()
    word_jieba = cut(article)
    end=datetime.datetime.now()
    print('\njieba分词时间:',(end-start).seconds,'s')
    # create_dict(article, maxlen)
    print('\n正向最大匹配分词')
    start = datetime.datetime.now()
    with open('dict.txt', 'r') as f:
        dict = f.read()
    dict_list = dict.split('\n')
    dict_list = [x.split(' ')[0] for x in dict_list]
    words_my = max_match(article, dict_list, maxlen)
    words_my = newlist(words_my)
    for i in words_my:
        print(i, end='/')
    end = datetime.datetime.now()
    print('\n正向最大匹配分词',(end - start).seconds,'s')
    # with open('max_match.txt', 'w') as f:
    #     for i in words:
    #         f.write(i + '\n')
    tfidf(words_my, word_jieba)
