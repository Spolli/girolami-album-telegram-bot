#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import timedelta, date
from time import sleep

import telepot
from telepot.loop import MessageLoop
from src.data.API import API_KEY
from src.model.user import User

db = None
bot = None
turn_list = {
    "index": 0,
    "current_owner": None,
    "list": [User(0, 'Ile', 0), User(1, 'Silve', 0), User(2, 'Khadim', 0), User(3, 'Dani', 0), User(4, 'Matti', 0), User(5, 'Pagge', 0), User(6, 'Albi', 958468633)]
}
#####################################################################################################

def get_usr_by_id(id):
    for t in turn_list['list']:
        if t.id == id:
            return t

def check_if_voted(id):
    for sc in db[-1]['score']:
        if id == sc['id']
            return True
    return False

def next_turn():
    global db, turn_list
    if turn_list['index'] >= len(turn_list['list'])-1:
        turn_list['index'] = 0
        #TODO classifica di fine giro
    else:
        turn_list['index'] += 1
    turn_list['current_owner'] = turn_list['list'][turn_list['index']]
    album = {
        "turn": db[-1]['turn']+1,
        "owner": turn_list['current_owner'],
        "init_date": date.utctoday().strptime("%d/%m/%y"),
        "end_date": date.utctoday().strptime("%d/%m/%y") + timedelta(days=7),
        "album_link": "",
        "score": []
    }
    db.append(album)
    update_db()

def load_db():
    with open('src/data/db.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def update_db():
    with open('src/data/db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def start(msg):
    global turn_list
    load_db()
    for t in turn_list['list']:
        if db[-1]['owner'] == t.id:
            turn_list['curret_owner'] = t
            turn_list['index'] = turn_list['list'].index(turn_list['curret_owner'])
            bot.sendMessage(msg['chat']['id'], f"è il turno di {turn_list['curret_owner'].name}")

def help_command(msg):
    txt = """
        La sintassi per usare i comandi del bot sono: comando parametro (ex. /vote_current 6)
        /start --> fai partire il bot\n
        /help --> info sul bot\n
        /add_album_link --> L'utente che è di turno nella settimana aggiunge il link dell'album\n
        /info_current --> informazioni sull'album della settimana\n
        /vote_current --> vota l'album corrente
        """
    bot.sendMessage(msg['chat']['id'], f"{msg['from']['id']} --> {msg['from']['username']}")

def add_album_link(param):
    if msg['from']['id'] == turn_list['current_owner'].id:
        global db
        db[-1]['album_link'] = msg['text'].split(' ')[1]
        update_db()
        bot.sendMessage(msg['chat']['id'], 'Album aggiunto!')
    else:
        bot.sendMessage(msg['chat']['id'], 'Non è il tuo turno coglione')

def info_current(param):
    avg = sum(int(r['voto']) for r in db[-1]['score']) / len(db[-1]['score'])
    text = f"""
        Turno N. {db[-1]['turn']}\n
        User {db[-1]['owner']}\n
        Data di inizio {db[-1]['init_date']}\n
        Data di fine {db[-1]['end_date']}\n
        Link {db[-1]['album_link']}\n
        Media dei voti {avg}
    """
    bot.sendMessage(msg['chat']['id'], text)
        
def vote_current(msg):
    if not check_if_voted:
        try:
            global db
            usr = get_usr_by_id(msg['from']['id'])
            db[-1]['score'].append({"user":usr.user, "id": usr.id, "voto": int(msg['text'].split(' ')[1]})
            update_db()
            bot.sendMessage(msg['chat']['id'], f"{usr.user} ha dato come voto {int(msg['text'].split(' ')[1])} all'album")
            return
        except Exception e:
            bot.sendMessage(msg['chat']['id'], "Diocane Input sbagliato. Ma che sei handicappato?")
    else:
        bot.sendMessage(msg['chat']['id'], "Hai già votato questo album coglione")

def skip_turn(msg):
    usr = get_usr_by_id(msg['from']['id'])
    next_turn()
    bot.sendMessage(msg['chat']['id'], f"{usr.user} ha saltato il turno")

def handle(msg):
    if msg['text'][0] == '/':
        print(msg['from']['id'])
        opt = {
            "/start": start(msg),
            "/help": help_command(msg),
            "/add_album": add_album(msg),
            "/info_current": info_current(msg),
            "/vote_current": vote_current(msg),
            "/skip_turn": skip_turn(msg)
        }
        opt[cmd]

def main():
    global db, bot
    db = load_db()
    bot = telepot.Bot(API_KEY)
    MessageLoop(bot, handle).run_as_thread()
    while True:
        sleep(5)
        '''
        if datetime.strptime(db[-1]['end_date'], '%d/%m/%y') <= date.today().strptime("%d/%m/%y"):
            next_turn()
        sleep(86000)
        '''

if __name__ == "__main__":
    main()