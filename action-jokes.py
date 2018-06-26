#!/usr/bin/env python2
# -*-: coding utf-8 -*-

from hermes_python.hermes import Hermes
import os
import random
import requests
import time


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

DIR = os.path.dirname(os.path.realpath(__file__)) + '/text/'

lang = "EN"
client = None

class Skill:

    def __init__(self):
        self.jokes = tuple(open(DIR + "jokes_" + lang + ".txt", 'r'))
        print(self.jokes)
    def get_jokes(self):
        line = random.choice(self.jokes)

def callback(hermes, intent_message):
    tmp = hermes.skill.get_jokes()
    current_session_id = intent_message.session_id
    print(tmp)
    hermes.publish_end_session(current_session_id, tmp)

def getLang():
    try:
        return requests.get("http://localhost:3000/config/lang").text.upper();
    except:
        return "EN"
if __name__ == "__main__":
    lang = getLang()
    print(lang)
    skill = Skill()
    with Hermes(MQTT_ADDR) as h:
        h.skill = skill
        h.subscribe_intent("snips-labs:askJokes_" + lang, callback) \
         .loop_forever()
