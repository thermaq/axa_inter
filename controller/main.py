import os
import time
import random
import json
import logging
import requests
from fastapi import FastAPI, Request
from fastapi_utils.tasks import repeat_every
from models import Fill, Splits
from database import Database

logging.basicConfig()
POSITIONS_URL = os.environ['POSITIONS_URI'] + "/positions"
database = Database()
logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', "").lower() in ("yes", "true", "y", "t", "1", 1):
    logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=int(os.environ.get('INTERVAL', 10)))
async def send_positions():
    logger.debug('send_positions')
    async with database.lock() as session:
        positions = session.get_all_positions()
    if not positions:
        logger.debug('No positions to send')
        return
    logger.debug(f"Sending positions", positions)
    try:
        requests.post(POSITIONS_URL, json=positions) 
    except:
        logger.exception('Positions push error')


def split_fill(splits, fill, positions):
    q = fill.quantity
    stock_sum = sum(positions.values()) + q
    ideal_differences = []
    for acc in splits:
        if acc not in positions:
            positions[acc] = 0
        ideal_position = int(round(splits[acc]*stock_sum/100))
        ideal_differences.append((ideal_position - positions[acc], acc))
    for difference, account in sorted(ideal_differences, reverse=True):
        if difference < 0:
            if q > 0:
                logger.error(f'Leftover stock ({q})!')
            break
        if q > difference:
            q -= difference
            positions[account] += difference
        elif q > 0:
            positions[account] += q
            break
    return positions


@app.post("/fills")
async def fills(fill: Fill):
    logger.debug(f'Got a fill {fill.dict()}')
    async with database.lock() as session:
        splits = session.get_splits()
        positions = session.get_positions(fill.stock)
        logger.debug(f'Actual splits: {splits}')
        logger.debug(f'Actual positions: {positions}')
        if len(splits) == 0:
            logger.info(f'Got fills before splits. Ignoring')
            return
        new_positions = split_fill(splits, fill, positions)
        logger.debug(f'New positions: {new_positions}')
        session.update_positions(fill.stock, new_positions)


@app.post("/splits")
async def splits(splits: Splits):
    logger.debug(f'Got a split {splits.dict()}')
    async with database.lock() as session:
        session.update_splits(splits.accounts)

