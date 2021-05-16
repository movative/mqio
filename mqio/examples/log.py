import logging as lg
from paho.mqtt.client import Client, error_string, MQTTMessage
from mqio.cli import log_level_pipe
from mqio.core import mqio

logger: lg.Logger = lg.getLogger(__name__)

state: bool = False


def on_status(client: Client, payload: str):
    client.publish(state)


def on_command(client, obj, msg):
    print("Deine Mudda")
    logger.info(f"Received: {msg.payload}")


if __name__ == '__main__':
    log_level_pipe('DEBUG')

    device: str = "switch"
    name: str = "1"

    main: str = f"/home/{device}/{name}"
    protocol: dict = {
        f"{main}/command": on_command,
        f"{main}/status": on_status
    }

    mqio(host="127.0.0.1", name=name, main=main, protocol=protocol)
