#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json
from datetime import timedelta, date
from time import sleep
import threading

from telegram.ext import (Updater, CommandHandler)
from src.data.API import API_KEY
from src.model.user import User

# Enable logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

db = None
turn_list = {
        "index": 0,
        "current_owner": None,
        "list": [User('Ile', 0), User('Silve', 0), User('Khadim', 0), User('Dani', 0), User('Matti', 0), User('Pagge', 0), User('Albi', 958468633)]
    }

#####################################################################################################
def next_turn():
    global db, turn_list
    if turn_list['index'] >= len(turn_list['list'])-1:
        turn_list['index'] = 0
    else:
        turn_list['index'] += 1
    turn_list['current_owner'] = turn_list['list'][turn_list['index']]
    album = {
        "turn": db[-1]['turn']+1,
        "owner": turn_list['current_owner'],
        "init_date": date.today().strptime("%d/%m/%y"),
        "end_date": date.today().strptime("%d/%m/%y") + timedelta(days=7),
        "album_link": "",
        "score": []
    }
    db.append(album)
    update_db()

def week_cicle():
    while True:
        if date.today().strptime("%d/%m/%y") = db[-1]['end_date']
            next_turn()
        sleep(86000)

def load_db():
    with open('src/data/db.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())

def update_db():
    with open('src/data/db.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def start(update, context):
    load_db()
    for t in turn_list['list']:
        if db[-1]['owner'] = t.id:
            global turn_list
            turn_list['curret_owner'] = t
            turn_list['index'] = turn_list['list'].index(turn_list['curret_owner'])
            update.message.reply_text(f"è il turno di {turn_list['curret_owner'].name}")

def help_command(update, context):
    update.message.reply_text(f"{update.message.from.id} --> {update.message.from.username}")

def add_album(update, context):
    if update.message.from.id = turn_list['current_owner'].id:
        global db
        db[-1]['album_link'] = update.message.text.split(' ')[1]
        update_db()
        update.message.reply_text('Album aggiunto!')
    else:
        update.message.reply_text('Non è il tuo turno coglione')

def info_current(update, context):
    avg = sum(int(r['voto']) for r in db[-1]['score']) / len(db[-1]['score'])
    text = f"Turno N. {db[-1]['turn']}\nUser {db[-1]['owner']}\nData di inizio {db[-1]['init_date']}\nLink {db[-1]['album_link']}\nMedia dei voti {avg}"
    update.message.reply_text(text)
        
def vote_current(update, context):
    for t in turn_list['list']:
        if t.id = update.message.from.id
            global db
            db[-1]['score'].append({"user":t.user, "id": t.id, "voto": int(update.message.text.split(' ')[1])})
            update_db()
            update.message.reply_text(f"{t.user} ha dato come voto {int(update.message.text.split(' ')[1])} all'album")
            return

def main():
    global db
    db = load_db()
    updater = Updater(API_KEY)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("aggiungi_album", add_album))
    dispatcher.add_handler(CommandHandler("info_album", info_current))
    dispatcher.add_handler(CommandHandler("vota_album_corrente", vote_current))
    x = threading.Thread(target=week_cicle, args=(,))
    x.start()
    updater.start_polling()
    updater.idle()
    x.join()

if __name__ == "__main__":
    main()