
# coding: utf-8

# In[42]:




from datetime import datetime
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import sys

index_name = sys.argv[1]
pmcidListFile = sys.argv[2]
#index_name = "dfr_total"

client = MongoClient('mongodb://210.107.192.201:27017')
es = Elasticsearch([{'host':'localhost', 'port':9200}])

db = client.trec

collection = db.article


# In[48]:


f = open(pmcidListFile, 'r')
pmcidlist = list(f)


# In[49]:

for pmid in pmcidlist:
    pmid = str(pmid).strip()

    try:
        #print(pmid)
        data = collection.find_one({'articleMeta.pmcid':pmid})
    except:
        print(pmid)
        f = open('indexError.txt', 'w')
        f.write(pmid + '\n')
        f.close()

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

    input_D = {
        'pmcid' : pmcid,
        'title' : title,
        'abstract' : abstractdata,
        'body' : bodydata
    }

    #input_D

    res = es.index(index=index_name, doc_type='article', id=pmcid, body=input_D, timeout=3600, request_timeout=3600)




# In[ ]:



