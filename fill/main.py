import os
import time
import random
import json
import requests
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', "").lower() in ("yes", "true", "y", "t", "1", 1):
    logger.setLevel(logging.DEBUG)


class FillServer:
    def __init__(self, controller_uri, stocks):
        self.fills_url = f"{controller_uri}/fills"
        self.stocks = stocks

    def wait_for_fill(self):
        t = round(random.uniform(5, 15), 2)
        logger.debug(f"waiting for {t}s")
        time.sleep(t)

    def get_fill(self):
        return {
            "stock": random.choice(self.stocks),
            "price": round(random.uniform(1,100), 2),
            "quantity": random.randint(1,20)
        }

    def send_fill(self, fill):
        logger.debug(f"Sending fill {fill}")
        try:
            requests.post(self.fills_url, json=fill) 
        except:
            logger.exception('Fill push error')

    def run(self):
        while True:
            self.wait_for_fill()
            fill = self.get_fill() 
            self.send_fill(fill)


if __name__ == "__main__":
    fill_server = FillServer(
        controller_uri = os.environ["CONTROLLER_URI"],
        stocks = os.environ["STOCKS"].split(";")
    )
    fill_server.run()

