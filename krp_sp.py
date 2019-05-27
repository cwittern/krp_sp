#  -*- coding: utf-8 -*-
import sys, os, codecs
import sentencepiece as spm
from random import sample

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


def makemodels(vsize='30000'):
    cdir="%s/data" % (sp_path)
    cs=[a for a in os.listdir(cdir) if a.endswith(".txt")]
    cs.sort()
    for c in cs:
        corpus="%s/%s" % (cdir, c)
        if c.startswith("krp"):
            flag="m0"
        elif len(c) == 7:
            flag="m1"
        else:
            flag="m2"
        cml='--input=%s --model_prefix=model/%s-%s-%s --vocab_size=%s' % (corpus, flag, c.replace(".txt", ""), vsize, vsize)
        print (cml)
        try:
            spm.SentencePieceTrainer.train(cml)
        except:
            print("ERROR: ", c)
            

def loadvoc(model, log=False):
    v = model.replace(".model", ".vocab")
    pas = "%s/model/%s" % (sp_path, v) 
    l=[]
    for line in codecs.open(pas, "r", "utf-8").readlines():
        # # use the log value as float
        if log:
            ln = float(line[:-1].split("\t")[1])
        else:
            ln = line[:-1].split("\t")[0]
        l.append(ln)
    return l


def loadmodels(flag="m2", log=False, use_krp_names=True):
    """Loads the model identified with the flag.  Returns a triple with a list of names, a list of models and a list of vocabulary."""
    mdir = "%s/model" % (sp_path) 
    mdir="model"
    ms=[a for a in os.listdir(mdir) if a.endswith("model") and a.startswith(flag)]
    ms.sort()
    len(ms) 
    md=[]
    mv=[]
    for m in ms:
        sp = spm.SentencePieceProcessor()
        vl = loadvoc(m, log)
        mv.append(vl)
        sp.load("%s/%s" % (mdir, m))
        md.append(sp)
    if use_krp_names:
        mn=[krp_names[a.split("-")[1]] for a in ms]
    else:
        mn=[a.split("-")[1] for a in ms]
    return (mn, md, mv)

def loadsamples(cnt=5, length=100):
    """Load random samples from the corpus files.  Returns a tuple with list of names and a list of a list of samples. """
    cdir="%s/data" % (sp_path)
    ss=[]
    cs=[a for a in os.listdir(cdir) if a.endswith(".txt")]
    if len(cs) == 0:
        import json
        with open('data/sample_data.json') as json_file:  
            data = json.load(json_file)        
        return data    
    else:
        cs.sort()
        for c in cs:
            sl=[]
            corpus="%s/%s" % (cdir, c)        
            ls = codecs.open(corpus, "r", "utf-8").read()
            for s in sample(range(len(ls) - length), cnt):
                end = s + length
                sstr = ls[s:end]
                sstr = sstr.replace("\n", "")
                sl.append(sstr)
            ss.append(sl)
        mn=[krp_names[a.split(".")[0]] for a in cs]
        return list(zip(mn, ss))
                      
def getbest(md, sntc, mv=None, cnt=3):
    """Get the best result for the sentence provided. Optionally, return cnt results. md is the loaded list of models. Optionally provide a list with log values in mv."""
    res=[]
    for i, mx in enumerate(md):
        ids = mx.encode_as_ids(sntc)
        if mv:
            r = sum([mv[i][a] for a in ids]) / len(ids)
        else:
            r = sum(ids) / len(ids)
        res.append((i, r))
    if mv:
        resx=sorted(res, key=lambda x: x[1], reverse=True)
    else:
        resx=sorted(res, key=lambda x: x[1])
    return [a[0] for a in resx[0:cnt]]
    


#makemodels()


    
    
