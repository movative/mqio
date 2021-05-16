import click
import logging as lg

logger: lg.Logger = lg.getLogger(__name__)


def log_level_pipe(level: str):
    lg.basicConfig(
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=level
    )
    return level


@click.command()
#@click.option("--log", dest="loglevel", default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], type=lambda l: log_level_pipe(l))
@click.option("--broker", default="127.0.0.1")
@click.option("--device", default="bulbs")
@click.option("--name", default="bulb1")
@click.option("--gpio", type=int, default=8)
def cli(level: str, broker: str, device: str, name: str, gpio: int):
    """
    :param level: LogLevel of the script from %(choices)s (default: %(default)s)
    :param broker: IP-Address from the MQTT-Broker
    :param device: Type of the device specifies the topic path
    :param name: Name of the device specifies the topic path
    :param gpio: GPIO Port of the device
    :return:
    """
    main: str = f"/home/{device}/{name}"
    command = f"{main}/command"
    status = f"{main}/status"

    #client = MQIO(args)
    #logger.info(f"Connecting to broker @ '{broker}'.")
    #client.connect(broker)
    logger.info("Subscribing to topic " + command + " .")
    #client.subscribe(command)
    #client.loop_forever(retry_first_connection=True)
    logger.info("End. Cleaning up now.")
    pass


if __name__ == "__main__":
    pass
