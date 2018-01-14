
# coding: utf-8

# In[3]:

import json
import jieba
import jieba.posseg as pseg
jieba.load_userdict('dict.txt.big.txt')
from collections import OrderedDict
import locale
import pandas as pd
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
from googlesearch.googlesearch import GoogleSearch


# In[4]:

with open('questions_example.json', 'rb') as qf:
    q_list = json.load(qf)


# In[45]:

tempDict = OrderedDict()
q = []
words = pseg.cut(q_list[0]['Question'])
for word in words:
    if 'n' in word.flag and not tempDict.has_key(word.word):
        tempDict.update({word.word:word.flag})
# print json.dumps(tempDict, encoding='utf-8', ensure_ascii=False)
for key in tempDict.keys():
    name = key.encode('utf-8')
    print name
    qstring.join(name)
    q.append(name)
qstring = ' '.join(q)
print qstring


# In[46]:

print qstring


# In[50]:

from googlesearch.googlesearch import GoogleSearch
response = GoogleSearch().search(qstring)

rp = ''
for result in response.results:
    rp += result.title
    print("Title: " + result.title)
print rp


# In[57]:

def findAnswer():
    ansN = 0
    ans = ''
    for op in 'ABC':
        score = rp.count(q_list[0][op])
        if score > ansN:
            ans = op
            ansN = score
    print ans, ansN
    return ans


# In[59]:

findAnswer()


# In[ ]:



