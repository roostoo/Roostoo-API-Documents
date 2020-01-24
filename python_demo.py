#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import hashlib
import hmac
import time
import random
import string
import math

PARTNER_ACCOUNT_API_KEY = "USEAPIKEYASMYID"
PARTNER_ACCOUNT_SECRET = "S1XP1e3UZj6A7H5fATj0jNhqPtmdSJYdInClVN65XAbvqqMKjVHjA7PZj4W12oep"

BASE_URL = "https://mock-api.roostoo.com"


def add_join_code_for_partner():
    payload = {
        "timestamp": int(time.time()) * 1000,
        "bind_email": "lzhao302@usc.edu",
    }

    r = requests.post(
        BASE_URL + "/v2/add_join_code",
        data=payload,
        headers={
            "RST-API-KEY": PARTNER_ACCOUNT_API_KEY,
            "MSG-SIGNATURE": generate_signature(payload, secret=PARTNER_ACCOUNT_SECRET),
        }
    )
    print r.status_code, r.text


def leader_board_for_partner():
    payload = {
        "timestamp": int(time.time()) * 1000,
    }

    r = requests.get(
        BASE_URL + "/v2/leader_board",
        params=payload,
        headers={
            "RST-API-KEY": PARTNER_ACCOUNT_API_KEY,
            "MSG-SIGNATURE": generate_signature(payload, secret=PARTNER_ACCOUNT_SECRET),
        }
    )
    print r.status_code, r.text
    print r.headers


if __name__ == '__main__':
    leader_board_for_partner()
    add_join_code_for_partner()
