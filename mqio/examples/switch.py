import logging as lg
from paho.mqtt.client import Client, MQTTMessage

from mqio.cli import log_level_pipe

logger: lg.Logger = lg.getLogger(__name__)

state: bool = False


def on_status(client: Client, payload: str):
    client.publish(state)


def on_command(client, obj, msg: MQTTMessage):
    state = msg.payload



if __name__ == '__main__':
    log_level_pipe('DEBUG')

    device: str = "log"
    name: str = "1"
    main: str = f"/home/{device}/{name}"
    protocol: dict = {
        f"{main}/command": on_command,
        f"{main}/status": on_status
    }
    mqio(host="127.0.0.1", name=name, main=main, protocol=protocol)
