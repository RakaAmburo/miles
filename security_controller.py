from dotenv import load_dotenv
load_dotenv()

import paho.mqtt.client as mqtt
from tools import get_logger, handle_exception, send_telegram
import sys
from uomi import uomis_on, uomis_off
from step_tracker import StepTracker, Trackers
from state_mgr import set_state
import constants as const

sys.excepthook = handle_exception

logger = get_logger("sec_cont")

grained_steps=["Camera Living Room", "Camera Work"]
def on_grainded_steps_complete(state):
    pass
grained_tracker = StepTracker(
    steps=grained_steps,
    on_complete=on_grainded_steps_complete
)
grouped_steps=["uomi-cams"]
def on_grouped_steps_complete(state):
    if grained_tracker.is_completed():
        send_telegram(f"✅ All steps completed — alarm {state}!")
    else:
        pending=grained_tracker.pending_steps()
        send_telegram("🚨 alarm {state} - Pending steps:\n" + "\n".join(f"  - {step}" for step in pending))
grouped_tracker = StepTracker(
    steps=grouped_steps,
    on_complete=on_grouped_steps_complete
)

trackers = Trackers(
    grained=grained_tracker,
    grouped=grouped_tracker
)

def on_connect(client, userdata, flags, rc, properties):
    logger.info("Mosquito client connected")
    client.subscribe("scutum")
    client.subscribe(const.TOPIC_MOVIL)
    client.subscribe(const.TOPIC_FULLARMED)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    logger.info(f"Recieved: {msg.topic} -> {message}")

    if msg.topic == const.TOPIC_FULLARMED:
        # Actualizar estado full-armed en DB
        set_state(const.FULL_ARMED, message)
        logger.info(f"Full armed updated: {message}")
        return

    if msg.topic == const.TOPIC_MOVIL or msg.topic == "scutum":
        # Normalizar: casa/movil usa in/out, scutum usa ON/OFF
        if msg.topic == const.TOPIC_MOVIL:
            normalized = const.ON if message == const.OUT else const.OFF
        else:
            normalized = message

        if normalized == const.ON:
            trackers.set_state("ON")
            uomis_on(trackers)
        elif normalized == const.OFF:
            trackers.set_state("OFF")
            uomis_off(trackers)
        trackers.reset()
    #client.publish("respuesta", f"recibí '{mensaje}'")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(const.MQTT_IP, 1883)
client.loop_forever()


""" def on_message(client, userdata, msg):
    camara = msg.topic.split("/")[1]  # sala, entrada, etc
    print(f"Foto de: {camara}")
    with open(f"foto_{camara}.jpg", "wb") as f:
        f.write(msg.payload)

client = mqtt.Client()
client.on_message = on_message
client.connect("localhost", 1883)
client.subscribe("cam/#")
client.loop_forever() """