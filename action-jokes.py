#!/usr/bin/env python2
# -*-: coding utf-8 -*-

from hermes_python.hermes import Hermes
import os
import random
import requests
import time
import glob

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

DIR = os.path.dirname(os.path.realpath(__file__)) + '/sound/'

lang = "EN"
client = None

class Skill:

    def __init__(self):
        self.jokes = glob.glob( "{}{}/*.wav".format(DIR, lang))
        print(self.jokes)
    def get_jokes(self):
        return random.choice(self.jokes)

def callback(hermes, intent_message):
    tmp = hermes.skill.get_jokes()
    current_session_id = intent_message.session_id
    playWav(intent_message.site_id, tmp)
    hermes.publish_end_session(current_session_id, None)

def playWav(siteId, wavFile):
    def getMqttPlayTopic(siteId, requestId):
        return "hermes/audioServer/{}/playBytes/{}".format(siteId,requestId);
    waveFile = wavFile.split('/')[-1]
    topic = getMqttPlayTopic(siteId, waveFile)
    with open(wavFile, "rb") as f:
        value = f.read()
    f.close()
    payload = bytearray(value)
    import paho.mqtt.publish as publish
    publish.single(topic, payload);

def getLang():
    try:
        return requests.get("http://localhost:3000/config/lang").text.upper();
    except:
        return "EN"

if __name__ == "__main__":
    lang = getLang()
    skill = Skill()
    with Hermes(MQTT_ADDR) as h:
        h.skill = skill
        h.subscribe_intent("snips-labs:askJokes_" + lang, callback) \
         .loop_forever()
