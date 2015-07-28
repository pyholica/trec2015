
# coding: utf-8

# In[2]:

from datetime import datetime
from elasticsearch import Elasticsearch


# In[3]:

from pymongo import MongoClient
client = MongoClient('mongodb://202.30.23.40:27017')
es = Elasticsearch([{'host':'localhost', 'port':9200}])


# In[4]:

db = client.trec


# In[5]:

collection = db.article


# In[6]:

cursor = collection.find()
data = cursor.next()


# In[6]:

target = open('pmcidList.csv', 'w')
count = 0
while(data):
    try:
        pmcid = data['articleMeta']['pmcid']
        target.write(pmcid + '\n')
        data = cursor.next()
        count += 1
    except:
        print("finish {0}".format(count))
        target.close()
print("finished List")

