
# coding: utf-8

# In[1]:

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host':'210.107.192.201', 'port':9200}])


# In[3]:

import csv
import os
folder_name = "pmclist_topic1"
index_name = "dfr_total"
#analyzer_name = "edge_ngram_analyzer"
topicNum = ""

newpath = './{0}/'.format(folder_name)
if not os.path.exists(newpath): os.makedirs(newpath)
target = open("{0}topic{1}.csv".format(newpath, topicNum), 'w')
#res = es.search(index=index_name2,doc_type="article", q=query, size=40000)
res = es.search(index=index_name,doc_type="article", size=50000)
for doc in res['hits']['hits']:
    count += 1
    text = '{0}, {1}, {2}'.format(count,doc['_source']['pmcid'],doc['_score'] )
    print (text)
    target.write(text + '\n')
target.close()


# In[ ]:



