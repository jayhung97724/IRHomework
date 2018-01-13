# -*- coding: utf-8 -*-
import json
import jieba
import jieba.posseg as pseg
jieba.load_userdict('dict.txt.big.txt')
from collections import OrderedDict
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
with open('wiki_data_small.json', 'rb') as json_data:    
    wiki_data = json.load(json_data)

top = 1000
tempDict = OrderedDict()
for key in range(len(wiki_data)):
    #key = '0'
    words = pseg.cut(wiki_data[str(key)])
    for word in words:
        if not tempDict.has_key(word.word):
            tempDict.update({word.word:top})
            top += 1
    print key
print json.dumps(tempDict, encoding='utf-8', ensure_ascii=False)

vec = []
for key in range(len(wiki_data)):
    temp_vec = [0 for j in range(top)]
    words = pseg.cut(wiki_data[str(key)])
    for word in words:
        temp_vec[tempDict[word.word]]+=1
    vec.append(temp_vec)
print vec
