from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from tools import get_logger, handle_exception, send_telegram
import sys
load_dotenv()
from uomi import uomis_on, uomis_off
from step_tracker import StepTracker, Trackers


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
        send_telegram(f"All steps completed — alarm {state}!")
    else:
        pending=grained_tracker.pending_steps()
        send_telegram("⏳ Pending steps:\n" + "\n".join(f"  - {step}" for step in pending))
grouped_tracker = StepTracker(
    steps=grained_steps,
    on_complete=on_grouped_steps_complete
)

trackers = Trackers(
    grained=grained_tracker,
    grouped=grouped_tracker
)

def on_connect(client, userdata, flags, rc, properties):
    logger.info("Mosquito client connected")
    client.subscribe("scutum")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    logger.info(f"Recieved: {message}")
    if message == "ON":
        trackers.set_state("ON")
        uomis_on(trackers)
    elif message == "OFF":
        trackers.set_state("OFF")
        uomis_off(trackers)
    trackers.reset()
    #client.publish("respuesta", f"recibí '{mensaje}'")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.135", 1883)
client.loop_forever()