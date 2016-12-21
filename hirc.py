import os
import sys
import time
import threading
import irc_bot_noblock
from datetime import datetime

# change it to your own
# get your oauth here: https://twitchapps.com/tmi/
nickname = 'twitch_plays_3ds'
oauth = 'oauth:qmdwk3rsm4qau59zf2dpxixsf4wxzf'

def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        print("creating directory " + dir_path)
        os.makedirs(dir_path)

def worker():
    global last_message
    while 1:
        last_message = input()
        time.sleep(0.1)

def log_msg(name, msg):
    msg = msg.replace('\r', '').replace('\n', '')
    with open('./comment_log/' + chat_channel + ".txt", mode='a', encoding='utf-8') as log_file:
        log_file.write(datetime.utcnow().isoformat(sep='T') + "Z " + name + ': ' + msg + '\r\n')

if(len(sys.argv) != 2):
    print (__file__ + ' chat_channel')
    exit()

ensure_dir('./comment_log')
last_message = ''
chat_channel = sys.argv[1].lower().lstrip().rstrip()
chat_server = ['irc.chat.twitch.tv', 6667]

bot = irc_bot_noblock.irc_bot(nickname, oauth, chat_channel, chat_server[0], chat_server[1], timeout=300)
bot.connect()

t = threading.Thread(target=worker)
t.start()

while 1:
    tmi_list = bot.get_parsed_message()
    tmi_list.reverse()
    for item in [x for x in tmi_list if "." not in x.username]:
        message_orig = item.message.replace(chr(1) + "ACTION", "/me").replace(chr(1), '').lstrip().rstrip()
        log_msg(item.username, message_orig)
        print(item.username + ": " + message_orig)

    if last_message != '':
        print("\n\t>> " + nickname + ": " + last_message)
        bot.send_message(last_message)
        log_msg(nickname, last_message)
        last_message = ''
    time.sleep(0.01)