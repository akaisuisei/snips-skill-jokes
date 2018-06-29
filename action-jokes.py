#!/usr/bin/env python2
# -*-: coding utf-8 -*-

import glob
from hermes_python.hermes import Hermes
import os
import paho.mqtt.client as mqtt
import random
import requests
import threading
import time

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

DIR = os.path.dirname(os.path.realpath(__file__)) + '/sound/'

alive = 0;
lang = "EN"
client = None
pingTopic = 'concierge/apps/live/ping'
pongTopic = 'concierge/apps/live/pong'

def on_connect(client, userdata, flags, rc):
    if (alive > 0):
        client.subscribe(pingTopic)

def on_message(client, userdata, msg):
    client.publish(pongTopic, '{"result":"snips-skill-joke"}')

def setTimer():
    global alive
    alive += 1
    client.subscribe(pingTopic)
    t = threading.Timer(300, runTimer)
    t.start()

def runTimer():
    global alive
    alive -= 1
    if (alive <= 0):
        client.unsubscribe(pingTopic)

def getLang():
    try:
        res = requests.get("http://localhost:3000/assistant/lang").json;
        return res.response
    except :
        return "EN"

class Skill:

    def __init__(self):
        self.jokes = glob.glob( "{}{}/*.wav".format(DIR, lang))
        print(self.jokes)
    def get_jokes(self):
        return random.choice(self.jokes)

def callback(hermes, intent_message):
    setTimer()
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


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_IP_ADDR)
    client.loop_start()
    lang = getLang()
    skill = Skill()
    with Hermes(MQTT_ADDR) as h:
        h.skill = skill
        h.subscribe_intent("snips-labs:askJokes_" + lang, callback) \
         .loop_forever()
