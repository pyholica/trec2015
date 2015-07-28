# coding: utf-8
from datetime import datetime
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import sys

index_name = sys.argv[1]

client = MongoClient('mongodb://202.30.23.40:27017')
es = Elasticsearch([{'host':'localhost', 'port':9200}])

db = client.trec

collection = db.ArticleSmallData3

#data = collection.find_one()
cursor = collection.find()
data = cursor.next()
#obj = next(cursor, None)
#data['pmcid']


while(data):
  #from bson.json_util import dumps
#import json
  title = data['title']
  pmcid = data['pmcid']
  abstract = data['abstrctSectionList']
  abstractdata = ''
  for p in abstract:
    for key, value in p.items():
      abstractdata += (value + "\n")
  body = data['bodySectionList']
  bodydata = ''
  for p in body:
    for key, value in p.items():
      bodydata += (value + "\n")
  #title = json.loads(dumps(data))['articleMeta']['title']
  #section = json.loads(dumps(data))['articleContent']['sectionList']
  #pmcid = json.loads(dumps(data))['articleMeta']['pmcid']

  #print(pmcid)
  #print(body)

  data = {
    'pmcid' : pmcid,
    'title' : title,
    'abstract' : abstractdata,
    'body' : bodydata
  }

  res = es.index(index=index_name, doc_type='article', id=pmcid, body=data)
#print(res['created'])
#res = es.get(index="trec", doc_type='articleSmall', id=pmcid)
#print(res['_source'])
  try:
    data = cursor.next()
  except:
    print("finished")


