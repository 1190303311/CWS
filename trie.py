from tqdm import tqdm
from queue import Queue

class TrieNode:
    # list实现的前缀树，主要代码参考了PPT
    def __init__(self, character, terminal, children) -> None:
        self.character = character
        self.terminal = terminal
        self.children = children

    def is_terminal(self):
        return self.terminal

    def set_terminal(self, terminal):
        self.terminal = terminal

    def get_character(self):
        return self.character

    def set_character(self, character):
        self.character = character

    def get_children(self):
        return self.children

    def get_child(self, character):
        for k in self.children:
            if k.character == character: return k
        return None

    def get_child_if_not_exist_then_create(self, character):
        child = self.get_child(character)
        if not child:
            child = TrieNode(character, False, [])
            self.add_child(child)
        return child
    
    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        n = len(self.children)
        for i in range(n):
            if self.children[i].character == child.character:
                del self.children[i]


class myDict:
    #哈希实现
    def __init__(self, dict) -> None:
        self.dict = [None] * 100000
        self.create(dict)

    def get_idx(self, word):
        idx = 0
        for c in word: idx += ord(c)
        return idx % 100000

    def create(self, dict):
        for word in dict:
            idx = self.get_idx(word)
            item = self.dict[idx]
            if item == None: self.dict[idx] = [word]
            if type(item) == list: self.dict[idx].append(word)
    
    def find(self, word):
        idx = self.get_idx(word)
        item = self.dict[idx]
        if item == None: return False
        else:
            for k in item:
                if word == k: return True
        return False


def contain(astr, root):
    astr = astr.replace(' ', '')
    if len(astr) < 1: return False
    node = root
    for i in astr:
        child = node.get_child(i)
        if not child: return False
        else: node = child
    return node.is_terminal()

def add(word, root):
    word = word.replace(' ', '')
    if len(word) < 1: return
    node = root
    for i in word:
        child = node.get_child_if_not_exist_then_create(i)
        node = child
    node.set_terminal(True)

def add_all(word_list):
    root = TrieNode('#', False, [])
    for word in word_list: add(word, root)
    return root