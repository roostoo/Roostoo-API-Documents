#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import hashlib
import hmac
import time
from pprint import pprint 


API_KEY = "API KEY"
SECRET = "API SECRET"

BASE_URL = "https://mock-api.roostoo.com"


def generate_signature(params):
    query_string = '&'.join(["{}={}".format(k, params[k])
                             for k in sorted(params.keys())])
    us = SECRET.encode('utf-8')
    m = hmac.new(us, query_string.encode('utf-8'), hashlib.sha256)
    return(m.hexdigest())

def get_server_time():
    r = requests.get(
        BASE_URL + "/v3/serverTime",
    )
    print (r.status_code)
    pprint(r.json())
    return (r.json())


def get_ex_info():
    r = requests.get(
        BASE_URL + "/v3/exchangeInfo",
    )
    print (r.status_code)
    pprint(r.json())
    return (r.json())


def get_ticker(pair=None):
    payload = {
        "timestamp": int(time.time()),
    }
    if pair:
        payload["pair"] = pair

    r = requests.get(
        BASE_URL + "/v3/ticker",
        params=payload,
    )
    print (r.status_code)
    pprint(r.json())
    return (r.json())


def get_balance():
    payload = {
        "timestamp": int(time.time()) * 1000,
    }

    r = requests.get(
        BASE_URL + "/v3/balance",
        params=payload,
        headers={"RST-API-KEY": API_KEY,
                 "MSG-SIGNATURE": generate_signature(payload)}
    )
    print(r.status_code)
    pprint(r.json())
    return (r.json())


def place_order(coin, side, qty, wallet="SPOT", price=None):
    payload = {
        "timestamp": int(time.time()) * 1000,
        "pair": coin + "/USD",
        "side": side,
        "quantity": qty,
        "wallet": wallet
    }

    if not price:
        payload['type'] = "MARKET"
    else:
        payload['type'] = "LIMIT"
        payload['price'] = price

    r = requests.post(
        BASE_URL + "/v3/place_order",
        data=payload,
        headers={"RST-API-KEY": API_KEY,
                 "MSG-SIGNATURE": generate_signature(payload)}
    )
    print (r.status_code)
    pprint(r.json())


def cancel_order():
    payload = {
        "timestamp": int(time.time()) * 1000,
        # "order_id": 77,
        "pair": "BTC/USD",
    }

    r = requests.post(
        BASE_URL + "/v3/cancel_order",
        data=payload,
        headers={"RST-API-KEY": API_KEY,
                 "MSG-SIGNATURE": generate_signature(payload)}
    )
    print (r.status_code)
    pprint(r.json())


def query_order():
    payload = {
        "timestamp": int(time.time())*1000,
        # "order_id": 77,
        # "pair": "DASH/USD",
        # "pending_only": True,
    }

    r = requests.post(
        BASE_URL + "/v3/query_order",
        data=payload,
        headers={"RST-API-KEY": API_KEY,
                 "MSG-SIGNATURE": generate_signature(payload)}
    )
    print (r.status_code)
    pprint(r.json())


def pending_count():
    payload = {
        "timestamp": int(time.time()) * 1000,
    }

    r = requests.get(
        BASE_URL + "/v3/pending_count",
        params=payload,
        headers={"RST-API-KEY": API_KEY,
                 "MSG-SIGNATURE": generate_signature(payload)}
    )
    print (r.status_code)
    pprint(r.json())
    return r.json()

def margin_transfer(pair, coin, is_in, qty):
    payload = {
        "timestamp": int(time.time()) * 1000,
        'pair': pair,
        'coin': coin,
        'direction': 'IN' if is_in else "OUT",
        'quantity': qty
    }

    r = requests.post(
        BASE_URL + "/v3/inner_transfer",
        data=payload,
        headers={
            "RST-API-KEY": API_KEY,
            "MSG-SIGNATURE": generate_signature(payload),
        }
    )
    print(r.status_code, r.text)

#unit test
#these line of code will not run when you import this module to another file
if __name__ == '__main__':
    get_server_time()
    get_ex_info()
    get_ticker()
    get_balance()
    place_order("BNB", "BUY", 200000)
    cancel_order()
    query_order()
    pending_count()
    margin_transfer("BTC", "USD", "IN", 1000)
    place_order("BTC", "BUY", 0.01, "MARGIN")
    cancel_order()
    margin_transfer("BTC", "USD", "OUT", 1000)
