from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import os
import sys
root_path=sys.argv[1]
index_file=sys.argv[2]
all_files = os.listdir(root_path)
stop_words = set(stopwords.words("english"))
dict = {}
N=0 #total number of docs in collection
for file_path in all_files:
    file_path = root_path + "/" + file_path
    with open(file_path,'r') as fb:
        while True:
            line=fb.readline()
            if line=="":
                break
            if line == "<DOC>\n":
                N+=1
                line=fb.readline()
                arr=line.split()
                doc_id=arr[1]
                temp_dict = {}
                while True:
                    line=fb.readline()
                    if line=="</DOC>" or line=="</DOC>\n":
                        break

                    #checking if line string is <Text>
                    if line == "<TEXT>\n":
                        line = fb.readline()
                        words=word_tokenize(line)
                        
                        i=0
                        while i<len(words):
                            if(words[i]=="<"):
                                i+=1
                                tag=words[i]
                                s=""
                                i+=2
                                while words[i] != "<":
                                    s+=words[i]
                                    i+=1
                                i+=3
                                prev=s
                                s=tag[0]+":"+s
                                if s not in stop_words:
                                    if s.lower()[0] >= 'a' and s.lower()[0] <= 'z' and len(s)>=3: 
                                        temp_dict[s.lower()]=temp_dict.get(s.lower(),0) + 1

                                if prev not in stop_words:
                                    if prev.lower()[0] >= 'a' and prev.lower()[0] <= 'z' and len(prev)>=3: 
                                        temp_dict[prev.lower()]=temp_dict.get(prev.lower(),0) + 1
                            else:
                                # find the frequency of all the words in the current document
                                if words[i] not in stop_words:
                                    if words[i].lower()[0] >= 'a' and words[i].lower()[0] <= 'z' and len(words[i])>=3:
                                        temp_dict[words[i].lower()] = temp_dict.get(words[i].lower(),0) +1
                                i+=1
                
                # storing all the words found in current doc in main dict
                for ele in temp_dict:
                    if dict.get(ele):
                        dict[ele][0] += 1
                        ar = [doc_id,temp_dict[ele]]
                        dict[ele].append(ar)
                    else:
                        dict[ele] = [1,[doc_id,temp_dict[ele]]]


dict_arr = sorted(dict.keys())
posting_file=index_file+".idx"
dict_file=index_file+".dict"
fb1=open(posting_file,'w')
fb1.write(str(N)+"\n")
fb2=open(dict_file,'w')
vocab_cnt=0
for ele in dict_arr:
    s1=ele+":"+str(dict[ele][0])+":"+str(vocab_cnt)+"\n"
    vocab_cnt+=1
    fb2.write(s1)
    s = str(ele) + " "
    s+=str(dict[ele][0])+" "
    for i in range(1,len(dict[ele])):
        for obj in dict[ele][i]:
            s=s+str(obj)+" "
    s=s.rstrip()
    s += "\n"
    fb1.write(s)

fb1.close()
fb2.close()