import math


def create_dict(filepath):
    dic = {}
    with open(filepath, 'r', encoding='gbk') as f:
        for k in f.readlines():
            k = k.strip().split()
            if len(k) == 0: continue
            dic[k[0]] = int(k[1])
            for i in range(len(k[0])):
                prefix = k[0][:i+1]
                if prefix not in dic: dic[prefix] = 0
    return dic

def create_DAG(line, dic):
    DAG = {}
    n = len(line)
    for i in range(n):
        temp = []
        k = i
        word = line[k]
        while k<n and word in dic:
            if dic[word] != 0: temp.append(k)
            k+=1
            word = line[i:k+1]
        if not temp: temp.append(i)
        DAG[i] = temp
    return DAG

def search(line, DAG, dic, logtotal):
    n = len(line)
    route = [None]*(n+1)
    route[n] = (0, 0)
    for idx in range(n-1, -1, -1):
        route[idx] = max((math.log(dic.get(line[idx:x+1]) or 1) - logtotal + route[x+1][0], x) for x in DAG[idx])
    return route