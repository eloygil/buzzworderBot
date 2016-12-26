import os
import sys
import telebot
import random


TOKEN = sys.argv[1]

bot = telebot.TeleBot(TOKEN)

sources = {
    '**PHRASE**': {'file': 'phrases'},
    '**NOUN**': {'file': 'nouns'},
    '**VERB**': {'file': 'verbs'},
    '**ADJ**': {'file': 'adjectives'},
    '**ADVERB**': {'file': 'adverbs'},
    '**BSE**': {'file': 'bse'},
    '**BSE_START**': {'file': 'bse_start'},
}

def load_file(f):
    prefix = os.path.split(sys.argv[0])[0]
    return [x.replace('\n', '') for x in open(os.path.join(prefix, 'resources', f + '.txt')).readlines()]

@bot.message_handler(commands=['phrase'])
def buzzwordyphrase(message):

    # Load files
    for v in sources.values():
        v['items'] = load_file(v['file'])
        v['blacklist'] = []

    # Choose initial phrase
    ret = random.choice(sources['**PHRASE**']['items'])

    # Iterate till there's no shit to replace
    finished = False
    while(not finished):
        finished = True
        old = ret
        for k, v in sources.items():
            # Try not to repeat words by maintainig a blacklist
            choices = [i for i in v['items'] if i not in v['blacklist']]
            if not choices:
                choices = v['items']
            chosen = random.choice(choices)

            # Replace and add to blacklist if changed
            ret = ret.replace(k, chosen, 1)
            if old != ret:
                v['blacklist'].append(chosen)
                finished = False

    # Return response!
    bot.reply_to(message, ret)

bot.polling()

while True:
    pass
