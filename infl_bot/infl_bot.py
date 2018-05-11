import json
import os
import random
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()


def form_dict():
    mass_dict = []
    with open("full_dict.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for word in lines[1:100000]:
            anel = {}
            ana = find_best_score(morph.parse(word.strip()))
            anel['tag'] = str(ana.tag)
            anel['lemma'] = str(ana.normal_form)
            anel['word'] = str(ana.word)
            mass_dict.append(anel)
            print(anel)
    with open("dict.json", "w", encoding="utf-8") as f1:
        json.dump(mass_dict, f1)

def load_dict():
    with open("dict.json", "r", encoding="utf-8") as f2:
        main_dict = json.load(f2)
    return main_dict

main_dict = load_dict()

def find_best_score(ana_list):
    min = 0.0
    best_i = 0
    for i in range(len(ana_list)):
        if ana_list[i].score > min:
            best_i = i
    return ana_list[best_i]

def get_inp():
    text = input()
    words = text.split()
    massinp = []
    for el in words:
        aneli = {}
        ana = find_best_score(morph.parse(el))
        print(ana)
        aneli['tag'] = str(ana.tag)
        aneli['lemma'] = str(ana.normal_form)
        aneli['word'] = str(ana.word)
        massinp.append(aneli)
    return massinp



def interchange():
    res = []
    massinp = get_inp()
    for el in massinp:
        poss_words = []
        tag = el['tag']
        for i in main_dict:
            if i['tag'] == tag:
                poss_words.append(i['word'])
        print(poss_words)
        word = random.choice(poss_words)
        res.append(word)
    sres = " ".join(res)
    return sres

#form_dict()
print(interchange())

