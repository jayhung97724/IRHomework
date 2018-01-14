
# coding: utf-8

# In[1]:

import json
import jieba
import jieba.posseg as pseg
jieba.load_userdict('dict.txt.big.txt')
from collections import OrderedDict
import locale
import pandas as pd
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
from googlesearch.newgooglesearch import GoogleSearch
from timeit import timeit
import time
from hanziconv.hanziconv import HanziConv


# In[2]:

with open('questions_example.json', 'rb') as qf:
    q_list = json.load(qf)


# In[3]:

def cutQuestion(no):
    tempDict = OrderedDict()
    q = []
    words = pseg.cut(q_list[no]['Question'])
    for word in words:
        if 'n' in word.flag and not tempDict.has_key(word.word):
            tempDict.update({word.word:word.flag})
    # print json.dumps(tempDict, encoding='utf-8', ensure_ascii=False)
    for key in tempDict.keys():
        name = key.encode('utf-8')
        q.append(name)
    qstring = ' '.join(q[0:10])
    qstring = qstring[0:31]
    # qstring += ' wiki'
    print qstring
    return qstring


# In[4]:

def cutQuestion1(no):
    qstring = ''
    qstring += q_list[no]['Question'][0:30].encode('utf-8')
    qstring += ' wiki'
    print qstring
    return qstring


# In[5]:

def Google(qstring):
    response = GoogleSearch().search(qstring, num_results = 7)
    rp = ''
    for i in range(5):
        rp += response.results[i].title
    return rp


# In[6]:

def findAnswer(no):
    ansN = 0
    ans = ''
    qstring = cutQuestion1(no)
    tStart = time.time()
    result = Google(qstring)
    tEnd = time.time()
    period = tEnd - tStart
    print "Google over It cost %f sec" % period
    for op in "ABC":
        score = result.count(q_list[no][op])
        if score > ansN:
            ans = op
            ansN = score
    if ansN == 0:
        for op in "ABC":
            score = result.count(HanziConv.toSimplified(q_list[no][op]))
            if score > ansN:
                ans = op
                ansN = score
        else:
            ans = 'B'
    print ans, q_list[no][ans]
    return ans


# In[7]:

def ultimate():
    ans_list = []
    for no in range(len(q_list)):
        print '%d ============' % no
        ans = findAnswer(no)
        ans_list.append(ans)
        print ans_list
    return ans_list


# In[8]:

if __name__== "__main__":
    tStart = time.time()
    ultimate()
    tEnd = time.time()
    period = tEnd - tStart
    print "It cost %f sec" % period

