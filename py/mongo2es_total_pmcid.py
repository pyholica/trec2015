
# coding: utf-8


from datetime import datetime
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import sys

index_name = sys.argv[1]

client = MongoClient('mongodb://210.107.192.201:27017')
es = Elasticsearch([{'host':'localhost', 'port':9200}])

db = client.trec

collection = db.article

#data = collection.find_one()
#cursor = collection.find()
#data = cursor.next()
#obj = next(cursor, None)
#data['pmcid']

f = open('pmcidList_copy.csv', 'r')
pmid = f.readline()
data = collection.find_one({'articleMeta.pmcid':pmid})

while(data):
    try:
        body = data['articleContent']
        meta = data['articleMeta']
    except:
        print("no article")

    title = meta['title']
    pmcid = meta['pmcid']
    abstract = meta['abstractText']
    abstractList = abstract['sectionList']
    abstractdata = ''
    for p in abstractList:
        for key, value in p.items():
          abstractdata += (value + "\n")
    bodyList = body['sectionList']
    bodydata = ''
    for p in bodyList:
        for key, value in p.items():
            bodydata += (value + "\n")
      #title = json.loads(dumps(data))['articleMeta']['title']
      #section = json.loads(dumps(data))['articleContent']['sectionList']
      #pmcid = json.loads(dumps(data))['articleMeta']['pmcid']

      #print(pmcid)
      #print(body)

    input_D = {
        'pmcid' : pmcid,
        'title' : title,
        'abstract' : abstractdata,
        'body' : bodydata
    }

    input_D

    res = es.index(index=index_name, doc_type='article', id=pmcid, body=input_D, timeout=3600)
#print(res['created'])
#res = es.get(index="trec", doc_type='articleSmall', id=pmcid)
#print(res['_source'])
    try:
        pmid = f.readline()
        data = collection.find_one({'articleMeta.pmcid':pmid})
    except:
        f = open('indexError.txt', 'w')
        f.write(pmid + '\n')
        f.close()


