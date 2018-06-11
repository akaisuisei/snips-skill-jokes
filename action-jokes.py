#!/usr/bin/env python2
# -*-: coding utf-8 -*-

from hermes_python.hermes import Hermes
import os
import time
import random

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

DIR = os.path.dirname(os.path.realpath(__file__)) + '/text/'

class Skill:

    def __init__(self):
        self.lang = 'en'
        self.jokes = tuple(open(DIR + "jokes_" + self.lang + ".txt", 'r'))
        print(self.jokes)
    def get_jokes(self):
        return random.choice(self.jokes)

def callback(hermes, intent_message):
    tmp = hermes.skill.get_jokes()
    current_session_id = intent_message.session_id
    print(tmp)
    hermes.publish_end_session(current_session_id, tmp)

if __name__ == "__main__":
    skill = Skill()
    
    with Hermes(MQTT_ADDR) as h: 
        h.skill = skill
        h.subscribe_intent("akaisuisei:askJokes", callback) \
         .loop_forever()
