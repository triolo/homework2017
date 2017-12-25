import re
import json
from flask import Flask
from flask import url_for, render_template, request, redirect

app = Flask(__name__)

diction = {}
def open_file(i, j):
    try:
        s = "thai_pages/{0}.{1}.html".format(i, j)
        with open(s, "r", encoding="utf-8") as f:
            text = f.read()
            return text
    except FileNotFoundError:
        print("Not found")
        print(s)


def parse_text():
    for i in range(187, 206):
        for j in range(1, 100):
            text = open_file(i, j)
            if text:
                m = re.findall(r"<td class=th><a href='.*?'>(.*?)</a>.*?</td>.*?<td>.*?<td class=.*?</td><td>(.*?)</td>", text)
                # m = re.findall(r"<td class=th><a href='.*?'>(.*?)(<a.*?/>)?</a></td>.*?<td>.*?<td class=.*?</td><td>(.*?)</td>", text)
                for tup in m:
                    diction[tup[0]] = tup[1]
    #print(diction)
    write_into(diction)
    write_back(diction)
    return 0


def write_into(diction):
    with open ("thai_eng.json", "w", encoding="utf-8") as f1:
        json.dump(diction, f1, ensure_ascii=False)
    return 0


def write_back(diction):
    new_dict = {v: k for k, v in diction.items()}
    newest_dict = {}
    for key, el in new_dict.items():
        for i in key.split("; "):
            newest_dict[i] = el
    with open ("eng_thai.json", "w", encoding="utf-8") as f1:
        json.dump(newest_dict, f1, ensure_ascii=False)
    return 0


parse_text()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results")
def results():
    sdict = {}
    if request.method == 'GET':
            word = request.args.get("word")
    with open("eng_thai.json", "r", encoding="utf-8") as f2:
        sdict = json.load(f2)
    #print(sdict)
    value = sdict[word]
    with open("templates/compile.html", "w", encoding="utf-8") as f3:
        f3.write(value)
    return render_template("results.html")

if __name__ == '__main__':
    app.run(debug=True)