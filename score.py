import codecs
import re
from tqdm import tqdm


def read_output(filepath):
    f = open(filepath, 'r', encoding='gbk')
    lines = f.readlines()
    f.close()
    res = []
    for k in lines:
        k = k.strip().split()
        ls = []
        idx = 0
        for word in k:
            word = word.split('/')[0]
            ls.append((idx, idx+len(word)-1))
            idx = idx + len(word)
        res.append(ls)
    return res

def preprocess(filepath):
    f = codecs.open(filepath, 'r', encoding='gbk')
    lines = f.readlines()
    f.close()
    res = []
    for k in lines:
        k = k.strip().split()
        ls = []
        idx = 0
        for word in k:
            word = word.split('/')[0]
            ls.append((idx, idx+len(word)-1))
            idx = idx + len(word)
        res.append(ls)
    return res

def read_src(srcpath):
    f = codecs.open(srcpath, 'r', 'gbk')
    lines = f.readlines()
    f.close()
    res = []
    for k in lines: 
        k = k.strip()
        res.append(k)
    return res

def normalize(src, tgt):
    src = read_src(src)
    f = codecs.open(tgt, 'r', 'gbk')
    lines = f.readlines()
    f.close()
    with open('./refer.txt','w') as f:
        for i in range(len(lines)):
            line = lines[i].strip().split()
            length = 0
            for word in line:
                length += len(word.split('/')[0])
            if length != len(src[i]): 
                lines[i] = lines[i].replace('[', '')
            f.write(lines[i])

def score(truepath, outputpath):
    #normalize('./199801_sent.txt', truepath)
    hypo = read_output(outputpath)
    #refer = preprocess('./refer.txt')
    refer = preprocess(truepath)

    assert len(hypo) == len(refer)
    TP = 0
    FN = 0
    FP = 0
    TN = 0
    for i in tqdm(range(len(refer))):
        for word in hypo[i]:
            if word in refer[i]: TP+=1
            else: FP+=1
        for word in refer[i]:
            if word not in hypo[i]: FN+=1
    precision = (TP) / (TP+FP)
    recall = (TP) / (TP + FN)
    f1 = 2*precision*recall / (precision+recall)
    return (precision, recall, f1)

if __name__=='__main__':
    fp, fr, ff = score('./data/testy.txt', './data/seg_FMM_test.txt')
    bp, br, bf = score('./data/testy.txt', './data/seg_BMM_test.txt')
    lp, lr, lf = score('./data/testy.txt', './data/seg_LM_test.txt')
    with open('./data/score_test.txt', 'w') as f:
        f.write('FMM:' + '\n')
        f.write('precision: ' + str(fp) + '\n')
        f.write('recall: ' + str(fr) + '\n')
        f.write('f1 score: ' + str(ff) + '\n' + '\n')
        f.write('BMM:' + '\n')
        f.write('precision: ' + str(bp) + '\n')
        f.write('recall: ' + str(br) + '\n')
        f.write('f1 score: ' + str(bf) + '\n' + '\n')
        f.write('LM:' + '\n')
        f.write('precision: ' + str(lp) + '\n')
        f.write('recall: ' + str(lr) + '\n')
        f.write('f1 score: ' + str(lf) + '\n')