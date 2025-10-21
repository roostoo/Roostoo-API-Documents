# RoostooPublicAPI

# API SERVICE

* REST API URL: `https://mock-api.roostoo.com`

* [Python Demo](python_demo.py)

- [RoostooPublicAPI](#roostoopublicapi)
- [API SERVICE](#api-service)
- [Document](#document)
  - [Public API_KEY & SECRET_KEY](#public-apikey--secretkey)
  - [Access Security Level](#access-security-level)
  - [RCL_TopLevelCheck (SIGNED) Endpoint security](#rcltoplevelcheck-signed-endpoint-security)
  - [Timing security](#timing-security)
  - [SIGNED Endpoint Examples for POST `/v3/place_order`](#signed-endpoint-examples-for-post-v3placeorder)
    - [Example 1: As a request body (POST endpoint)](#example-1-as-a-request-body-post-endpoint)
    - [Example 2: As a query string (GET endpoint)](#example-2-as-a-query-string-get-endpoint)
- [Roostoo Public API](#roostoo-public-api)
  - [Check server time](#check-server-time)
  - [Exchange information](#exchange-information)
  - [Get Market Ticker](#get-market-ticker)
  - [Balance information](#balance-information)
  - [Pending Order Count](#pending-order-count)
  - [New order  (Trade)](#new-order-trade)
  - [Query order](#query-order)
  - [Cancel order](#cancel-order)

# Document


## Public API_KEY & SECRET_KEY 

* This pair of keys will generate and send when Roostoo offer you Public API promission

* You can apply API premission by mail developer group [jolly@roostoo.com](mailto:jolly@roostoo.com)

## Access Security Level

* `RCL_TSCheck` This level need timestamp parameter
* `RCL_TopLevelCheck` This level need `MSG-SIGNATURE` in header and all above levels requirement

## RCL_TopLevelCheck (SIGNED) Endpoint security
* `RCL_TopLevelCheck` endpoints require parameters: `RST-API-KEY`, `MSG-SIGNATURE`, to be
  sent in the header of http request.
* Endpoints use `HMAC SHA256` signatures. The `HMAC SHA256 signature` is a keyed `HMAC SHA256` operation.
  Use your `secretKey` as the key and `totalParams` as the value for the HMAC operation.
* `totalParams` is defined as the `query string` in GET request OR `request body` in POST request.
* All post request should set http header `Content-Type` = `application/x-www-form-urlencoded`

## Timing security
* A `SIGNED` endpoint also requires a `timestamp` parameter to be sent, which is a millisecond timestamp (13-digits) of request was created and sent.
* The logic is as follows:
  ```javascript
  if (abs(serverTime - timestamp) <= 60*1000) {
    // process request
  } else {
    // reject request
  }
  ```

## SIGNED Endpoint Examples for POST `/v3/place_order`
Here is a step-by-step example of how to send a vaild signed payload from the
Linux command line using `echo`, `openssl`.

Key | Value
------------ | ------------
apiKey | USEAPIKEYASMYID
secretKey | S1XP1e3UZj6A7H5fATj0jNhqPxxdSJYdInClVN65XAbvqqMKjVHjA7PZj4W12oep


Parameter | Value
------------ | ------------
timestamp | 1580774512000
pair | BNB/USD
quantity | 2000
side | BUY
type | MARKET

### Example 1: As a request body (POST endpoint)

* **sortParamsByKey, connect with their value by `=` and connect each param by `&`:** 
pair=BNB/USD&quantity=2000&side=BUY&timestamp=1580774512000&type=MARKET

* **requestBody: (order insensitive)** pair=BNB/USD&quantity=2000&side=BUY&timestamp=1580774512000&type=MARKET
* **HMAC SHA256 signature:**

    ```
    [linux]$ echo -n "pair=BNB/USD&quantity=2000&side=BUY&timestamp=1580774512000&type=MARKET" | openssl dgst -sha256 -hmac "S1XP1e3UZj6A7H5fATj0jNhqPxxdSJYdInClVN65XAbvqqMKjVHjA7PZj4W12oep"
    (stdin)= 20b7fd5550b67b3bf0c1684ed0f04885261db8fdabd38611e9e6af23c19b7fff
    ```

So:
* **Http Header:**:
`Content-Type` = `application/x-www-form-urlencoded`
`RST-API-KEY` = `USEAPIKEYASMYID`
`MSG-SIGNATURE` = `20b7fd5550b67b3bf0c1684ed0f04885261db8fdabd38611e9e6af23c19b7fff`

### Example 2: As a query string (GET endpoint)
* **queryString: (order insensitive)** pair=BNB/USD&quantity=2000&side=BUY&timestamp=1580774512000&type=MARKET
* **HMAC SHA256 signature:**

    ```
    [linux]$ echo -n "pair=BNB/USD&quantity=2000&side=BUY&timestamp=1580774512000&type=MARKET" | openssl dgst -sha256 -hmac "S1XP1e3UZj6A7H5fATj0jNhqPxxdSJYdInClVN65XAbvqqMKjVHjA7PZj4W12oep"
    (stdin)= 20b7fd5550b67b3bf0c1684ed0f04885261db8fdabd38611e9e6af23c19b7fff
    ```

So:
* **Http Header:**:
`RST-API-KEY` = `USEAPIKEYASMYID`
`MSG-SIGNATURE` = `20b7fd5550b67b3bf0c1684ed0f04885261db8fdabd38611e9e6af23c19b7fff`

### Sample Python Code
```python
import requests
import time
import hmac
import hashlib

BASE_URL = "https://mock-api.roostoo.com"
API_KEY = "USEAPIKEYASMYID"
SECRET_KEY = "S1XP1e3UZj6A7H5fATj0jNhqPxxdSJYdInClVN65XAbvqqMKjVHjA7PZj4W12oep"
# --------------------------------------------------------

def _get_timestamp():
    """Returns a 13-digit millisecond timestamp as a string."""
    return str(int(time.time() * 1000))

def _get_signed_headers(payload={}):
    """
    Creates a signature for a given payload (dict) and returns
    the correct headers for a SIGNED (RCL_TopLevelCheck) request.
    """
    # 1. Add timestamp to the payload
    payload['timestamp'] = _get_timestamp()
    
    # 2. Sort keys and create the totalParams string
    sorted_keys = sorted(payload.keys())
    total_params = "&".join(f"{key}={payload[key]}" for key in sorted_keys)
    
    # 3. Create HMAC-SHA256 signature
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        total_params.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # 4. Create headers
    headers = {
        'RST-API-KEY': API_KEY,
        'MSG-SIGNATURE': signature
    }
    
    return headers, payload, total_params

# --- Now we can define functions for each API call ---

```


# Roostoo Public API


## Check server time
```
GET /v3/serverTime
Auth RCL_NoVerification
```
Test connectivity to the Rest API and get the current server time.

**Parameters**

NONE

**Response**
```json
{
  "ServerTime":1570083944052
}
```
### Sample Python Code
```python
def check_server_time():
    """Checks server time. (Auth: RCL_NoVerification)"""
    url = f"{BASE_URL}/v3/serverTime"
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking server time: {e}")
        return None

# --- To run this specific test ---
# if __name__ == "__main__":
#     print("--- Checking Server Time ---")
#     server_time = check_server_time()
#     if server_time:
#         print(f"Server time: {server_time.get('ServerTime')}")
```


## Exchange information
```
GET /v3/exchangeInfo
Auth RCL_NoVerification
```
Current exchange trading rules and symbol information

**Parameters**

NONE

**Response**
```json
{
  "IsRunning": true,
  "InitialWallet": {
    "USD": 50000
  },
  "TradePairs": {
    "BNB/USD": {
      "Coin": "BNB",
      "CoinFullName": "Binance Coin",
      "Unit": "USD",
      "UnitFullName": "US Dollar",
      "CanTrade": true,
      "PricePrecision": 4,
      "AmountPrecision": 2,
      "MiniOrder": 1.0
    },
    "BTC/USD": {
      "Coin": "BTC",
      "CoinFullName": "Bitcoin",
      "Unit": "USD",
      "UnitFullName": "US Dollar",
      "CanTrade": true,
      "PricePrecision": 2,
      "AmountPrecision": 6,
      "MiniOrder": 1.0
    }
  }
}
```


**Return Explain**

Name | Type | Description
------------ | ------------ | ------------
PricePrecision | INT | dicimal precision. Eg. 3 means the minimal order price step is 0.001
AmountPrecision | INT | dicimal precision. Eg. 2 means the minimal order amount step is 0.01
MiniOrder | FLOAT | The one order minimal unit amount. Ok if OrderPrice*OrderAmount > MiniOrder


### Sample Python Code
```python
def get_exchange_info():
    """Gets exchange info. (Auth: RCL_NoVerification)"""
    url = f"{BASE_URL}/v3/exchangeInfo"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting exchange info: {e}")
        return None

# --- To run this specific test ---
# if __name__ == "__main__":
#     print("--- Getting Exchange Info ---")
#     info = get_exchange_info()
#     if info:
#         print(f"Is running: {info.get('IsRunning')}")
#         print(f"Available pairs: {list(info.get('TradePairs', {}).keys())}")

```


## Get Market Ticker
```
GET /v3/ticker
Auth RCL_TSCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING | YES | Used with 13-digits millsecomd timestamp
pair | STRING | NO | `Used with 'EOS/USD', 'TRX/USD', etc.`

**Response if `pair` is sent `(EOS/USD)`**
```json
{
  "Success": true,
  "ErrMsg": "",
  "ServerTime": 1580762734517,
  "Data": {
    "EOS/USD": {
      "MaxBid": 4.2139,
      "MinAsk": 4.2149,
      "LastPrice": 4.2137,
      "Change": -0.0112,
      "CoinTradeValue": 8493899.21,
      "UnitTradeValue": 36057856.188109
    }
  }
}
```

**Response if `pair` is NOT sent**
```json
{
  "Success": true,
  "ErrMsg": "",
  "ServerTime": 1580763411852,
  "Data": {
    "BTC/USD": {
      "MaxBid": 9318.45,
      "MinAsk": 9319.42,
      "LastPrice": 9319.35,
      "Change": -0.0132,
      "CoinTradeValue": 53001.931315,
      "UnitTradeValue": 496450629.05850565
    },
    "ETC/USD": {
      "MaxBid": 11.7137,
      "MinAsk": 11.7189,
      "LastPrice": 11.7137,
      "Change": 0.0144,
      "CoinTradeValue": 4960239.5,
      "UnitTradeValue": 58671425.990265
    },
    "ETH/USD": {
      "MaxBid": 190.4,
      "MinAsk": 190.41,
      "LastPrice": 190.41,
      "Change": -0.0095,
      "CoinTradeValue": 455291.61925,
      "UnitTradeValue": 86565544.788425
    }
  }
}
```

Other info:

* If `pair` is not sent, API will return all tickers data which are listed on RoostooMock 
* If `pair` is sent but it's not listed on RoostooMock, API will return Error (Success=false)
* `Change` is this pair's 24 hours price percentage change, like `0.0059` you can see it as `0.59%` rise, or `-0.0178` as `1.78%` drop


<!-- 
## Available Stream Subscribe
```
GET /v3/available_sub
Auth RCL_NoVerification
```
Current exchange available socket.io subscribe tag

**Parameters**

NONE

**Response**
```json
{
  "ServerTime": 1570234888922,
  "AvailableSub": {
    "BNB/USD": [
      "DEPTH",
      "TICKER"
    ],
    "BTC/USD": [
      "DEPTH",
      "TICKER"
    ],
    "EOS/USD": [
      "DEPTH",
      "TICKER"
    ],
    "ETH/USD": [
      "DEPTH",
      "TICKER"
    ],
    "LTC/USD": [
      "DEPTH",
      "TICKER"
    ],
    "TRX/USD": [
      "DEPTH",
      "TICKER"
    ]
  }
}
``` -->

### Sample Python Code
```python
def get_ticker(pair=None):
    """Gets market ticker. (Auth: RCL_TSCheck)"""
    url = f"{BASE_URL}/v3/ticker"
    params = {
        'timestamp': _get_timestamp()
    }
    if pair:
        params['pair'] = pair
        
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting ticker: {e}")
        return None

# --- To run this specific test ---
# if __name__ == "__main__":
#     print("--- Getting Ticker (All) ---")
#     ticker_all = get_ticker()
#     if ticker_all:
#         print(f"Got data for {len(ticker_all.get('Data', {}))} pairs.")
    
#     print("\n--- Getting Ticker (BTC/USD) ---")
#     ticker_btc = get_ticker(pair="BTC/USD")
#     if ticker_btc:
#         print(f"BTC/USD Last Price: {ticker_btc.get('Data', {}).get('BTC/USD', {}).get('LastPrice')}")
```

## Balance information
```
GET /v3/balance
Auth RCL_TopLevelCheck
```
Get current wallet balance.

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING | YES | Used with 13-digits millsecomd timestamp

**Response**
```json
{
  "Success": true,
  "ErrMsg": "",
  "Wallet": {
    "BTC": {
      "Free": 0.454878,
      "Lock": 0.555
    },
    "ETH": {
      "Free": 0,
      "Lock": 0
    },
    "USD": {
      "Free": 98389854.152001,
      "Lock": 1601798.197999
    }
  }
}
```

### Sample Python Code
```python
def get_balance():
    """Gets account balance. (Auth: RCL_TopLevelCheck)"""
    url = f"{BASE_URL}/v3/balance"
    
    # 1. Get signed headers and the payload (which now includes timestamp)
    # For a GET request with no params, the payload is just the timestamp
    headers, payload, total_params_string = _get_signed_headers(payload={})
    
    try:
        # 2. Send the request
        # In a GET request, the payload is sent as 'params'
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting balance: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None

# --- To run this specific test ---
# if __name__ == "__main__":
#     print("--- Getting Balance ---")
#     balance = get_balance()
#     if balance and balance.get('Success'):
#         print(f"USD Free: {balance.get('Wallet', {}).get('USD', {}).get('Free')}")
#     elif balance:
#         print(f"Error: {balance.get('ErrMsg')}")
```

## Pending Order Count
```
GET /v3/pending_count
Auth RCL_TopLevelCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING | YES | Used with 13-digits millsecomd timestamp

**Response when pending order found**

```json
{
  "Success": true,
  "ErrMsg": "",
  "TotalPending": 3,
  "OrderPairs": {
    "BAT/USD": 1,
    "LINK/USD": 2
  }
}
```

**Response when no pending order found**

```json
{
  "Success": false,
  "ErrMsg": "no pending order under this account",
  "TotalPending": 0,
  "OrderPairs": {}
}
```

### Sample Python Code
```python
def get_pending_count():
    """Gets pending order count. (Auth: RCL_TopLevelCheck)"""
    url = f"{BASE_URL}/v3/pending_count"
    
    headers, payload, total_params_string = _get_signed_headers(payload={})
    
    try:
        response = requests.get(url, headers=headers, params=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting pending count: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None

# --- To run this specific test ---
# if __name__ == "__main__":
#     print("--- Getting Pending Order Count ---")
#     count = get_pending_count()
#     if count:
#         print(f"Success: {count.get('Success')}")
#         print(f"Total Pending: {count.get('TotalPending')}")
#         print(f"Error Msg: {count.get('ErrMsg')}")
```


## New order  (Trade)
```
POST /v3/place_order
Auth RCL_TopLevelCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
pair | STRING | YES | Used with `BTC/USD`, etc...
side | STRING | YES | Used with `BUY`, `SELL`
type | STRING | YES | Used with `LIMIT`, `MARKET`
quantity | STRING | YES | 
timestamp | STRING | YES | Used with 13-digits millsecomd timestamp
price | DECIMAL | NO |


Additional mandatory parameters based on `type`:

Type | Additional mandatory parameters
------------ | ------------
`LIMIT` | `price`

Other info:

* New order should obey rules ExchangeInfo, other wise you will get a `ErrMsg` in response


**Response when it's a Taker order:**
```json
{
  "Success": true,
  "ErrMsg": "",
  "OrderDetail": {
    "Pair": "BTC/USD",
    "OrderID": 81,
    "Status": "FILLED",
    "Role": "TAKER",
    "ServerTimeUsage": 0.039723,
    "CreateTimestamp": 1570224271550,
    "FinishTimestamp": 1570224271590,
    "Side": "SELL",
    "Type": "MARKET",
    "StopType": "GTC",
    "Price": 8149.07,
    "Quantity": 11.112,
    "FilledQuantity": 11.112,
    "FilledAverPrice": 8149.07,
    "CoinChange": 11.112,
    "UnitChange": 90552.46584,
    "CommissionCoin": "USD",
    "CommissionChargeValue": 10.8662959008,
    "CommissionPercent": 0.00012
  }
}

```
**Response when it's a Maker order:**
```json
{
  "Success": true,
  "ErrMsg": "",
  "OrderDetail": {
    "Pair": "BTC/USD",
    "OrderID": 83,
    "Status": "PENDING",
    "Role": "MAKER",
    "ServerTimeUsage": 0.040867,
    "CreateTimestamp": 1570224463181,
    "FinishTimestamp": 0,
    "Side": "SELL",
    "Type": "LIMIT",
    "StopType": "GTC",
    "Price": 8893,
    "Quantity": 11.112,
    "FilledQuantity": 0,
    "FilledAverPrice": 0,
    "CoinChange": 0,
    "UnitChange": 0,
    "CommissionCoin": "USD",
    "CommissionChargeValue": 0,
    "CommissionPercent": 0.00008
  }
}
```

### Sample Python Code
```python
def place_order(pair_or_coin, side, quantity, price=None, order_type=None):
    """
    Places a new order with improved flexibility and safety checks.

    Args:
        pair_or_coin (str): The asset to trade (e.g., "BTC" or "BTC/USD").
        side (str): "BUY" or "SELL".
        quantity (float or int): The amount to trade.
        price (float, optional): The price for a LIMIT order. Defaults to None.
        order_type (str, optional): "LIMIT" or "MARKET". Auto-detected if not provided.
    """
    print(f"\n--- Placing a new order for {quantity} {pair_or_coin} ---")
    url = f"{BASE_URL}/v3/place_order"

    # 1. Determine the full pair name
    pair = f"{pair_or_coin}/USD" if "/" not in pair_or_coin else pair_or_coin

    # 2. Auto-detect order_type if it's not specified
    if order_type is None:
        order_type = "LIMIT" if price is not None else "MARKET"
        print(f"Auto-detected order type: {order_type}")

    # 3. Validate parameters to prevent errors
    if order_type == 'LIMIT' and price is None:
        print("Error: LIMIT orders require a 'price' parameter.")
        return None
    if order_type == 'MARKET' and price is not None:
        print("Warning: Price is provided for a MARKET order and will be ignored by the API.")

    # 4. Create the request payload
    payload = {
        'pair': pair,
        'side': side.upper(),
        'type': order_type.upper(),
        'quantity': str(quantity)
    }
    if order_type == 'LIMIT':
        payload['price'] = str(price)

    # 5. Get signed headers and the final request body
    headers, total_params_string = _get_signed_headers_and_body(payload)

    # 6. Send the request
    try:
        response = requests.post(url, headers=headers, data=total_params_string)
        response.raise_for_status()
        print(f"API Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error placing order: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None


# --- Example Usage ---
#if __name__ == "__main__":
    # Example 1: Place a LIMIT order (by providing a price)
    # The function will correctly identify this as a LIMIT order.
#    place_order(
#        pair_or_coin="BTC",
#        side="SELL",
#        quantity=0.01,
#        price=99000
#    )

    # Example 2: Place a MARKET order (by not providing a price)
    # The function will correctly identify this as a MARKET order.
#    place_order(
#        pair_or_coin="BNB/USD",
#        side="BUY",
#        quantity=10
#    )

    # Example 3: Invalid order (LIMIT without a price)
    # The function will catch this error before sending the request.
#    place_order(
#        pair_or_coin="ETH",
#        side="BUY",
#        quantity=0.5,
#        order_type="LIMIT" # Explicitly set, but no price given
#    )
```

## Query order
```
POST /v3/query_order
Auth RCL_TopLevelCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING | YES | Used with 13-digits millsecomd timestamp
order_id | STRING | NO | 
pair | STRING | NO | Used with `BTC/USD`, etc...
offset | STRING_INT | NO |  
limit | STRING_INT | NO |
pending_only | STRING_BOOL | NO |  Used with `TRUE` `FALSE`

Other info:

* when `order_id` is sent, none of other optional parameter is allowed. 
* if none of `order_id` and `pair` is sent, system will match all orders under this user's account.
* `pending_only` can send to ask pending order(s) only. 
* if `limit` is not sent, the default limit would be implemented and set to 100. 

**Response when at least one order matched:**
```json
{
  "Success": true,
  "ErrMsg": "",
  "OrderMatched": [
    {
      "Pair": "BTC/USD",
      "OrderID": 81,
      "Status": "FILLED",
      "Role": "TAKER",
      "ServerTimeUsage": 0.039723,
      "CreateTimestamp": 1570199071550,
      "FinishTimestamp": 1570199071590,
      "Side": "SELL",
      "Type": "MARKET",
      "StopType": "GTC",
      "Price": 8149.07,
      "Quantity": 11.112,
      "FilledQuantity": 11.112,
      "FilledAverPrice": 8149.07,
      "CoinChange": 11.112,
      "UnitChange": 90552.46584,
      "CommissionCoin": "USD",
      "CommissionChargeValue": 10.866295,
      "CommissionPercent": 0.00012
    },
    {
      "Pair": "BTC/USD",
      "OrderID": 80,
      "Status": "PENDING",
      "Role": "MAKER",
      "ServerTimeUsage": 0.039082,
      "CreateTimestamp": 1570198992695,
      "FinishTimestamp": 0,
      "Side": "BUY",
      "Type": "LIMIT",
      "StopType": "GTC",
      "Price": 7893,
      "Quantity": 11.112,
      "FilledQuantity": 11.112,
      "FilledAverPrice": 0,
      "CoinChange": 0,
      "UnitChange": 0,
      "CommissionCoin": "BTC",
      "CommissionChargeValue": 0,
      "CommissionPercent": 0.00008
    },
    {
      "Pair": "BTC/USD",
      "OrderID": 79,
      "Status": "CANCELED",
      "Role": "MAKER",
      "ServerTimeUsage": 0.042137,
      "CreateTimestamp": 1570198744804,
      "FinishTimestamp": 1570224038339,
      "Side": "BUY",
      "Type": "LIMIT",
      "StopType": "GTC",
      "Price": 7893,
      "Quantity": 11.112,
      "FilledQuantity": 11.112,
      "FilledAverPrice": 0,
      "CoinChange": 0,
      "UnitChange": 0,
      "CommissionCoin": "BTC",
      "CommissionChargeValue": 0,
      "CommissionPercent": 0.00008
    }
  ]
}


```
**Response when no order matched:**
```json
{
  "Success": false,
  "ErrMsg": "no order matched"
}
```

### Sample Python Code
```python
def query_order(order_id=None, pair=None, pending_only=None):
    """Queries orders. (Auth: RCL_TopLevelCheck)"""
    url = f"{BASE_URL}/v3/query_order"
    
    payload = {}
    if order_id:
        payload['order_id'] = str(order_id)
    elif pair: # Docs say order_id and pair cannot be sent together
        payload['pair'] = pair
        if pending_only is not None:
             # Docs specify STRING_BOOL
            payload['pending_only'] = 'TRUE' if pending_only else 'FALSE'
            
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        response = requests.post(url, headers=headers, data=total_params_string)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying order: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None

# --- To run this specific test ---
# if __name__ == "__main__":
#     print("--- Querying Pending BTC/USD Orders ---")
#     orders = query_order(pair="BTC/USD", pending_only=True)
#     if orders and orders.get('Success'):
#         print(f"Found {len(orders.get('OrderMatched', []))} matching orders.")
#     elif orders:
#         print(f"Error: {orders.get('ErrMsg')}")
```


## Cancel order
```
POST /v3/cancel_order
Auth RCL_TopLevelCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
order_id | STRING | NO |
pair | STRING | NO | Used with `BTC/USD`, etc...
timestamp | STRING | YES | Used with 13-digits millsecomd timestamp


Other info:

* only pending order can be canceled.
* `order_id` and `pair` are not mandatory parameters. 
* `order_id` and `pair` only none or one parameter allowed.
* if one of `order_id` and `pair` is sent, system will cancel 0-? pending order(s) based on given statement.
* if none of `order_id` and `pair` is sent, system will cancel all pending orders under this user's account.


**Response**
```json
{
  "Success": true,
  "ErrMsg": "",
  "CanceledList": [
    20,
    35
  ]
}
```
### Sample Python Code
```python
def cancel_order(order_id=None, pair=None):
    """Cancels orders. (Auth: RCL_TopLevelCheck)"""
    url = f"{BASE_URL}/v3/cancel_order"
    
    payload = {}
    if order_id:
        payload['order_id'] = str(order_id)
    elif pair: # Docs say only one is allowed
        payload['pair'] = pair
    # If neither is sent, it cancels all
        
    headers, final_payload, total_params_string = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    
    try:
        response = requests.post(url, headers=headers, data=total_params_string)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error canceling order: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None

# --- To run this specific test ---
# if __name__ == "__main__":
#     # First, let's place an order to cancel
#     print("--- Placing an order to cancel ---")
#     order_to_cancel = place_order("ETH/USD", "BUY", "LIMIT", 0.1, 1000)
#     if order_to_cancel and order_to_cancel.get('Success'):
#         order_id = order_to_cancel.get('OrderDetail', {}).get('OrderID')
#         print(f"Placed order with ID: {order_id}")
        
#         if order_id:
#             print(f"\n--- 8. Canceling order {order_id} ---")
#             cancel_result = cancel_order(order_id=order_id)
#             if cancel_result:
#                 print(f"Cancel Success: {cancel_result.get('Success')}")
#                 print(f"Canceled List: {cancel_result.get('CanceledList')}")
#     else:
#         print("Could not place order to test cancellation.")
```

<!-- ## Get Leader Board information

```
GET /v2/leader_board
Auth RCL_TopLevelCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING_OF_INT | YES | Used with 13-digits millsecomd timestamp

**Response if success**
```json
{
  "Success": true,
  "ErrMsg": "",
  "LastUpdate": 1579871672843,
  "UpdateInterval": 5,
  "PublicRank": [
    {
      "Rank": 1,
      "UserCode": "XX1",
      "Email": "zh***@usc.edu",
      "DisplayName": "",
      "PhotoURL": "",
      "InitBal": 50000,
      "CurrBal": 98623.87,
      "TradeVolume": 379807.14,
      "Profit": 0.9725
    },
    {
      "Rank": 2,
      "UserCode": "XX2",
      "Email": "na***@gmail.com",
      "DisplayName": "",
      "PhotoURL": "",
      "InitBal": 50000,
      "CurrBal": 64175.54,
      "TradeVolume": 56469.05,
      "Profit": 0.2835
    },
    {
      "Rank": 3,
      "UserCode": "XX3",
      "Email": "dy***@gmail.com",
      "DisplayName": "",
      "PhotoURL": "",
      "InitBal": 50000,
      "CurrBal": 62415.25,
      "TradeVolume": 54825.69,
      "Profit": 0.2483
    },
    ...
  ]
}

```

**Response if fail**
```json
{
  "Success": false,
  "ErrMsg": "your partner access is terminated",
  "LastUpdate": 0,
  "UpdateInterval": 0,
  "PublicRank": null
}
```


**Return Explain**

Name | Type | Description
------------ | ------------ | ------------
Success | BOOL | Indicates is this request success
ErrMsg | STRING | Error message, if "" means it's passed(Success=true), othervice it tells you about problem.
LastUpdate | INT | The 13-digits millsecond timestamp marks update time of this rank.
UpdateInterval | INT | The Integer marks as the update interval (minutes).
UserCode | STRING | Can be used to identify one user.
DisplayName | STRING | The display name which is set by user OR auto set by OAUTH provider, such as Google OAuth. It could be "" if it is not set.
PhotoURL | STRING | The URL for user photo which is set by user or OAuth provider. It could be "" if it is not set.
InitBal | FLOAT | The user's wallet when join this competition (unit: USD).
CurrBal | FLOAT | The user's wallet when last update time of leader board (unit: USD).
TradeVolume | FLOAT | The user's total trade volume during this competition (unit: USD).
Profit | FLOAT | User profit change since the competition began. (CurrBal-InitBal) / InitBal


Other info:

* The total amount of rank list length is the count of participants but no more than 100.
* `TotalProfit = 0.0070` means the user total wallet value `increase 0.07%`.
* `Profit24hr = -0.0107` means the user total wallet value `drop 1.07%`. -->
