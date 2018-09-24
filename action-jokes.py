#!/usr/bin/env python2
# -*-: coding utf-8 -*-

from concierge_python.concierge import Concierge
import glob
from hermes_python.hermes import Hermes
import os
import random
import threading
import time

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))
DIR = os.path.dirname(os.path.realpath(__file__)) + '/sound/'
lang = "EN"


class Skill:
    _id = "snips-skill-jokes"

    def __init__(self, concierge, lang):
        print(lang)
        self.jokes = glob.glob( "{}{}/*.wav".format(DIR, lang))
        print(self.jokes)
        self.concierge = concierge
        self._alive = 0
        self.concierge.subscribePing(self.on_ping)

    def get_jokes(self, siteId):
        self.setTimer()
        tmp = random.choice(self.jokes)
        self.concierge.play_wave(siteId, tmp, tmp)

    def on_ping(self):
        if (self._alive > 0):
            self.concierge.publishPong(Skill._id)

    def on_timer(self):
        self._alive -= 1

    def setTimer(self):
        self._alive += 1
        t = threading.Timer(300, self.on_timer)
        t.start()

def callback(hermes, intent_message):
    hermes.skill.get_jokes(intent_message.site_id)
    current_session_id = intent_message.session_id
    hermes.publish_end_session(current_session_id, "")

if __name__ == "__main__":
    lang = Concierge.getLang()
    c = Concierge(MQTT_IP_ADDR)
    skill = Skill(c, lang)
    with Hermes(MQTT_ADDR) as h:
        h.skill = skill
        h.subscribe_intent("snips-labs:askJokes_" + lang, callback) \
         .subscribe_intent("snips-labs:Jokes", callback) \
         .loop_forever()
