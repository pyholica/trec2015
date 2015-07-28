
# coding: utf-8

# In[1]:

from datetime import datetime
from elasticsearch import Elasticsearch


# In[7]:

from pymongo import MongoClient
client = MongoClient('mongodb://210.107.192.201:27017')
es = Elasticsearch([{'host':'210.107.192.201', 'port':9200}])


# In[8]:

db = client.trec


# In[9]:

collection = db.ArticleSmallData3


# In[10]:

#data = collection.find_one()
cursor = collection.find()
data = cursor.next()
#obj = next(cursor, None)
#data['pmcid']


# In[11]:

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

  res = es.index(index="dfr_2014_sample", doc_type='article', id=pmcid, body=data, request_timeout = 10000000)  
#print(res['created'])
#res = es.get(index="trec", doc_type='articleSmall', id=pmcid)
#print(res['_source'])
  data = cursor.next()
print("finished")


# In[1]:

print("finish")


# In[ ]:



