import sys
from nltk.corpus import stopwords
import math
import bisect

N=0 # total number of docs
def words_with_given_prefix(words_list_for_prefix,ele):
    result=[]
    new_word=ele[:len(ele)-1]
    index_in_words_list=bisect.bisect_left(words_list_for_prefix,new_word)
    for i in range(index_in_words_list,len(words_list_for_prefix)):
        if words_list_for_prefix[i].startswith(new_word):
            result.append(words_list_for_prefix[i])
        else:
            break
    return result

def search_engine(queryfile,k,resultfile,indexfile,dictfile):
    res=open(resultfile,'w')

    #RETRIEVE THE INVERTED INDEX AND POSTINGS LIST FROM THE FILE AND FIND THE MAGNITUDE OF ALL THE VECTORS.
    inverted_index={}  # word -> [docfreq , lists of [docid , termfreq]]
    magnitude_of_docs={} # docs -> magnitude of document vector
    words_list_for_prefix=[] # sorted list of index words for prefix finding.

    with open(indexfile,'r') as fb:
        N=float(fb.readline())
        while True:
            line = fb.readline()
            if line=="":
                break
            words=line.split()
            index_word=words[0]
            arr=[]
            document_freq=words[1]
            idf_value=math.log2(1+(float(N)/float(document_freq)))
            arr.append(idf_value)
            
            i=2
            while i<len(words)-1:
                temp=[]
                temp.append(words[i])
                document_id=words[i]
                temp.append(words[i+1])
                term_frequency_in_doc=words[i+1]
                tf_value_doc=1+math.log2(float(term_frequency_in_doc))
                score_for_word_in_doc=idf_value*tf_value_doc
                magnitude_of_docs[document_id]=magnitude_of_docs.get(document_id,0)+score_for_word_in_doc**2
                arr.append(temp)
                i+=2
            inverted_index[index_word]=arr
            words_list_for_prefix.append(index_word)

    #EXTRACT THE QUERY WORDS
    stop_words=set(stopwords.words("english"))
    query_dict={}  #query -> [array of words]

    with open(queryfile,'r') as fb:
        while True:
            line=fb.readline()
            if line=="":
                break
            words_in_query=line.split()
            if len(words_in_query)>0 and  words_in_query[0]=="<num>":
                query_id=words_in_query[2]
                while len(words_in_query)==0 or words_in_query[0]!="<title>":
                    line=fb.readline()
                    words_in_query=line.split()
                temp=[]
                for i in range(2,len(words_in_query)):
                    if words_in_query[i] not in stop_words:
                        if words_in_query[i].lower()[0]>='a' and words_in_query[i].lower()[0]<='z':
                            if words_in_query[i].lower()[:2]=="n:": #For all noun query words.
                                word1="p:"+words_in_query[i].lower()[2:]
                                if word1[len(word1)-1]=='*':
                                    prefix_words_list=words_with_given_prefix(words_list_for_prefix,word1)
                                    for ele_words in prefix_words_list:
                                        temp.append(ele_words)
                                else:
                                    temp.append(word1)

                                word2="l:"+words_in_query[i].lower()[2:]
                                if word2[len(word2)-1]=='*':
                                    prefix_words_list=words_with_given_prefix(words_list_for_prefix,word2)
                                    for ele_words in prefix_words_list:
                                        temp.append(ele_words)
                                else:
                                    temp.append(word2)

                                word3="o:"+words_in_query[i].lower()[2:]
                                if word3[len(word3)-1]=='*':
                                    prefix_words_list=words_with_given_prefix(words_list_for_prefix,word3)
                                    for ele_words in prefix_words_list:
                                        temp.append(ele_words)
                                else:
                                    temp.append(word3)
                            else:
                                if words_in_query[i].lower()[len(words_in_query[i])-1]=='*':
                                    prefix_words_list=words_with_given_prefix(words_list_for_prefix,words_in_query[i].lower())
                                    for ele_words in prefix_words_list:
                                        temp.append(ele_words)
                                else:
                                    temp.append(words_in_query[i].lower())
                
                if len(temp)>0:
                    query_dict[query_id]=temp

    

    #BUILDING THE DOCUMENT VECTOR (USING A DICTIONARY) FOR EVERY QUERY
    for query in query_dict:
        doc_vector={}  # docid -> (index of query word , tf*idf score)
        query_vector={}
        words_in_query=query_dict[query]
        words_count={}  # freq of each word in query
        for word in words_in_query:
            words_count[word]=words_count.get(word,0)+1

        for i in range(len(words_in_query)):
            idf_value=0
            if inverted_index.get(words_in_query[i]):
                postings_list=inverted_index[words_in_query[i]]
                idf_value=postings_list[0]

                for j in range(1,len(postings_list)):
                    docid=postings_list[j][0]
                    term_freq=postings_list[j][1]
                    tf_value_doc=1+math.log2(float(term_freq))
                    score_doc=idf_value*tf_value_doc
                    if doc_vector.get(docid):
                        doc_vector[docid].append((i,score_doc))
                    else:
                        doc_vector[docid]=[(i,score_doc)]

            term_freq_query=words_count[words_in_query[i]]
            tf_value_query=1+math.log2(float(term_freq_query))
            score_query=idf_value*tf_value_query
            query_vector[i]=score_query

        final_list_of_docs=[]
        for doc in doc_vector:
            vector=doc_vector[doc]
            final_score_doc=0
            mag_query_vector=0
            mag_doc_vector=0
            for unit1 in query_vector:
                mag_query_vector += query_vector[unit1]**2
            mag_query_vector=math.sqrt(mag_query_vector)
            for unit in vector:
                index=unit[0]
                final_score_doc+=unit[1]*query_vector[index]

            mag_doc_vector=math.sqrt(magnitude_of_docs[doc])
            total_denominator=mag_query_vector*mag_doc_vector
            final_score_doc=final_score_doc/total_denominator
            final_list_of_docs.append((final_score_doc,doc))

        final_list_of_docs.sort(reverse=True)
        cnt1=1
        for ele in final_list_of_docs:
            if cnt1==k+1:
                break
            if query !="100":
                s=str(query[1:])+" "+"Q0"+" "+str(ele[1])+" "+str(cnt1)+" "+str(ele[0])+" "+"STANDARD"+"\n"
            else:
                s=str(query)+" "+"Q0"+" "+str(ele[1])+" "+str(cnt1)+" "+str(ele[0])+" "+"STANDARD"+"\n"
            cnt1+=1
            res.write(s)
        res.write("\n")
        res.write("\n")
    
    res.close()

if __name__ == '__main__':
    #TAKE ALL THE COMMAND LINE ARGUMENTS AND PASS INTO THE FUNCTION SEARCH ENGINE
    arguments=sys.argv
    query_file=""
    k=0
    result_file=""
    index_file=""
    dict_file=""
    i=1
    while i<len(arguments):
        if arguments[i]=="--query":
            query_file=arguments[i+1]
            i+=2
        elif arguments[i]=="--cutoff":
            k=int(arguments[i+1])
            i+=2
        elif arguments[i]=="--output":
            result_file=arguments[i+1]
            i+=2
        elif arguments[i]=="--index":
            index_file=arguments[i+1]
            i+=2
        elif arguments[i]=="--dict":
            dict_file=arguments[i+1]
            i+=2
    
    if k==0:
        k=10
    search_engine(query_file,k,result_file,index_file,dict_file)
    