Abhinav
------------------------------------
This directory contains an implementation of Vector Space Model of Information Retrieval.
The Python version used for implementation is 3.8.5
------------------------------------
External Library Used :
NLTK
------------------------------------
All the files will generate in the same directory of python files.
------------------------------------
For creation of Inverted Index : 
command : python invidx.py coll-path indexfile
where, coll-path specifies the directory containing the files containing documents of the collection, and indexfile is the file name.
The two files: (i) indexfile.idx and (ii) indexfile.dict will be generated in the same directory.
-------------------------------------
Printing dictionary : 
command : python printdict.py indexfile.dict
The indexfile.dict will be in the directory od printdict.py
-------------------------------------
For Querying : 
command : python vecsearch.py --query queryfile --cutoff k --output resultfile --index indexfile --dict dictfile
This command is case sensitive.
Note : Except --cutoff, all arguments are necessary. Value of k(cutoff) is 10 by default.