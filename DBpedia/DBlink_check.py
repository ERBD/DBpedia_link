#!/usr/bin/env python
# coding: utf-8
import nltk
import requests
from nltk.tokenize import word_tokenize, sent_tokenize
#from SPARQLWrapper import SPARQLWrapper, JSON
from nltk.corpus import stopwords

url = 'http://model.dbpedia-spotlight.org/en/annotate'

f1 = open("dbcheck.txt").read().splitlines()
f= open("filtered_out.txt","w+")
dict1 = {}

def entityList(text, confidence = '0.6'):
    #print(text)
    data_req = {}
    headers = {}
    data_req['text'] = text
    data_req['confidence'] = confidence
    data_req['support'] = 20
    headers['Accept'] = 'application/json'
    response = requests.post(url, data=data_req, headers=headers)
    ent_List = {}
    try:
        if 'Resources' in response.json(): 
            for res in response.json()['Resources']:
                ent_List[res['@surfaceForm']] = res['@URI']
    except ValueError:
        f.write("oops!\n")
    #print(ent_List)
    return ent_List


for j in range(len(f1)):
    
    str1 = f1[j]
    temp = str1.split(";")
    #temp = [x.strip(' ') for x in temp]
    if temp[4]!=" ":
        dict1[j] = temp
        print(len(temp),"==>", j)
    
        ###FOR subject part
        sub = dict1[j][2].strip()
        sub_link = entityList(sub)
        if len(sub_link)>0:
            s_count = len(sub_link)
        else:
            s_count = 0

    
        dict1[j].append(s_count)
        dict1[j].append(sub_link)


        ###For object part
        obj = dict1[j][4].strip()
        obj_link = entityList(obj)
        o_count = len(obj_link)

        dict1[j].append(o_count)
        dict1[j].append(obj_link)


for i in range(len(dict1)):
    try:
        if dict1[i][-2] != 0 or dict1[i][-4]!=0:
             f.write("%d  %s\n" % (i, dict1[i]))
             # f.write("%d  %d okay\n" % (i, i))
    
    except KeyError:
        f.write("oops1!\n")
f.close() 
#f1.close()
#for i in range(len(dict1)):
 #   print(i,"  okay")


# In[ ]:




