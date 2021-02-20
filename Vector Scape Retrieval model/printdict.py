import sys
dict_file=sys.argv[1]

with open(dict_file,'r') as fb:
    while True:
        line=fb.readline()
        if line == "":
            break
        print(line,end="")