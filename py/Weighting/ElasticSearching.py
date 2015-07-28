from elasticsearch import Elasticsearch
#import MongoEx
import csv
import pandas as pd

class ElasticSearching:
    def __init__(self):
        self.es = Elasticsearch([{'host':'210.107.192.201','port':9200}])

    def search(self,query,scheme,alpha,beta,gamma):
        #content = query.replace(r"/",',')
        content = query
        token = content.split(' ')
        content = [x for idx,x in enumerate(token) if not idx == 0]
        content = ' '.join(content)

        analyzer = 'my_DFR_analyzer'
        resTitle = self.es.search(index=scheme,doc_type='article',q='title:' + content,analyzer=analyzer,size=1000)
        resAbstract = self.es.search(index=scheme,doc_type='article',q='Abstract:' + content,analyzer=analyzer,size=1000)
        resBody = self.es.search(index=scheme,doc_type='article',q='body:' + content,analyzer=analyzer,size=1000)

        v = pd.DataFrame()
        l = pd.DataFrame()
        for entry in resTitle['hits']['hits']:
            pmcid = entry['_source']['pmcid']
            score = entry['_score']
            l = l.append(pd.DataFrame({'pmcid':[pmcid], 'title':[score]}))

        v = l
        l = pd.DataFrame()
        for entry in resAbstract['hits']['hits']:
            pmcid = entry['_source']['pmcid']
            score = entry['_score']
            l = l.append(pd.DataFrame({'pmcid':[pmcid], 'abstract':[score]}))

        v = pd.merge(v,l,how = 'outer', on =['pmcid'])
        l = pd.DataFrame()
        for entry in resBody['hits']['hits']:
            pmcid = entry['_source']['pmcid']
            score = entry['_score']
            l = l. append(pd.DataFrame({'pmcid':[pmcid], 'body':[score]}))

        v = pd.merge(v,l,how = 'outer', on = ['pmcid'])
        v = v.fillna(0)
        v['score'] = alpha*v['title']+beta*v['abstract']+gamma*v['body']
        return v.ix[:,['pmcid','score']]


    def test(self):
        with open('summary2.csv','rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for idx,item in enumerate(reader):
                query = item['summary'].replace(r"/",',')
                abstractQuery = {"abstract" : query}
                res = self.es.search(index="trec",doc_type="BM25",q=query,analyzer="my_BM25_analyzer",size=100)
                for doc in res['hits']['hits']:
                    text = '{0},{1}'.format(doc['_source']['pmcid'],doc['_score'])
                    print text

# Example
#e = ElasticSearch()
#result = e.search(q,'summary','dfr',0.3,0.3,0.4)


#print result['pmcid']
#print result['score']
