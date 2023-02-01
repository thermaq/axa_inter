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


class AUMServer:
    def __init__(self, controller_uri, interval, accounts):
        self.splits_url = f"{controller_uri}/splits"
        self.interval = interval
        self.accounts = accounts

    def wait_for_split(self):
        t = self.interval 
        logger.debug(f"waiting for {t}s")
        time.sleep(t)

    def get_split(self):
        splits = [random.randint(1,100) for i in range(self.accounts)]
        split_sum = sum(splits)
        splits_percent = [int(round(split/split_sum*100)) for split in splits]
        splits_percent[random.randint(1,self.accounts)-1] += 100-sum(splits_percent)
        return {
            "accounts": {
                f"account{i+1}": splits_percent[i] for i in range(self.accounts)
            }
        }

    def send_split(self, split):
        logger.debug(f"Sending split {split}")
        try:
            requests.post(self.splits_url, json=split) 
        except:
            logger.exception('Split push error')

    def run(self):
        while True:
            self.wait_for_split()
            split = self.get_split() 
            self.send_split(split)


if __name__ == "__main__":
    aum_server = AUMServer(
        controller_uri = os.environ["CONTROLLER_URI"],
        interval = int(os.environ.get("INTERVAL", 30)),
        accounts = int(os.environ.get("ACCOUNTS", 10))
    )
    aum_server.run()
