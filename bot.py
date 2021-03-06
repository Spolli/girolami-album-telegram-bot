#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from datetime import timedelta, date
from time import sleep

import telepot
from telepot.loop import MessageLoop
from src.data.API import API_KEY, turn_list
from src.model.user import User
from src.model.utility_json import load_json, update_json, append_obj

db = None
bot = None
users = None
#####################################################################################################

def register(msg):
    global users
    name = msg['text'].split(' ')[1]
    id = msg['from']['id']
    for usr in users:
        if usr['id'] == id:
            bot.sendMessage(msg['chat']['id'], f"Utente {name} già registrato!")
            return
    user = {
        'index': 0,
        'name': name,
        'id': id
    }
    users.append(user)
    append_obj('src/data/users.json', user)
    bot.sendMessage(msg['chat']['id'], f"Utente {user['name']} registrato!")

def not_yet_vote():
    not_voted = []
    for u in users:
        for d in db[-1]['score']:
            if not u['id'] == d['id']:
                not_voted.append(u['name'])
    return not_voted

def get_usr_by_id(id):
    for t in users:
        if t['id'] == id:
            return t

def check_if_voted(id):
    for sc in db[-1]['score']:
        if id == sc['id']:
            return True
    return False

def next_turn():
    global db, turn_list
    if turn_list['current_owner']['index'] >= len(users)-1:
        turn_list['current_owner'] = users[0]
        #TODO classifica di fine giro
    else:
        turn_list['current_owner'] = users[users.index(turn_list['current_owner']) + 1]
    album = {
        "turn": db[-1]['turn']+1,
        "owner": turn_list['current_owner']['name'],
        "owner_id": turn_list['current_owner']['id'],
        "init_date": date.utctoday().strptime("%d/%m/%y"),
        "end_date": date.utctoday().strptime("%d/%m/%y") + timedelta(days=7),
        "album_link": "",
        "score": []
    }
    db.append(album)
    append_obj('src/data/db.json', album)

def start(msg):
    global turn_list
    for t in users:
        if db[-1]['owner_id'] == t['id'] and not date.utctoday().strptime("%d/%m/%y") < db[-1]['end_date']: #TODO migliorare il confronto tra date
            turn_list['curret_owner'] = t
            bot.sendMessage(msg['chat']['id'], f"è il turno di {t['name']}")
        else:
            next_turn()

def help_command(msg):
    txt = """
        La sintassi per usare i comandi del bot sono: comando parametro (ex. /vote_current 6)
        /start --> fai partire il bot\n
        /help --> info sul bot\n
        /add_album_link --> L'utente che è di turno nella settimana aggiunge il link dell'album\n
        /info_current --> informazioni sull'album della settimana\n
        /vote_current --> vota l'album corrente
        /register --> registra nuovo partecipante
        """
    bot.sendMessage(msg['chat']['id'], txt)

def add_album_link(param):
    if msg['from']['id'] == turn_list['current_owner']['id']:
        global db
        db[-1]['album_link'] = msg['text'].split(' ')[1]
        update_json('src/data/db.json', db)
        bot.sendMessage(msg['chat']['id'], 'Album aggiunto!')
    else:
        bot.sendMessage(msg['chat']['id'], 'Non è il tuo turno coglione')

def info_current(msg):
    avg = sum(int(r['voto']) for r in db[-1]['score']) / len(db[-1]['score'])
    text = f"""
Turno N. \t{db[-1]['turn']}
User: \t{db[-1]['owner']}
Data di inizio: \t{db[-1]['init_date']}
Data di fine: \t{db[-1]['end_date']}
Media dei voti: \t{avg}
Devono ancora votare: \t{', '.join(not_yet_vote())}\n
Link: \t{db[-1]['album_link']}
    """
    bot.sendMessage(msg['chat']['id'], text)
        
def vote_current(msg):
    try:
        if not check_if_voted(msg['from']['id']):
                global db
                usr = get_usr_by_id(msg['from']['id'])
                db[-1]['score'].append({
                    "user":usr['name'], 
                    "id": usr['id'], 
                    "voto": int(msg['text'].split(' ')[1])
                    })
                update_json('src/data/db.json', db)
                bot.sendMessage(msg['chat']['id'], f"{usr['name']} ha dato come voto {int(msg['text'].split(' ')[1])} all'album")
                return
        else:
            bot.sendMessage(msg['chat']['id'], "Hai già votato questo album coglione")
    except Exception:
        bot.sendMessage(msg['chat']['id'], "Hai sbagliato l'input coglione")

def skip_turn(msg):
    bot.sendMessage(msg['chat']['id'], f"{db[-1]['owner']} ha saltato il turno")
    next_turn()

def handle(msg):
    if msg['text'][0] == '/':
        cmd = msg['text'].split(' ')[0]
        if cmd == "/start": start(msg)
        elif cmd == "/help": help_command(msg)
        elif cmd == "/add_album": add_album_link(msg)
        elif cmd == "/info_current": info_current(msg)
        elif cmd == "/vote_current": vote_current(msg)
        elif cmd == "/skip_turn": skip_turn(msg)
        elif cmd == "/register": register(msg)
        else: 
            bot.sendMessage(msg['chat']['id'], "Comando non valido!")

def main():
    global db, bot, users
    db = load_json('src/data/db.json')
    users = load_json('src/data/users.json')
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