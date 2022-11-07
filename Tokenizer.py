import codecs
from tqdm import tqdm
import time
import math
import os
from trie import add_all, contain, myDict
from utils import create_dict, create_DAG, search

def read_text(filepath):
    f = codecs.open(filepath, 'r', 'gbk')
    text = f.readlines()
    f.close()
    return text

def read_dic(filepath):
    dic = []
    maxlen = 0
    f = codecs.open(filepath, 'r', encoding='gbk')
    for k in f.readlines():
        k = k.strip().split(' ')
        dic.append(k[0])
        if(len(k[0]) > maxlen):maxlen = len(k[0])
    f.close()
    return (dic, maxlen)

def create_trie(dic):
    return add_all(dic)

def FMM_list(text, maxlen=0, dic=None, root=None):
    seglist = []
    while len(text) > 0:
        length = maxlen
        if len(text) < maxlen: length = len(text)
        tryword = text[0:length]
        while tryword not in dic:
            if len(tryword)==1: break
            tryword = tryword[0:-1]
        seglist.append(tryword)
        text = text[len(tryword):]
    return seglist

def FMM(text, maxlen=0, dic=None, root=None):
    seglist = []
    while len(text) > 0:
        length = maxlen
        if len(text) < maxlen: length = len(text)
        tryword = text[0:length]
        #while not contain(tryword,root):
        while not dic.find(tryword):
            if len(tryword)==1: break
            tryword = tryword[0:-1]
        seglist.append(tryword)
        text = text[len(tryword):]
    return seglist

def BMM(text, maxlen=0, dic=None, root=None):
    seglist = []
    while len(text) > 0:
        length = maxlen
        if len(text) < maxlen: length = len(text)
        tryword = text[len(text)-length:]
        #while not contain(tryword,root):
        while not dic.find(tryword):
            if len(tryword)==1: break
            tryword = tryword[1:]
        seglist.insert(0, tryword)
        text = text[:len(text)-len(tryword)]
    return seglist

def one_gram_tokenizer(text, maxlen=0, dic=None, root=None):
    DAG = create_DAG(text, dic)
    route = search(text, DAG, dic, logtotal=maxlen)
    seglist = []
    i=0
    j = route[i][1]
    while i<len(text):
        seglist.append(text[i:j+1])
        i = j+1
        j = route[i][1]
    return seglist


def tokenize(filepath, dicpath, savepath, method='FMM'):
    text = read_text(filepath)
    root = None
    dic = None
    maxlen = 0
    if method == 'FMM':                      # FMM 
        tokenizer = FMM
        dict, maxlen = read_dic(dicpath)
        #root = create_trie(dic)             #list实现的前缀树，主体代码参考了PPT
        dic = myDict(dict)                   #哈希实现
    if method == 'BMM': 
        tokenizer = BMM
        dict, maxlen = read_dic(dicpath)
        #root = create_trie(dic)
        dic = myDict(dict)
    if method == 'gram':                     #一元文法分词，主题代码参考了PPT
        tokenizer = one_gram_tokenizer
        dic = create_dict(dicpath)
        maxlen = math.log(sum(dic.values()))
    if method == 'list':                     #最简单的纯使用list搜索
        tokenizer = FMM_list
        dic, maxlen = read_dic(dicpath)
    print('tokenizing with {}'.format(method))
    with open(savepath, 'w', encoding='gbk') as f:
        for line in tqdm(text):
            line_seg = tokenizer(line.strip(), maxlen=maxlen, dic=dic, root=root)
            for k in line_seg: f.write(k + '/' + ' ')
            f.write('\n')

if __name__=='__main__':
    filepath = '/home/u1190303311/NLP/expr-1/199801_sent.txt'
    dicpath = './dic.txt'
    savepath = '/home/u1190303311/NLP/expr-1/'
    #t = time.time()
    #tokenize(filepath, dicpath, os.path.join(savepath, 'seg_FMM0.txt'), method='list')
    #tf1 = str(time.time()-t)

    t = time.time()
    tokenize(filepath, dicpath, os.path.join(savepath, 'seg_FMM_test.txt'), method='FMM')
    tf2 = str(time.time()-t)

    t = time.time()
    tokenize(filepath, dicpath, os.path.join(savepath, 'seg_BMM_test.txt'), method='BMM')
    tb2 = str(time.time()-t)

    tokenize(filepath, dicpath, os.path.join(savepath, 'seg_LM_test.txt'), method='gram')
    #with open('./data/TimeCost.txt', 'w') as f:
        #f.write('seg_FMM.txt: \n')
        #f.write('Before optimization: ' + tf1 + '\n')
        #f.write('After optimization: ' + tf2)
