import random
from pymorphy2 import MorphAnalyzer
import json
import tweepy
import os
consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

morph = MorphAnalyzer()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

pnct = [",",".",":",";","\"","-", " ", "?", "!", "\n"]
patterns = [1, 2, 3]

def syllen(word):
    vowels = ["а", "о", "у", "ы", "и", "е", "ё", "ю", "я", "э"]
    leng = 0
    for symbol in word:
        if symbol in vowels:
            leng += 1
    return leng

def find_best_score(ana_list):
    min = 0.0
    best_i = 0
    for i in range(len(ana_list)):
        if ana_list[i].score > min:
            best_i = i
    return ana_list[best_i]

def find_needed_score(ana_list, tag):
    for el in ana_list:
        if str(el.tag) == tag:
            return el
        else:
            return find_best_score(ana_list)



def form_dict():
    mass_dict = []
    ignore = ["Abbr", "Name", "Surn", "Patr", "Geox", "Orgn", "Trad", "Subx", "Infr", "Slng", "Arch", "Litr", "Erro", "Dist", "Anph", "Dmns", "Prnt", "Init", "LATN", "PNCT", "NUMB", "ROMN", "UNKN"]
    with open("full_dict.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for word in lines[5000:100000]:
            anel = {}
            ana = find_best_score(morph.parse(word.strip()))
            fl = 0
            for ign in ignore:
                if ign in ana.tag:
                    fl = 1
                    break
            if fl == 0:
                anel['tag'] = str(ana.tag)
                anel['lemma'] = str(ana.normal_form)
                anel['word'] = str(ana.word)
                mass_dict.append(anel)
                print(anel)
    with open("dict.json", "w", encoding="utf-8") as f1:
        json.dump(mass_dict, f1)
    with open("dict.txt", "w", encoding="utf-8") as f5:
        f5.writelines(str(mass_dict))

#form_dict()
def load_dict():
    with open("dict.json", "r", encoding="utf-8") as f2:
        main_dict = json.load(f2)
    return main_dict

main_dict = load_dict()

def punct():
    return random.choice(["...", "."])



def infl(lemma, gram):
    forma = find_best_score(morph.parse(lemma))
    return forma.inflect(gram)

def make_verse(p, leng):
    flag = 0
    rdict = {}

    sres = ""
    for el in p:
        poss_lems = []
        for i in main_dict:
            pair = {}
            if list(el)[0] in i['tag']:
                pair[i['lemma']] = i['tag']
                poss_lems.append(pair)
        rdict[list(el)[0]] = poss_lems
    while syllen(sres) != leng:
        res = []
        for el in p:
            try:
                par = random.choice(rdict[list(el)[0]])
                lem = list(par)[0]
                while check_restrictions(find_needed_score(morph.parse(lem),par[lem]).tag, el[list(el)[0]]) != 0:
                    par = random.choice(rdict[list(el)[0]])
                    lem = list(par)[0]
                res.append(infl(lem, el[list(el)[0]]).word)

            except AttributeError:
                res.append("")
                print("\""+lem+"\"", find_needed_score(morph.parse(lem), par[lem]).tag, el[list(el)[0]])
            sres = " ".join(res)
    return sres

def compile_verse(p, masslen, pt):
    res_verse = []
    better_verse = []
    if pt == 'p':
        for l in range(len(p)):
            res_verse.append(make_verse(p[l], masslen[l]))
        better_verse.append(res_verse[0].capitalize())
        better_verse.append(res_verse[1].capitalize() + punct())
        better_verse.append(res_verse[2].capitalize() + punct())
        hajku = "\n".join(better_verse)
    if pt == 'p1':
        for l in range(len(p)):
            res_verse.append(make_verse(p[l], masslen[l]))
        better_verse.append(res_verse[0].capitalize() + punct())
        better_verse.append('Как ' + res_verse[1])
        better_verse.append(res_verse[2].capitalize() + punct())
        hajku = "\n".join(better_verse)
    if pt == 'p2':
        for l in range(len(p)):
            res_verse.append(make_verse(p[l], masslen[l]))
        better_verse.append(res_verse[0].capitalize())
        better_verse.append(res_verse[1].capitalize() + punct())
        better_verse.append(res_verse[2].replace(" ", " как ").capitalize() + punct())
        hajku = "\n".join(better_verse)
    return hajku

def check_restrictions(tag, gram):
    restr = [{'plur':{'Sgtm', 'PRED', 'ADVB', 'CONJ', 'INTJ', 'UNKN', 'PRCL'}}, {'sing':{'Pltm', 'PRED', 'ADVB', 'CONJ', 'INTJ', 'UNKN','PRCL'}}, {'pres': {'Impe', 'Impx', 'NOUN', 'UNKN', 'tran', 'perf'}}, {'femn': {'NOUN'}}, {'masc': {'NOUN'}}, {'neut': {'NOUN'}}]
    for item in restr:
        if list(item)[0] in gram:
            for item2 in item[list(item)[0]]:
                if item2 in tag:
                    return -1
    return 0

def generate():
    pat = ['p', 'p1', 'p2']

    p = [[{'VERB,impf,intr': {'plur', 'pres', '3per'}}, {'NOUN': {'plur', 'nomn'}}],
         [{'ADJF': {'sing', 'ablt', 'femn'}}, {'NOUN,inan,femn': {'sing', 'ablt'}}],
         [{'ADJF': {'sing', 'nomn', 'masc'}}, {'NOUN,inan,masc': {'sing', 'nomn'}}]]

    p1 = [[{'ADJF': {'plur', 'nomn'}}, {'NOUN': {'plur', 'nomn'}}],
         [{'NOUN': {'plur', 'nomn'}}, {'NOUN': {'sing', 'gent'}}, {'impf,intr': {'plur', 'pres', '3per'}}],
         [{'NOUN': {'plur', 'nomn'}}, {'NOUN': {'plur', 'gent'}}]]

    p2 = [[{'NOUN,inan,masc': {'sing', 'nomn'}}, {'ADJF': {'sing', 'gent', 'masc'}}],
         [{'NOUN,inan,masc': {'sing', 'gent'}}, {'ADJF': {'sing', 'gent','femn'}}, {'NOUN,inan,femn': {'sing', 'gent'}}],
         [{'impf,intr': {'sing', 'pres', '3per'}}, {'NOUN': {'sing', 'nomn'}}]]
    masslen = [5, 7, 5]
    masslen1 = [5, 6, 5]
    masslen2 = [5, 7, 4]

    pt = random.choice(pat)
    if pt == 'p':
        return compile_verse(p, masslen, pt)
    if pt == 'p1':
        return compile_verse(p1, masslen1, pt)
    if pt == 'p2':
        return compile_verse(p2, masslen2, pt)


def main():
    tweet = generate()
    api.update_status(tweet)






