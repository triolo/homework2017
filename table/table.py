import sqlite3

source = sqlite3.connect('hittite.db')
curses = source.cursor()
goal = sqlite3.connect('goal.db')

curseg = goal.cursor()

curseg.execute("CREATE TABLE words(Idw INTEGER PRIMARY KEY, Lemma TEXT, Wordform TEXT, Glosses TEXT);")
curseg.execute("CREATE TABLE glosses(Idg INTEGER PRIMARY KEY, Obozn TEXT, Rassh TEXT);")
curseg.execute("CREATE TABLE words_glosses (Id_word INTEGER, Id_gloss INTEGER);")


for row in curses.execute('SELECT Lemma, Wordform, Glosses FROM wordforms'):
    curseg.execute("""INSERT INTO words
(Lemma, Wordform, Glosses)
 VALUES (?, ?, ?);""", row)

with open("glosses.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
    mas = []
for el in lines:
    mas = el.strip().split(" — ")
    curseg.execute("""INSERT INTO glosses
    (Obozn, Rassh)
     VALUES (?, ?);""", (mas[0], mas[1]))

x = []
res = ''
for i, row in enumerate(curses.execute('SELECT Glosses FROM wordforms')):
    x = row[0].split(".")
    #print(x)
    for j in x:
        if j.isupper():
            res = curseg.execute('SELECT Idg FROM glosses WHERE Obozn=?', (j,))
            print(j)
            print(res)
            if res == None:
                curseg.execute('INSERT INTO glosses (Obozn) VALUES (?)', (j,))
            for row1 in curseg.execute('SELECT Idg FROM glosses WHERE Obozn=?', (j,)):
                curseg.execute('INSERT INTO words_glosses (Id_word, Id_gloss) VALUES (?, ?)',(i,row1[0]))
                print(row1)
        #print(row1)
#for row2 in curseg.execute('SELECT Id_word, Id_gloss FROM words_glosses'):
#print(row2)

goal.commit()