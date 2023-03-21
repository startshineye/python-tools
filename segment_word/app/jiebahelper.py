# !usr/bin/python
# -*- coding: utf-8 -*-
# jiebahelper 结巴分词封装模块
import jieba
import jieba.analyse
import jieba.posseg
import re
import datetime

# 加载自定义词典
# jieba.load_userdict('userdict.txt')
# 至少包含一个汉字的正则表达式
contains_hanzi_pattern = re.compile(r'.*[\u4e00-\u9fa5]+.*')


# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


stopwords = stopwordslist('hit_stopwords.txt')  # 这里加载停用词的路径
emptyList = ["\t", "\r\n", "\r", "\n"]


# 对句子进行分词
def dosegment(sentence, must_contains_hanzi=False):
    '''
    分词
    :param sentence:输入字符
    :param must_contains_hanzi:是否必须包含汉字，默认False,即全部切词。Ture,即不返回词中没有汉字的词语
    :return:
    '''
    start = datetime.datetime.now()
    sentence_seged = jieba.cut(sentence.strip())
    step1 = datetime.datetime.now()
    # outstr = ''
    # for word in sentence_seged:
    #     if word not in stopwords and word not in emptyList:
    #         # 带数字或者只返回不是数字的字符
    #         if not must_contains_hanzi or contains_hanzi_pattern.match(word):
    #             outstr += word+" "
    outstr = " ".join(list(filter(lambda x: (x not in stopwords and x not in emptyList and (
                not must_contains_hanzi or contains_hanzi_pattern.match(x))), sentence_seged)))
    # outstr=" ".join(sentence_seged)
    step2 = datetime.datetime.now()

    print("cut:{}us微秒 filter:{}us".format((step1 - start).microseconds, (step2 - step1).microseconds))
    return outstr


# 带词性标注，对句子进行分词
def dosegment_with_pos(sentence, must_contains_hanzi=False):
    '''
    分词
    :param sentence:输入字符
    :param must_contains_hanzi:是否必须包含汉字，默认False,即全部切词。Ture,即不返回词中没有汉字的词语
    :return:
    '''
    start = datetime.datetime.now()
    sentence_seged = jieba.posseg.cut(sentence.strip())
    step1 = datetime.datetime.now()
    outstr = ''
    for x in sentence_seged:
        # 是否必须包含汉字
        if x.word not in stopwords and x.word not in emptyList and (not must_contains_hanzi or
                                                                    contains_hanzi_pattern.match(x.word)):
            outstr += "{}/{},".format(x.word, x.flag)

    step2 = datetime.datetime.now()

    print("poscut:{}us微秒 filter:{}us".format((step1 - start).microseconds, (step2 - step1).microseconds))
    return outstr


def dosegment_all(sentence):
    '''
    带词性标注，对句子进行分词，不排除停词等
    :param sentence:输入字符
    :return:
    '''
    sentence_seged = jieba.posseg.cut(sentence.strip())
    outstr = ''
    for x in sentence_seged:
        outstr += "{}/{},".format(x.word, x.flag)
    return outstr


# 提取关键词
def extract_tags(content, topk):
    content = content.strip()
    tags = jieba.analyse.extract_tags(content, topK=topk)
    return ','.join(tags)