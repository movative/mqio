import logging as lg
from paho.mqtt.client import Client, error_string, MQTTMessage
from mqio.core import log_level_pipe

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


def mqtt(host: str, name: str, main: str, protocol: dict):
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

def on_command(client, obj, msg):

    logger.info(f"Received: {msg.payload}")
    if msg.payload == "1":
        gpio.output(args.gpio, True)
    elif msg.payload == "0":
        logger.info("Received: 0")
        gpio.output(args.gpio, False)
    elif msg.payload == "?":
        logger.info("Received: ?")
        client.publish(state, ".")


if __name__ == '__main__':
    log_level_pipe('DEBUG')

    device: str = "log"
    name: str = "1"
    main: str = f"/home/{device}/{name}"
    protocol: dict = {
        f"{main}/command": on_command
    }
    test(host="127.0.0.1", name=name, main=main)
