import json
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)
keys = ['man', 'woman', 'fire', 'nose']
nom = ''
prenom = ''
inform = []
syr = []
data = {}
pairs = {}
isk = ''
result = ''
ess = []


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stats', methods=['GET'])
def collect():
    newdata = []
    if request.method == 'GET':
        nom = request.args.get('nom')
        prenom = request.args.get('prenom')
        chiffre = nom + ' ' + prenom
        for item in keys:
            pairs[item] = request.args.get(item)
        data = {chiffre: pairs}
        with open("inform.json", "r", encoding="utf-8") as f:
            text = f.read()
            text = text.rstrip(']')
            strdata = str(data)
            strdata = list(strdata)
            for element in strdata:
                if element == "\'":
                    element = "\""
                newdata.append(element)
            newdata = ''.join(newdata)
            text = text + ', ' + newdata + ']'
        inform = json.loads(text)
    with open("inform.json", "w", encoding="utf-8") as f:
        json.dump(inform, f)
    return render_template('stats.html', pairs=pairs, keys=keys, informants=inform)


@app.route('/json')
def importation():
    with open("inform.json", "r", encoding="utf-8") as f1:
        dictionnaire = json.load(f1)
    return '<html><body><p>' + str(dictionnaire) + '</p><a href="/"> На главную </a> </body></html>'

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results', methods=['GET'])
def result():
    ess = []
    if request.method == 'GET':
        stim = request.args.get('stimulus')
        with open("inform.json", "r", encoding="utf-8") as f1:
            dictionnaire = json.load(f1)
        for element in dictionnaire:
            for name, data in element.items():
                if data[stim]:
                    ess.append(data[stim])
                    result = 'Найдено:'
                else:
                    result = 'Не найдено'
    return render_template('results.html', ess=ess, stim=stim, result=result)


if __name__ == '__main__':
    app.run(debug=True)