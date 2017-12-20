from flask import Flask
from flask import url_for, render_template, request, redirect
from bs4 import BeautifulSoup
from pymystem3.mystem import Mystem
import re
import urllib.request
import requests

app = Flask(__name__)

@app.route('/')
def index():
	info = get_skopje_info()
	return render_template('index.html', skopje=info)

def download_page(pageUrl, enc='utf-8'):
    text = ""
    try:
        page = urllib.request.urlopen(pageUrl)
        text = page.read().decode(enc)
        print("Success at: ", pageUrl)
    except:
        print('Error at', pageUrl)
    return text


def mystem(word):
    cont = Mystem(disambiguation=False)
    result = Mystem.analyze(cont, word)
    return result

def get_skopje_info():
    fulltext = download_page("https://www.gismeteo.ru/weather-skopje-3253/now/")
    m = re.search(r'<span class=\"js_value tab-weather__value_l\">\s(.*?)<span class=\"tab-weather__value_m\">(.*?)</span>', fulltext, flags=re.DOTALL)
    cel = m.group(1)
    drob = m.group(2)
    skopje = cel.replace('&minus;', '-') + drob + ' °C'
    return skopje


def parse_dict(page, word):
    try:
        m = re.search(r'<td class=\".*?\"><font color=\".*?\">(.*?)</font></td>.*?<td class=\".*?\"><font color=\".*?\">(.*?)</font>(.{1,}?) .*?', page ,flags=re.DOTALL)
        m1 = re.search(r'Предположен&#1110;е:.*?><b.*?>(.*?)<\/b><\/span> \(скор&#1123;е всего, такъ и пишется\)\.</span>', page ,flags=re.DOTALL)
        print(m)
        print(m1)
        if m:
            old = m.group(2) + m.group(3)
        elif not m:
            old = m1.group(1)
        print(old.strip(","))
    except AttributeError:
        old = change_ortho(word)
    return old.strip(",").replace("\'","")


def get_news():
        page = download_page('https://snob.ru')
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.get_text()
        rus = re.findall('[А-ЯЁа-яё ]{2,}', text)
        mas = []
        for word in rus:
            word = word.strip()
            if len(word.split(' ')) > 3:
                mas.append(word)
        rus = ' '.join(mas)
        print(rus)
        print(mas)
        return mas[30:50:2]

@app.route('/news')
def news():
    new = each_word(get_news())
    return render_template('news.html', news=new)

def gram_change(text, gr, lex):
    print(text,gr)
    if (gr.split(',')[0] == 'S' or gr.split(',')[0] == 'SPRO') and (('дат'in gr) or ('пр' in gr)) and (text[-1:] == 'е'):
        a = list(text)
        a[-1:] = 'ѣ'
        res = ''.join(a)
    else:
        res = text
    return res

def requ(word):
    headers = {
        "Host": "www.dorev.ru",
        "Cookie": "XMMGETHOSTBYADDR213134210163=U1%3A+163.210.unused-addr.ncport.ru; XMMcms4siteUSER=1; XMMFREE=YES; XMMPOLLCOOKIE=XMMPOLLCOOKIE",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
    }
    res = requests.get('http://www.dorev.ru/ru-index.html?s=' + urllib.parse.quote(word.encode("windows-1251")), headers=headers)
    page = res.text
    return page


def bez(list):
    list[2] = 'з'
    return list

def each_word(liste):
    newmas = []
    for e in liste:
        newel = []
        nliste = e.split(' ')
        for i in nliste:
            i = change_ortho(i)
            newel.append(i)
        newstr = ' '.join(newel)
        newmas.append(newstr)
    print(newmas)
    return newmas

def change_ortho(word):
    stem = mystem(word)
    stem0 = stem[0]
    print(stem0)
    if 'analysis' in stem0:
        result = gram_change(stem0['text'], stem0['analysis'][0]['gr'], stem0['analysis'][0]['lex'])
    else:
        result = stem0['text']
    liste = list(result)
    cons = 'бвгжзклмнпрстфхцчшщБВГЖЗКЛМНПРСТФХЦЧШЩ'
    vowj = 'аеёиоуэюяйАЕЁИОУЭЮЯЙ'
    if liste[len(liste)-1] in cons:
        liste.append('ъ')
    if liste[1:3] == ['б','е','c']:
        bez(liste)
    for i in range(len(liste)):
        if i != len(liste)-1 and (liste[i] == 'и' ) and (liste[i+1] in vowj):
            liste[i] = 'i'
    result = ''.join(liste)
    return result

@app.route('/results')
def word_changed():
    if request.method == 'GET':
        word = request.args.get('word')

        page = requ(word)
        old = parse_dict(page, word)
    with open("templates/doref.html", "w", encoding="utf-8") as f:
        f.write(old)
    return render_template('results.html', doref=old)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/tres')
def tres():
    answ = {'bread':'1', 'grand':'1','zenit':'1','tower':'1','leo':'0','mesh':'1','mess':'1','tender':'1','nut':'0','peg':'1'}
    get = {}
    k = 0
    if request.method == 'GET':
        for el in answ.keys():
            get[el] = request.args.get(el)
    for i in answ.keys():
        if answ[i] == get[i]:
            k += 1
    return render_template('tres.html', res=k)

if __name__ == '__main__':
    app.run(debug=True)