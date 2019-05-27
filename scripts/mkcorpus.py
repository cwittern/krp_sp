#  -*- coding: utf-8 -*-
# create the corpus files from kr-shadow
# usage: 
# first, check out the repositories KR1 to KR6 from https://github.com/kr-shadow.  Store them as subdirectories to kr-shadow
# make a directory called data as a subdirectory to here
# then run
# python mkcorpus.py <full path-to-kr-shadow/>

import os, codecs, sys

krshadow=sys.argv[1]

bu=[a for a in os.listdir(krshadow) if a.startswith("KR")]
for l in bu:
    lei=set([a[0:4] for a in os.listdir("%s%s" % (krshadow, l)) if a.startswith("KR")])
    for lf in lei:
        of = codecs.open("data/%s.txt" % (lf), "w", "utf-8")
        files = [a for a in os.listdir("%s%s" % (krshadow, l)) if a.startswith(lf)]
        files.sort()
        lx = 0
        for f in files:
            print(f)
            for line in codecs.open("%s%s/%s" % (krshadow, l, f)).readlines():
                line = line.replace("\n", "")
                line = line.replace("　", "")
                if line.startswith("*"):
                    continue
                if line.startswith("#"):
                    continue
                l1 = len(line)
                lx += l1
                if lx > 1000:
                    of.write("\n")
                    lx = 0
                of.write(line)
        of.close()
