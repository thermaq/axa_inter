import os
import time
import json
import logging
from fastapi import FastAPI, Request

logging.basicConfig()
logger = logging.getLogger(__name__)
if os.environ.get('DEBUG', "").lower() in ("yes", "true", "y", "t", "1", 1):
    logger.setLevel(logging.DEBUG)

app = FastAPI()

@app.post("/positions")
async def update_positions(request: Request):
    positions = await request.json()
    for stock in positions:
        print(f"{stock}: {positions[stock]}")

