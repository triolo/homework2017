import flask
import telebot
import conf
import json
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
    with open("/home/triolo/h_ling_bot/dict.json", "w", encoding="utf-8") as f1:
        json.dump(mass_dict, f1)

def load_dict():
    with open("/home/triolo/h_ling_bot/dict.json", "r", encoding="utf-8") as f2:
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

def get_inp(message):
    words = message.split()
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



def interchange(message):
    res = []
    massinp = get_inp(message)
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


WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN,
                      threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

app = flask.Flask(__name__)


# этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте! Это бот, который меняет слова в вашем сообщении.")


@bot.message_handler(func=lambda m: True)  # этот обработчик реагирует все прочие сообщения
def send_len(message):
    bot.send_message(message.chat.id, interchange(message.text))


# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)