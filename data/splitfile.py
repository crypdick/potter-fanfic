#!/usr/bin/python
'''
Splits a file into numbered files, one line per file
'''

def main() :
    fin = open("stories.csv","r")
    i=0
    for line in fin :
        dir=str(i/1000)
        fi = str(i % 1000)
        if i == 0 :
            fout = open("stories/header", "w");
        else :
            fout = open("stories/" + dir + "/" + fi, "w");
        fout.write(line);
        i = i+1

main()
