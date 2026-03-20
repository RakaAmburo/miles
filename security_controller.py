from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from tools import get_logger, handle_exception
import sys
load_dotenv()
from uomi import uomis_on, uomis_off

sys.excepthook = handle_exception

logger = get_logger("sec_cont")

def on_connect(client, userdata, flags, rc, properties):
    logger.info("Mosquito client connected")
    client.subscribe("scutum")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    logger.info(f"Recieved: {message}")
    if message == "ON":
        uomis_on()
    elif message == "OFF":
        uomis_off()
    #client.publish("respuesta", f"recibí '{mensaje}'")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.1.135", 1883)
client.loop_forever()