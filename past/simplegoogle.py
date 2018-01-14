
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
from googlesearch.googlesearch import GoogleSearch
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
        # print name
        q.append(name)
    qstring = ' '.join(q[0:10])
    qstring = qstring[0:31]
    # qstring += ' wiki'
    print qstring
    return qstring


# In[28]:

def cutQuestion1(no):
    qstring = q_list[no]['Question'][0:30].encode('utf-8')
    # qstring += ' wiki'
    print qstring
    return qstring


# In[29]:

a = cutQuestion1(14)
print a


# In[6]:

def Google(qstring):
    response = GoogleSearch().search(qstring)
    rp = ''
    for i in range(6):
        rp += response.results[i].title
    return rp


# In[30]:

def findAnswer(no):
    ansN = 0
    ans = ''
    qstring = cutQuestion1(no)
    print "%d Googling... " % no
    result = Google(qstring)
    print "Google over " 
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
    # print ans, ansN
    return ans


# In[31]:
findAnswer(3)


# In[32]:

def ultimate():
    ans_list = []
    for no in range(len(q_list)):
        ans = findAnswer(no)
        print no, ans
        ans_list.append(ans)
        time.sleep(0.3)
    print ans_list
    return ans_list


# In[33]:

if __name__== "__main__":
    tStart = time.time()
    ultimate()
    tEnd = time.time()
    period = tEnd - tStart
    print "It cost %f sec" % period

# t = timeit('ultimate()', 'from __main__ import ultimate', number=1)
# print t
# findAnswer(0)
# findAnswer(1)
# findAnswer(2)
# findAnswer(3)
# findAnswer(4)
# findAnswer(5)
# findAnswer(6)
# findAnswer(7)
# findAnswer(8)
# findAnswer(9)
# findAnswer(10)
# findAnswer(11)
# findAnswer(12)
# findAnswer(13)
# findAnswer(14)
# findAnswer(15)
# findAnswer(16)
# findAnswer(17)
# findAnswer(18)
# findAnswer(19)