#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import hashlib
import hmac
import time

PARTNER_ACCOUNT_API_KEY = "USEAPIKEYASMYID"
PARTNER_ACCOUNT_SECRET = "THISISTHESECRET"

BASE_URL = "https://mock-api.roostoo.com"


def generate_signature(params, secret=PARTNER_ACCOUNT_SECRET):
    query_string = '&'.join(["{}={}".format(k, params[k]) for k in sorted(params.keys())])
    us = secret.encode('utf-8')
    m = hmac.new(us, query_string.encode('utf-8'), hashlib.sha256)
    return m.hexdigest()


def gen_join_code_for_partner():
    payload = {
        "timestamp": int(time.time()) * 1000,
        "bind_email": "lzhao302@usc.edu",
    }

    r = requests.post(
        BASE_URL + "/v2/gen_join_code",
        data=payload,
        headers={
            "RST-API-KEY": PARTNER_ACCOUNT_API_KEY,
            "MSG-SIGNATURE": generate_signature(payload, secret=PARTNER_ACCOUNT_SECRET),
        }
    )
    print r.status_code, r.text


def gen_multi_join_code_for_partner():
    payload = {
        "timestamp": int(time.time()) * 1000,
        "number": 5,
    }

    r = requests.post(
        BASE_URL + "/v2/gen_multi_join_code",
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
        "lb_level": "OVERALL"
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



def create_api():
    payload = {
        "timestamp": int(time.time()) * 1000,
        "email": "zhaolei@pm.me"
    }

    r = requests.post(
        BASE_URL + "/v2/create_api",
        data=payload,
        headers={
            "RST-API-KEY": PARTNER_ACCOUNT_API_KEY,
            "MSG-SIGNATURE": generate_signature(payload, secret=PARTNER_ACCOUNT_SECRET),
        }
    )
    print r.status_code, r.text


if __name__ == '__main__':
    leader_board_for_partner()
    gen_join_code_for_partner()
    gen_multi_join_code_for_partner()
    create_api()
