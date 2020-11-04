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

* This pair of keys will generate and send when Roostoo offer you Public API permission

* You can apply API permission by mail developer group [jolly@roostoo.com](mailto:jolly@roostoo.com)

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
