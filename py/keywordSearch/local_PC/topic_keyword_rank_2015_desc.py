
# coding: utf-8

# In[6]:

from elasticsearch import Elasticsearch
import os, re
es = Elasticsearch([{'host':'210.107.192.201', 'port':9200}])


# In[ ]:

file = open('2015_description_topic.csv', 'rb')
newpath = './2015_desc_topic_keyword/'
if not os.path.exists(newpath): os.makedirs(newpath)
    
topics = file.readlines()
cnt = 1
for topic in topics:
    topic = topic.lower()
    
    topic = re.sub('[^a-zA-Z0-9-_*.]', ' ', topic)
    print("{} : ".format(cnt) + topic)
    
    
    res = es.search(index="dfr_ngram_total_new",doc_type="article", q=topic
                    #,size=100
                    ,request_timeout=1000000
                    #,search_type="count"
                    ,fields=['pmcid'])
    #print(res['hits']['hits'])
    total = res['hits']['total']
    size = total/10
    res = es.search(index="dfr_ngram_total_new",doc_type="article", q=topic
                    ,size=size
                    ,request_timeout=1000000
                    #,search_type="count"
                    ,fields=['pmcid'])
    print "total : {0}".format(total)
    print "size : {0}".format(size)
    results = res['hits']['hits']
    target = open(newpath+'topic{0}.csv'.format(cnt), 'w')
    for result in results:
        pmcid = str(result['fields']['pmcid'][0])

        
        print(pmcid)
        target.write(pmcid + '\n')
    cnt += 1    
    target.close()

