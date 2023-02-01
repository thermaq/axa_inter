from pydantic import BaseModel, validator
from typing import Dict


class Fill(BaseModel):
    stock: str
    price: float
    quantity: int


class Splits(BaseModel):
    accounts: Dict[str, int]

    @validator('accounts')
    @classmethod
    def check_accounts(cls, accs):
        s = 0
        for k,v in accs.items():
            if v < 0:
                raise ValueError("Splits have to be bigger than 0")
            s += v
        if s != 100:
            raise ValueError("Splits don't add up to 100%")
        return accs

