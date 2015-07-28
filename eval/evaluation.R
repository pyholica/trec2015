library(stringr)
#setwd("C:\\Users\\ajou\\Documents\\TREC\\code\\eval")
#setwd("/Users/woojin/Dropbox/woojin/code/py/keywordSearch")
setwd("C:/Users/ajou/Dropbox/woojin/code/eval")
getwd()
#answers = read.csv("testDataAnswer.txt", sep = "\t")
answers = read.csv("2014answer.csv", sep = ",")
head(answers)

for (i in 1:30 ) {
  assign(paste("answer", i, sep=''), answers[answers$topicNum==i,]['Pmcid'])
}

make_val <- function(path, name){
  for (i in 1:30 ) {
    col = c(path,i,".csv")
    file = paste(col, collapse = '')
    print(file)
    data = read.csv(file)
    #print(data)
    assign(paste(name, i, sep=''), data['pmcid'], envir = .GlobalEnv)
    print(paste(name, i, sep=''))
  }
  return(do_eval(name))
}

do_eval <- function(name){
  list <- vector()
  for (i in 1:30){
    data = paste(c(name, i), collapse = '')
    ans = paste(c("answer", i), collapse = '')
    print(ans[[1]])
    precision =length(intersect(get(data)[[1]], get(ans)[[1]]))
    print(paste(i, length(intersect(get(data)[[1]], get(ans)[[1]])), sep = ', '))  
    list <- c(list, precision)
  }
  return(list)
}


tfidf_desc <- make_val(".\\TFIDF_400\\TFIDF description", "TFIDF description")
tfidf_smry <- make_val(".\\TFIDF_400\\TFIDF summary", "TFIDF summary")
#make_val(".\\TFIDF(5gram)\\description\\TF-IDF_5gram_description", "TF_IDF_5gram_description")
#make_val(".\\TFIDF(5gram)\\summary\\TF-IDF_5gram_summary", "TF_IDF_5gram_summary")
bm25_desc <- make_val(".\\12BM25_400\\BM25 description", "BM25 description")
bm25_smry <- make_val(".\\12BM25_400\\BM25 summary", "BM25 summary")
dfr_desc <- make_val(".\\DFR_400\\DFR description", "DFR description")
dfr_smry <- make_val(".\\DFR_400\\DFR summary", "DFR summary")
ib_desc <- make_val(".\\IB_400\\IB description", "IB description")
ib_smry <- make_val(".\\IB_400\\IB summary", "IB summary")
lmd_desc <- make_val(".\\LMD_400\\LMD description", "LMD description")
lmd_smry <- make_val(".\\LMD_400\\LMD summary", "LMD summary")
lmj_desc <- make_val(".\\LMJ_400\\LMJ description", "LMJ description")
lmj_smry <- make_val(".\\LMJ_400\\LMJ summary", "LMJ summary")

ib_desc <- make_val(".\\IB_400\\IB description", "IB description")
ib_desc_boost <- make_val(".\\IB_BOOST_400\\IB description", "IB description")
ib_desc_boost2 <- make_val(".\\IB_BOOST2_400\\IB description", "IB description")
ib_desc_boost_syno <- make_val(".\\IB_BOOST400_SYNO\\IB description", "IB description")
ib_desc_boost_syno2 <- make_val(".\\IB_BOOST_400_SYNO2\\IB description", "IB description")
ib_smry <- make_val(".\\IB_400\\IB summary", "IB summary")
ib_smry_boost <- make_val(".\\IB_BOOST_400\\IB summary", "IB summary")
ib_smry_boost2 <- make_val(".\\IB_BOOST2_400\\IB summary", "IB summary")
ib_smry_boost_syno <- make_val(".\\IB_BOOST400_SYNO\\IB summary", "IB summary")
ib_smry_boost_syno2 <- make_val(".\\IB_BOOST_400_SYNO2\\IB summary", "IB summary")

ib_smry_stop <- make_val(".\\IB_STOP_400\\IB summary", "IB summary")
getwd()
dfr_edge_smry <- make_val("./DFR_EdgeNGram_400/DFR summary", "DRF summary")
dfr_edge_smry_standard <- make_val("./DFR_EdgeNGram_400_Standard/DFR summary", "DRF summary")
bm25_edge_smry <- make_val("./BM25_EdgeNGram_400/BM25 summary", "BM25 summary")
bm25_edge_smry_standard <- make_val("./BM25_EdgeNGram_400_Standard/BM25 summary", "BM25 summary")

DFR_edge_smry_standard <- make_val("./Keyword_DFR_NGRAM/DFR_EDGE_NGRAM suumary", "DFR_EDGE_NGRAM suumary1")
DFR_edge_desc_standard <- make_val("./Keyword_DFR_NGRAM_DESC/DFR_EDGE_NGRAM description", "DFR_EDGE_NGRAM desc")

DFR_topic_expansion <- make_val("./topic_DFR/DFR_topic_queryexpansion_2014/DFR summary", "DFR summary")

DFR_topic_expansion_edge <- make_val("./topic_DFR/DFR_topic_queryexpansion_EDGE_2014/DFR summary", "DFR summary")

evaluation2 <- data.frame(ib_desc
                          ,ib_desc_boost
                          ,ib_desc_boost2
                          ,ib_desc_boost_syno
                          ,ib_desc_boost_syno2
                          ,ib_smry
                          ,ib_smry_boost
                          ,ib_smry_boost2
                          ,ib_smry_boost_syno
                          ,ib_smry_boost_syno2)


evaluation <- data.frame(tfidf_desc
                        ,tfidf_smry
                        ,bm25_desc
                        ,bm25_smry
                        ,dfr_desc
                        ,dfr_smry
                        ,ib_desc
                        ,ib_smry
                        ,lmd_desc
                        ,lmd_smry
                        ,lmj_desc
                        ,lmj_smry)

evaluation <- data.frame(ib_smry_stop)

evaluation_edge <- data.frame(dfr_edge_smry)
evaluation_edge <- data.frame(dfr_edge_smry_standard)
evaluation_edge <- data.frame(bm25_edge_smry)
evaluation_edge <- data.frame(bm25_edge_smry_standard)

evaluation_edge <- data.frame(DFR_edge_desc_standard)

evaluation_topic_expans <- data.frame(DFR_topic_expansion)

evaluation_topic_expans_edge <- data.frame(DFR_topic_expansion_edge)

write.csv(evaluation_topic_expans_edge, file="evaluation_topic_expans_edge.csv")
