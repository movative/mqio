import logging as lg
from paho.mqtt.client import Client, error_string, MQTTMessage

logger: lg.Logger = lg.getLogger(__name__)


def on_connect(client, userdata, flags, rc, properties=None):
    logger.info(error_string(rc))


def on_disconnect(client: Client, userdata, rc):
    logger.info(f"({rc}) {error_string(rc)}")
    if rc != 0:
        client.reconnect()


def on_subscribe(client: Client, userdata, mid, granted_qos, properties):
    logger.debug(f"Subscribed to {userdata, mid, granted_qos, properties}")


def on_message(client: Client, userdata, message: MQTTMessage):
    message.payload = str(message.payload.decode("utf-8"))
    logger.debug("Received a message on" + message.topic)


def mqio(host: str, name: str, main: str, protocol: dict):
    client = Client(name)
    client.enable_logger(logger=logger)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    for sub, callback in protocol.items():
        client.message_callback_add(sub, callback)
    client.subscribe(f"{main}/#", 0)
    logger.debug(f"Started with protocol: {protocol}")
    client.connect(host=host)
    client.loop_forever(retry_first_connection=True)