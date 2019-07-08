#  -*- coding: utf-8 -*-
import sys, os, codecs, math, re
#import sentencepiece as spm
import numpy as np
from random import sample
from collections import defaultdict

#sp_path = os.path.dirname(os.path.realpath(sys.argv[0]))

sp_path=os.getcwd()

krp_names={
"krp" : "KR Rep",
"KR1" : "經部",
"KR1a" : "易類",
"KR1b" : "書類",
"KR1c" : "詩類",
"KR1d" : "禮類",
"KR1e" : "春秋類",
"KR1f" : "孝經類",
"KR1g" : "五經總義類",
"KR1h" : "四書類",
"KR1i" : "樂類",
"KR1j" : "小學類",
"KR2" : "史部",
"KR2a" : "正史類",
"KR2b" : "編年類",
"KR2c" : "紀事本末類",
"KR2d" : "別史類",
"KR2e" : "雜史類",
"KR2f" : "詔令奏議類",
"KR2g" : "傳記類",
"KR2h" : "史鈔類",
"KR2i" : "載記類",
"KR2j" : "時令類",
"KR2k" : "地理類",
"KR2l" : "職官類",
"KR2m" : "政書類",
"KR2n" : "目錄類",
"KR2o" : "史評類",
"KR2p" : "簡帛金石類",
"KR3" : "子部",
"KR3a" : "儒家類",
"KR3b" : "兵家類",
"KR3c" : "法家類",
"KR3d" : "農家類",
"KR3e" : "醫家類",
"KR3f" : "天文算法類",
"KR3g" : "術數類",
"KR3h" : "藝術類",
"KR3i" : "譜錄類",
"KR3j" : "雜家類",
"KR3k" : "類書類",
"KR3l" : "小說家類",
"KR4" : "集部",
"KR4a" : "楚辭類",
"KR4b" : "別集類-漢六朝",
"KR4c" : "別集類-唐",
"KR4d" : "別集類-宋",
"KR4e" : "別集類-明",
"KR4f" : "別集類-清",
"KR4g" : "別集類-近",
"KR4h" : "總集類",
"KR4i" : "詩文評類",
"KR4j" : "詞曲類",
"KR5" : "道部",
"KR5a" : "洞真部",
"KR5b" : "洞玄部",
"KR5c" : "洞神部",
"KR5d" : "太玄部",
"KR5e" : "太平部",
"KR5f" : "太清部",
"KR5g" : "正一部",
"KR5h" : "續道藏",
"KR5i" : "清代道教文獻",
"KR5j" : "敦煌道教文獻",
"KR6" : "佛部",
"KR6a" : "阿含部類",
"KR6b" : "本緣部類",
"KR6c" : "般若部類",
"KR6d" : "法華部類",
"KR6e" : "華嚴部類",
"KR6f" : "寶積部類",
"KR6g" : "涅槃部類",
"KR6h" : "大集部類",
"KR6i" : "經集部類",
"KR6j" : "密教部類",
"KR6k" : "律部類",
"KR6l" : "毘曇部類",
"KR6m" : "中觀部類",
"KR6n" : "瑜伽部類",
"KR6o" : "論集部類",
"KR6p" : "淨土宗部類",
"KR6q" : "禪宗部類",
"KR6r" : "史傳部類",
"KR6s" : "事彙部類",
"KR6t" : "續諸宗(日本)",
"KR6u" : "敦煌寫本部類",
"KR6v" : "新編部類"}

def make_ngram_lists(n=3, vsize=100000):
    ndir="%s/ngram" % (sp_path)
    cdir="%s/data" % (sp_path)
    cs=[a for a in os.listdir(cdir) if a.endswith(".txt")]
    cs.sort()
    for c in cs:
        ngf=codecs.open("%s/n%d-%s.vocab" % (ndir, n, c[:-4]), "w", "utf-8")
        print(n, c)
        corpus="%s/%s" % (cdir, c)
        d=defaultdict(int)
        for line in codecs.open(corpus, "r", "utf-8"):
            line = re.sub(r"[\u3000-\u3fff\uff00-\uffff()/ ]", "", line)
            for i in range(len(line) - n):
                ng=line[i:i+n]
                d[ng] +=1
        dc=sum([a[1] for a in d.items()])
        ds=sorted(d.items(), key=lambda x : x[1], reverse=True)
        ngf.write("# %s n: %d, ngram_total_count: %d, voc_size: %d\n" % (c, n, dc, len(d)))
        for ng in ds[0:vsize]:
            ngf.write("%s\t%d\t%10.10f\n" % (ng[0], ng[1], ng[1] / dc))
        ngf.close()
            
def loadvocs(flag="n2", cutoff=30000, use_krp_names=True):
    mdir="ngram"
    ms=[a for a in os.listdir(mdir) if a.endswith("vocab") and a.startswith(flag)]
    ms.sort()
    mv=[]
    for m in ms:
        vl = loadvoc(m, cutoff)
        mv.append(vl)
    if use_krp_names:
        mn=[krp_names[a.split("-")[1].split(".")[0]] for a in ms]
    else:
        mn=[a.split("-")[1].split(".")[0] for a in ms]
    return (mn, mv)

def loadvoc(v, cutoff=30000):
    pas = "%s/ngram/%s" % (sp_path, v) 
    l=[]
    cnt = 0
    for line in codecs.open(pas, "r", "utf-8").readlines():
        if line.startswith("#"):
            continue
        cnt += 1
        if cnt > cutoff:
            break
        lx = line[:-1].split("\t")
        l.append((lx[0], float(lx[-1])))
    return l


    
def agg_voclist(mv, w=None):
    """mv is the list of voclist returned by loadmodels, w can be
    - 'score' : get the log score for each entry and add it to the entry, which thus becomes a tuple
    - 'pos' : use the id number (which is the position in the voclist)
    - None  : dont use any weight.  
    returns a dictionary of lists, one entry for each sp (with score option):
    {'好施' :
    [(13, -11.637325286865234),
    (16, -11.83456039428711),
    (18, -10.804060935974121),
    (20, -11.320064544677734),
    (40, -12.115601539611816),
    (41, -11.592039108276367),
    (42, -11.932478904724121),
    (56, -12.036428451538086),
    (72, -12.097436904907227)]}
    """
    vx=defaultdict(list)
    for i, vl in enumerate(mv):
        for j, v in enumerate(vl):
            # j is the id of this sp in this model
            if w is None:
                vx[v[0]].append(i)
            else:
                if w == 'score':
                    vx[v[0]].append((i, v[1]))
                elif w == 'pos':
                    vx[v[0]].append((i,j))
    return vx

def red_voclist(vx, up=40, lo=20):
    """Reduce the aggregate voclist by giving upper and lower limits for
the number of occurrences. Returns a list of key, value items, not a
dictionary, this can be converted to a dictionary with dict().
    """
    v2 = [a for a in vx.items() if len(a[1]) > lo and len(a[1]) < up]
    return v2

def vocmatrix(vx, size=77, vsize=30000, w=None):
    """Converts the aggregated voclist into a matrix."""
    sx=np.zeros((size,size))
    for v in vx:
        for b in v[1]:
            if isinstance(b, int):
                bu = b
            else:
                bu = b[0]
            for b1 in v[1]:
                if isinstance(b1, int):
                    bu1 = b1
                else:
                    bu1 = b1[0]
                # I only want to see one half of the matrix
                if bu < bu1:
                    # only count
                    if w is None:
                        sx[bu, bu1] += 1
                    else:
                        if w == 'score':
                            # we add the probabilities
                            px = math.exp(b[1]) + math.exp(b1[1])
                        else:
                            # we use position, but invert the size
                            px = ( (vsize - b[1]) + (vsize - b1[1])) / 2
                        sx[bu, bu1] += px
    return sx

def evalvocmatrix(sx, ms, cutoff=10):
    s1, s2 = sx.shape
    res={}
    for n in range(s1):
        o = []
        for i in range(s2):
            if n < i:
                try:
                    o.append((ms[i], sx[n, i]))
                except:
                    print("ERROR:", i, n, sx.shape, len(ms))
                    
            else:
                o.append((ms[i], sx[i, n]))
        o = sorted(o, key = lambda x : x[1], reverse=True)
        res[ms[n]] = o[0:cutoff]
    return res
#makemodels()

def report(flag, up=40, lo=10, w=None, cutoff=10, krp=False):
    ms, md, mv = k.loadmodels(flag=flag, use_krp_names=False)
    if krp:
        m="m0-krp-30000.model"
        ms, md, mv = add_model(m, ms, md, mv, use_krp_names=False)    
    vx = k.agg_voclist(mv, md, w=w)
    v2 = k.red_voclist(vx, up=up, lo=lo)
    sx = k.vocmatrix(v2, size=len(md), vsize=len(mv[0]), w=w)
    res = k.evalvocmatrix(sx, ms, cutoff=cutoff)
    return res
    
def report_matrix():
    flags=["n2", "n3", "n4", "n5"]
    labels={"None" : "Count", "score" : "Comb.prop", "pos" : "Position"}
    limits=[(70,35), (30, 5), (3,1)]
    weights=[None, 'score', 'pos']
    of=codecs.open("report1.txt", "w", "utf-8")
    reps=[]
    cnt=0
    for flag in flags:
        for up, lo in limits:
            for w in weights:
                res=report(flag, up, lo, w)
                if w is None:
                    w="None"
                flx=(flag, up, lo, w)
                print(flx)
                ofh=codecs.open("nrep/%s-%3.3d-%3.3d-%s.html" % flx, "w", "utf-8")
                ofh.write("""<html><body><h1>Result for calculation %d</h1>
                <p>Parameters: Ngram:%s, limits: %d,%d, Combination: %s</p>
                <table>\n""" % (cnt, flag, up, lo, labels[w]))
                ofh.write("<tr><th>部類</th><th>Self/Other</th><th>Most related部類</th></tr>")
                reps.append((flx, res))
                cnt += 1
                if w is None:
                    info = "flag:%s,up:%d,lo:%d,score:None" % (flag, up, lo)
                else:
                    info = "flag:%s,up:%d,lo:%d,score:%s" % (flag, up, lo, w)
                of.write("====\n%s\n\n" % (info))    
                kr=list(res.keys())
                kr.sort()
                bu=defaultdict(list)
                bldict={}
                for r in kr:
                    s = r[0:3]
                    c = Counter([a[0][0:3] for a in res[r]])
                    other = sum([a[1] for a in c.items() if a[0] != s])
                    bu[s].append((c[s], other))
                    bldict[r] = "%2.2d / %2.2d" % (c[s], other)
                for r in kr:
                    # should integrate the following table here!
                    rx=["%s:%s" % (a[0], k.krp_names[a[0]]) for a in res[r]]
                    #ofh.write("%s\t%s\t%s\t%s\n" % (r, k.krp_names[r], bldict[r], ",".join(rx[0:5])))
                    ofh.write("<tr><td>%s %s</td><td>%s</td><td>%s</td></tr>\n" % (r, k.krp_names[r], bldict[r], ",".join(rx[0:5])))
                #of.write("\n==Self/other\n")
                ofh.write("</table></body></html>")
                ofh.close()
                of.write("\n==s/o, bu\n")
                bs=list(bu.keys())
                bs.sort()
                for b in bs:
                    of.write("%s\t%d\t%d\t%s\n" % (b, sum([a[0] for a in bu[b]]), sum([a[1] for a in bu[b]]), info))
    of.close() 

