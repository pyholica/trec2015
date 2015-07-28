from elasticsearch import Elasticsearch
import numpy as np
import pandas as pd
import MongoEx

class ElasticTraining:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])
        self.que = pd.read_csv(open('query2014.csv'),sep='\t')
        self.ans = pd.read_csv(open('answer2014.csv'),sep='\t')
        self.field = ['title','body','abstract']
        self.scheme = ['tfidf', 'bm25','ib','lmd','lmj','dfr']

    def buildPairDB(self):
        filename1 = 'pair_answer2014.csv'
        filename2 = 'eval_answer2014.csv'
        
        tByTopic = []

        ans = pd.read_csv(open('answer2014.csv'),sep='\t')
        for i in range(1,31):
            tByTopic.append(ans[ans['topic'] == i])

        
        l = pd.DataFrame()
        eva = pd.DataFrame()

        cum =  0
        for topic_bundle in tByTopic:
            relnum = len(topic_bundle[(topic_bundle['relevancy']==2) | (topic_bundle['relevancy']==1)])
            cnt = (relnum*4)/5
            zerocnt = cnt
            cum = cum + cnt
            print "COUNT:",cnt
            print "CUM :", cum
            for idx,entry in topic_bundle.iterrows():
                if ((entry['relevancy'] == 1) or (entry['relevancy'] == 2)) and (not cnt == 0):
                    l = l.append(pd.DataFrame({
                                "pmcid" : [entry['pmcid']],
                                "topic" : [entry['topic']],
                                "relevancy" : [entry['relevancy']]
                                }))
                    cnt = cnt - 1
                elif (entry['relevancy'] == 0) and (not zerocnt == 0):
                    l = l.append(pd.DataFrame({
                                "pmcid" : [entry['pmcid']],
                                "topic" : [entry['topic']],
                                "relevancy" : [entry['relevancy']]
                                }))
                    zerocnt = zerocnt - 1
                else:
                    eva = eva.append(pd.DataFrame({
                                "pmcid" : [entry['pmcid']],
                                "topic" : [entry['topic']],
                                "relevancy" : [entry['relevancy']]
                                }))

        l.to_csv(filename1,sep='\t',index=False)
        eva.to_csv(filename2,sep='\t',index=False)

    def search_scheme(self,scheme,num,ds):
        filename = "search_result/"+ scheme + "_"+ds+"_"+str(num)+".csv"
        pmcList = []
        relevancyList = []

        for index,entry in self.que.iterrows():
            if entry['topic'] == num:
                query = entry
                break

        for index,entry in self.ans.iterrows():
            if entry['topic'] == num:
                pmcList.append(entry['pmcid'])
                relevancyList.append(entry['relevancy'])
                
        reTable = pd.DataFrame({"pmcid" : pmcList, "relevancy" : relevancyList})

        content = query[ds].replace(r"/",',')
        analyzer = "my_"+scheme+"_analyzer"

        res = self.es.search(index=scheme +"_garam",q=content,doc_type='article',analyzer=analyzer,size=40000,request_timeout=120)

        l = pd.DataFrame()
        for entry in res['hits']['hits']:
            if entry['_source']['topicnum'] == num:
                pmcid = entry['_source']['pmcid']
                score = entry['_score']
                l = l.append(pd.DataFrame({"pmcid" : [pmcid],"score" : [score]}))

        l = pd.merge(l,reTable,how='inner',on=['pmcid'])
        l = l.fillna(0)
        l.to_csv(filename,sep='\t',index=False)

    def search_field(self,num,ds,scheme):
        filename = "search_result/"+"field_" + scheme + "_" +ds + "_" + str(num) + ".csv"
        for index,entry in self.que.iterrows():
            if entry['topic'] == num:
                query = entry
                break
        pmcList = []
        relevancyList = []

        for index,entry in self.ans.iterrows():
            if entry['topic'] == num:
                pmcList.append(entry['pmcid'])
                relevancyList.append(entry['relevancy'])

        reTable = pd.DataFrame({"pmcid":pmcList,"relevancy":relevancyList})

        content = query[ds].replace(r"/",',')
        token = content.split(' ')
        content = [ x for idx,x in enumerate(token) if not idx == 0]
        content = ' '.join(content)

        analyzer = "my_"+scheme+"_analyzer"

        resTitle= self.es.search(index=scheme+"_garam",q='title:' + content,doc_type='article',analyzer=analyzer,size=40000,request_timeout=200)
        print "Done with title :",len(resTitle['hits']['hits'])
        l = pd.DataFrame()
        for entry in resTitle['hits']['hits']:
            if entry['_source']['topicnum'] == num:
                pmcid = entry['_source']['pmcid']
                score = entry['_score']
                l = l.append(pd.DataFrame({"pmcid":[pmcid], 'title':[score]}))

        resAbstract= self.es.search(index=scheme+"_garam",q='abstract:'+content,doc_type='article',analyzer=analyzer,size=40000,request_timeout=200)
        print "Done with abstract :",len(resAbstract['hits']['hits'])
        resBody= self.es.search(index=scheme+"_garam",q='body:'+content,doc_type='article',analyzer=analyzer,size=40000,request_timeout=200)
        print "Done with body :",len(resBody['hits']['hits'])
        

        v = l
        l = pd.DataFrame()
        
        for entry in resAbstract['hits']['hits']:
            if entry['_source']['topicnum'] == num:
                pmcid = entry['_source']['pmcid']
                score = entry['_score']
                l = l.append(pd.DataFrame({"pmcid":[pmcid], 'abstract' : [score]}))
        print "V:",len(v)
        print "L:",len(l)
    
        v = pd.merge(v,l,how='outer',on=['pmcid'])
        l = pd.DataFrame()
        for entry in resBody['hits']['hits']:
            if entry['_source']['topicnum'] == num:
                pmcid = entry['_source']['pmcid']
                score = entry['_score']
                l = l.append(pd.DataFrame({"pmcid":[pmcid], 'body' : [score]}))

        v = pd.merge(v,l,how='outer',on=['pmcid'])
        v=v.fillna(0)
        v = pd.merge(v,reTable,how='inner',on=['pmcid'])
        v=v.fillna(0)
        v.to_csv(filename,sep='\t',index=False)

    def training_scheme3(self,s1,s2,s3,ds):
        l = pd.DataFrame()
        for i in range(1,31):
            print "working on topic",str(i)
            filename1 = 'scheme_' + s1 + '_' + ds + '_' + str(i) + '_training.csv'
            filename2 = 'scheme_' + s2 + '_' + ds + '_' + str(i) + '_training.csv'
            filename3 = 'scheme_' + s3 + '_' + ds + '_' + str(i) + '_training.csv'

            data1 = pd.read_csv(open("vector/"+filename1),sep='\t')
            data2 = pd.read_csv(open("vector/"+filename2),sep='\t')
            data3 = pd.read_csv(open("vector/"+filename3),sep='\t')

            data1 = data1.rename(columns={'score':s1})
            data2 = data2.rename(columns={'score':s2})
            data3 = data3.rename(columns={'score':s3})

            m = pd.merge(data1,data2,how='outer',on=['pmcid','relevancy'])
            m = pd.merge(m,data3,how='outer',on=['pmcid','relevancy'])
            m = m.fillna(0)

            em_min = float('inf')
            remember_alpha = 0
            remember_beta = 0

            for alpha in np.arange(0,1,0.01):
                for beta in np.arange(0,1,0.01):
                    normA = m[s1]/m[s1].sum()
                    normB = m[s2]/m[s2].sum()
                    normC = m[s3]/m[s3].sum()

                    score = (1-alpha)*(1-beta)*normA + (1-alpha)*beta*normB + alpha*normC
                    relevancy = m['relevancy']

                    em = (relevancy-score) ** 2

                    if em.sum() < em_min:
                        em_min = em.sum()
                        remember_alpha = alpha
                        remember_beta = beta
            l = l.append(pd.DataFrame({
                        'scheme1' : [s1],
                        'scheme2' : [s2],
                        'scheme3' : [s3],
                        'topic' : [i],
                        'loss' : [em_min],
                        'alpha' : [(1-remember_alpha)*(1-remember_beta)],
                        'beta' : [(1-remember_alpha)*remember_beta],
                        'gamma' : [remember_alpha]
                        }))
        
        l.to_csv('analysis/' + 'scheme_' + s1 +'_' +s2 + '_' + s3 + '_' + ds + '.csv',sep='\t',index=False)     

    def training_scheme(self,s1,s2,ds):
        l = pd.DataFrame()
        for i in range(1,31):
            filename1 = 'scheme_' + s1 + '_' + ds + '_' + str(i) + '_training.csv'
            filename2 = 'scheme_' + s2 + '_' + ds + '_' + str(i) + '_training.csv'

            data1 = pd.read_csv(open("vector/"+filename1),sep='\t')
            data2 = pd.read_csv(open("vector/"+filename2),sep='\t')

            data1 = data1.rename(columns={'score':s1})
            data2 = data2.rename(columns={'score':s2})

            m = pd.merge(data1,data2,how='outer',on=['pmcid','relevancy'])
            m = m.fillna(0)
            
            min_em = float("inf")
            remember_alpha = 0

            for alpha in np.arange(0,1,0.01):
                normA = m[s1]/m[s1].sum()
                normB = m[s2]/m[s2].sum()
                
                score= alpha*normA + (1-alpha)*normB
                relevancy = m['relevancy']
                
                em = (relevancy - score) ** 2
                
                if em.sum() < min_em:
                    min_em = em.sum()
                    remember_alpha = alpha
                    
            l = l.append(pd.DataFrame( 
                    {
                        'scheme1' : [s1], 
                        'scheme2' : [s2], 
                        'ds' : [ds], 
                        'topic' : [i], 
                        'loss'  : [min_em], 
                        'alpha' : [remember_alpha],
                        'beta' : [1-remember_alpha]
                        }
                    ))
        l.to_csv('analysis/' + s1+'_'+s2+'_'+ds+'.csv',sep='\t',index=False)
        
    def test(self):
         # Find the topic we are dealing with
        for entry in self.que:
            if entry['number'] == str(1):
                query = entry
                break

        content = query['description'].replace(r"/",",")
        res = self.es.search(index='tfidf',q=content,doc_type="article",analyzer="my_tfidf_analyzer",size=1500)

        print str(res['hits']['hits'][0]['_score'])
                 
        
    def buildVectorWithScheme(self,num,scheme,ds='summary'):
        filename = scheme + "_" + ds + "_" + str(num) + ".csv"
        filename_training = 'scheme_' + scheme + '_' + ds + '_' + str(num) + '_training.csv'
        filename_eval = 'scheme_' + scheme + '_' + ds + '_' + str(num) + '_eval.csv'
        print "Working on",filename
        data = pd.read_csv(open('search_result/' + filename),sep='\t')
        data_shuffle = data.iloc[np.random.permutation(len(data))]

        training = pd.DataFrame()
        evaluation = pd.DataFrame()

        cnt = len(data[(data['relevancy'] == 1) | (data['relevancy'] == 2)])*4/5
        zero_cnt = cnt

        for index,entry in data_shuffle.iterrows():
            if entry['relevancy'] == 0:
                if zero_cnt == 0:
                    evaluation = evaluation.append(entry)
                else:
                    # training = training.append(entry)
                    zero_cnt = zero_cnt -1
            else:
                if cnt==0:
                    evaluation = evaluation.append(entry)
                else:
                    training = training.append(entry)
                    cnt = cnt - 1

        training.to_csv('vector/'+filename_training,sep='\t',index=False)
        evaluation.to_csv('vector/'+filename_eval,sep='\t',index=False)
        
            
    def buildVectorWithField(self,scheme,num,ds='summary'):
        filename = "field" + "_" + scheme+"_" + ds + "_"  + str(num) + ".csv"
        filename_training = "field" + "_" + scheme+"_" + ds + "_"  + str(num) + "_training.csv"
        filename_eval = "field" + "_" + scheme+ "_" + ds + "_" + str(num) + "_eval.csv" 
        print "Working on",filename
        data = pd.read_csv(open("search_result/"+filename),sep='\t')
        data_shuffle = data.iloc[np.random.permutation(len(data))]

        training = pd.DataFrame()
        evaluation = pd.DataFrame()

        cnt = len(data[(data['relevancy'] == 1) | (data['relevancy'] == 2)])*4/5
        zero_cnt = cnt
        

        for idx,entry in data_shuffle.iterrows():
            if entry['relevancy'] == 0:
                if zero_cnt == 0:
                    evaluation = evaluation.append(entry)
                else:
                    #training = training.append(entry)
                    zero_cnt = zero_cnt - 1
            else:
                if cnt == 0:
                    evaluation = evaluation.append(entry)
                else:
                    training = training.append(entry)
                    cnt = cnt - 1

        training.to_csv('vector/'+filename_training,sep='\t',index=False)
        evaluation.to_csv('vector/'+filename_eval,sep='\t',index=False)  

      

    def training_field(self,scheme,ds):

        l = pd.DataFrame()
        for i in range(1,31):
            print "Topic :",str(i)
            em_min = float("inf")
            remember_alpha = 0
            remember_beta = 0
            filename = 'field_' + scheme + '_' + ds + '_' + str(i) + '_training.csv'
            data = pd.read_csv(open("vector/"+filename),sep='\t')
            data.drop_duplicates(subset='pmcid',take_last=True,inplace=True)
            
            for alpha in np.arange(0,1,0.01):
                for beta in np.arange(0,1,0.01):
                    normA = data['title']/data['title'].sum()
                    normB = data['abstract']/data['abstract'].sum()
                    normC = data['body']/data['body'].sum()

                    score = (1-alpha)*(1-beta)*normA + (1-alpha)*beta*normB + alpha*normC
                    relevancy = data['relevancy']

                    em = (relevancy - score) ** 2

                    if em.sum() < em_min:
                        em_min = em.sum()
                        remember_alaph = alpha
                        remember_beta = beta
            print "Alpha:",(1-remember_alpha)*(1-remember_beta)
            print "Beta:",(1-remember_alpha)*remember_beta
            print "Gamma:",remember_alpha

            l = l.append(pd.DataFrame({
                'scheme' : [scheme],
                'ds' : [ds],
                'topic' : [i],
                'loss' : [em_min],
                'alpha' : [(1-remember_alpha)*(1-remember_beta)],
                'beta' : [(1-remember_alpha)*remember_beta],
                'gamma' : [remember_alpha]
            }))
        l.to_csv('analysis/' +'field_' + scheme + '_' + ds+ '.csv',sep='\t',index=False)
