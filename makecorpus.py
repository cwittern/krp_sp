#!/usr/bin/env python    -*- coding: utf-8 -*-
import os, sys, codecs, random

krshadow="/home/chris/projects/kr-shadow/"
bu=["KR1", "KR2","KR3","KR4","KR6"]
sample=100
cat=True
def make_corpus():
    if cat:
        of = codecs.open("corpus-all-s%3.3d.txt" % (sample), "w", "utf-8")
    for i, b in enumerate(bu):
        ipd="%s%s" % (krshadow, b)
        if not cat:
            of = codecs.open("corpus%s-s%d.txt" % (b, sample), "w", "utf-8")
            
        files = [a for a in os.listdir(ipd) if a.startswith("KR")]
        cnt = 0
        for f in random.sample(files, sample):
            print (f)
            for line in codecs.open("%s/%s" % (ipd, f)).readlines():
                cnt +=1
                if (cnt % 100) == 99:
                    of.write("\n")
                line = line.replace("\n", "")
                line = line.replace("　", "")
                if line.startswith("*"):
                    continue
                if not(line.startswith("#")):
                    of.write(line)
    of.close()

# for i, b in enumerate(bu):
#     ipd="%s%s" % (krshadow, b)

make_corpus()
