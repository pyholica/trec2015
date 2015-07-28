
# coding: utf-8

# In[2]:




# In[42]:




from datetime import datetime
from elasticsearch import Elasticsearch
from pymongo import MongoClient
import sys




client = MongoClient('mongodb://210.107.192.201:27017')
es = Elasticsearch([{'host':'210.107.192.201', 'port':9200}])
es_local = Elasticsearch([{'host':'localhost', 'port':9200}])

db = client.trec

collection = db.article


# In[48]:
def indexing(index_name, pmcidListFile):

    f = open(pmcidListFile, 'r')
    pmcidlist = list(f)


    # In[49]:

    for pmid in pmcidlist:
        pmid = str(pmid).strip()

        #res = es.search(index="dfr_ngram_total_new",doc_type="article", q=pmid, id=pmid, size=1, request_timeout=1000000)
        res = es.get(index='dfr_ngram_total_new', doc_type='article', id=pmid)
        #result = res['hits']['hits']['_source']
        result = res['_source']
        input_D = {
            'pmcid' : result['pmcid'],
            'title' : result['title'],
            'abstract' : result['abstract'],
            'body' :  result['body']
        }

        #input_D

        res = es_local.index(index=index_name, doc_type='article', id=pmid, body=input_D, timeout=3600, request_timeout=100000)

for topicNum in range(1, 31):
    index_name = 'dfr_ngram_2015_topic{0}'.format(topicNum)
    pmcidListFile = '2015_mix_topic_final/topic{0}.csv'.format(topicNum)
    indexing(index_name, pmcidListFile)

    #index_name = "dfr_total"

    # In[ ]:




