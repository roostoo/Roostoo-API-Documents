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
  - [Open short position (Trade)](#open-short-position-trade)
  - [Close short position (Trade)](#close-short-position-trade)
  - [Get short positions](#get-short-positions)

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
```
-->



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

## Open short position (Trade)
```
POST /v6/short_open
Auth RCL_TopLevelCheck
```
Open a new short position, or add to the one you already hold on that pair.

Note these short endpoints are served under `/v6` instead of `/v3`. They use the same host, the
same `API_KEY` / `SECRET_KEY` and the same `RCL_TopLevelCheck` signing rules as the endpoints
above.

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
pair | STRING | YES | Used with `BTC/USD`, etc...
collateral | STRING | YES | The USD amount to lock as collateral. Minimum `1`.
timestamp | STRING | YES | Used with 13-digits millsecomd timestamp
order_type | STRING | NO | Used with `LIMIT`. If not sent, or sent with any other value, the order is a market order.
price | DECIMAL | NO |


Additional mandatory parameters based on `order_type`:

Type | Additional mandatory parameters
------------ | ------------
`LIMIT` | `price`

Other info:

* There is no `side` or `quantity` parameter. A short is sized by the `collateral` you commit, and
  the quantity is calculated from it as `collateral / EntryPrice`, rounded down to the pair's
  `AmountPrecision` from ExchangeInfo.
* A market order fills immediately at the current best bid (`MaxBid` in the ticker).
* A `LIMIT` order does not fill when placed. It stays pending until the market reaches your price.
  If `price` is at or above the current market it fills when the price rises, if it is below the
  current market it fills when the price drops.
* The fee is `0.1%` of the position value, the same for market and limit orders. It is
  `ShortQty * EntryPrice * 0.001`, charged when the request is accepted, including for a `LIMIT`
  order that has not been filled yet.
* For example, a short opened with `10000` collateral pays `10` as the open fee, `0.1%` of `10000`.
* Opening again on a pair you are already short will merge into the existing position, using a
  quantity weighted average entry price. No second position is created.
* The pending order created by a `LIMIT` order can be canceled with `POST /v3/cancel_order` using
  its `order_id`. Canceling releases both the locked collateral and the open fee.
* Your free `USD` balance must cover `collateral` + fee, otherwise you will get a `ErrMsg` in
  response.


**Response when it's a market order:**
```json
{
  "Success": true,
  "ID": 412,
  "Pair": "BTC/USD",
  "OrderType": "MARKET",
  "EntryPrice": 50000,
  "ShortQty": 0.2,
  "Collateral": 10000,
  "OpenFee": 10,
  "Status": "OPEN",
  "CreateTimestamp": 1757980800000
}
```
**Response when it's a limit order:**
```json
{
  "Success": true,
  "ID": 90271,
  "Pair": "BTC/USD",
  "OrderType": "LIMIT",
  "EntryPrice": 62500,
  "ShortQty": 0.16,
  "Collateral": 10000,
  "OpenFee": 10,
  "Status": "PENDING",
  "CreateTimestamp": 1757980800000
}
```

**Return Explain**

Name | Type | Description
------------ | ------------ | ------------
ID | INT | When `Status` is `OPEN` this is the short position id, the same id returned by `/v6/short_positions`. When `Status` is `PENDING` this is the order id, used to cancel the order.
Pair | STRING | The pair of this position.
OrderType | STRING | `MARKET` or `LIMIT`.
EntryPrice | FLOAT | The filled price for a market order, or your requested price for a limit order. After a merge it is the weighted average entry price of the whole position.
ShortQty | FLOAT | The quantity shorted. After a merge it is the total quantity of the whole position.
Collateral | FLOAT | The USD locked against the position. After a merge it is the total collateral of the whole position.
OpenFee | FLOAT | The commission charged for this request only, `0.1%` of `ShortQty * EntryPrice`. It is not the cumulative fee of a merged position.
Status | STRING | `OPEN` means filled and the position is live. `PENDING` means the limit order is waiting to be filled.
CreateTimestamp | INT | The 13-digits millsecomd timestamp of this request.


## Close short position (Trade)
```
POST /v6/short_close
Auth RCL_TopLevelCheck
```
Close all or part of an open short position. It always fills immediately at the current best ask
(`MinAsk` in the ticker).

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
pair | STRING | YES | Used with `BTC/USD`, etc...
timestamp | STRING | YES | Used with 13-digits millsecomd timestamp
close_qty | STRING | NO | The absolute quantity to close.
close_pct | STRING | NO | The percentage to close, greater than `0` and at most `100`.

Other info:

* if `close_qty` is sent, it takes precedence over `close_pct`.
* if none of `close_qty` and `close_pct` is sent, system will close the whole position.
* every close is reduce only. A `close_qty` bigger than the open quantity is reduced to it, so a
  short can never be over closed or turned into a long.
* a partial close keeps the entry price unchanged and reduces the quantity and the collateral in
  proportion. The remaining collateral stays locked until the position is fully closed.
* a short can never lose more than the collateral backing it, so `RealizedPNL` is capped at that
  loss.
* the close fee is `0.1%` of the value you close, `ClosedQty * ClosePrice * 0.001`. In the example
  below half of a `10000` position is closed, that half is worth `4800` at the close price, so the
  fee is `4.8`.
* if the requested part would leave a remainder too small to keep, system will close the whole
  position instead and `FullyClosed` will be `true`.


**Response when it's a partial close:**
```json
{
  "Success": true,
  "ClosePrice": 48000,
  "RealizedPNL": 200,
  "CloseFee": 4.8,
  "ReturnAmount": 5195.2,
  "ClosedQty": 0.1,
  "FullyClosed": false,
  "RemainingQty": 0.1,
  "RemainingCollateral": 5000
}
```
**Response when it's a full close:**
```json
{
  "Success": true,
  "ClosePrice": 48000,
  "RealizedPNL": 400,
  "CloseFee": 9.6,
  "ReturnAmount": 10390.4,
  "ClosedQty": 0.2,
  "FullyClosed": true
}
```

**Return Explain**

Name | Type | Description
------------ | ------------ | ------------
ClosePrice | FLOAT | The price this close was filled at.
RealizedPNL | FLOAT | The settled profit or loss on the closed part of the position, `ClosedQty * (EntryPrice - ClosePrice)`. It is not rounded, so it can carry many decimal places.
CloseFee | FLOAT | The commission charged on the closed part, `0.1%` of `ClosedQty * ClosePrice`.
ReturnAmount | FLOAT | The USD returned to your wallet, `closed collateral + RealizedPNL - CloseFee`. It can be negative when the loss reaches the full collateral.
ClosedQty | FLOAT | The quantity actually closed.
FullyClosed | BOOL | `true` if the position is now fully closed, `false` if a part of it is still open.
RemainingQty | FLOAT | The quantity still open. Not returned when it's a full close.
RemainingCollateral | FLOAT | The collateral still locked. Not returned when it's a full close.


## Get short positions
```
GET /v6/short_positions
Auth RCL_TopLevelCheck
```
Get all your currently open short positions, with live profit and loss.

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING | YES | Used with 13-digits millsecomd timestamp

Other info:

* only open positions are returned. Closed positions can be found in your order history with
  `POST /v3/query_order`, where opening and closing a short appear as orders with `Side` =
  `SHORT_OPEN` and `Side` = `SHORT_CLOSE`.
* `Positions` is always a list. It is `[]` when no position is open, never `null`.
* `UnrealizedPNL` is the value a close would realize before the close fee is charged.


**Response when at least one position is open:**
```json
{
  "Success": true,
  "Positions": [
    {
      "ID": 412,
      "Pair": "BTC/USD",
      "EntryPrice": 50000,
      "ShortQty": 0.2,
      "Collateral": 10000,
      "CurrentPrice": 48000,
      "UnrealizedPNL": 400,
      "UnrealizedPNLPct": 0.04,
      "PositionValue": 10400,
      "CreateTimestamp": 1757980800000,
      "PositionStatus": "OPEN"
    }
  ]
}
```
**Response when no position is open:**
```json
{
  "Success": true,
  "Positions": []
}
```

**Return Explain**

Name | Type | Description
------------ | ------------ | ------------
ID | INT | The short position id, the same id returned by `/v6/short_open` when `Status` is `OPEN`.
Pair | STRING | The pair of this position.
EntryPrice | FLOAT | The weighted average entry price of the position.
ShortQty | FLOAT | The quantity shorted.
Collateral | FLOAT | The USD locked against the position.
CurrentPrice | FLOAT | The current market price a close would be filled at, the pair's `MinAsk`.
UnrealizedPNL | FLOAT | The profit or loss if the position were closed now, before the close fee.
UnrealizedPNLPct | FLOAT | `UnrealizedPNL` against the collateral, like `0.04` you can see it as `4%` profit, or `-0.0107` as `1.07%` loss.
PositionValue | FLOAT | `Collateral + UnrealizedPNL`, what a full close is worth before the fee.
CreateTimestamp | INT | The 13-digits millsecomd timestamp when the position was opened.
PositionStatus | STRING | Always `OPEN` on this endpoint.


**Response when a short request fails:**
```json
{
  "Success": false,
  "ErrMsg": "insufficient balance"
}
```

Other info for all three short endpoints:

* Like the endpoints above, a failed request is still answered with http `200` and an `ErrMsg`, so
  always check the `Success` flag.
* Common `ErrMsg` values are `insufficient balance`, `minimum collateral is $1`, `pair not found`,
  `no open short position for this pair`, `this competition does not allow short positions`,
  `limit order requires a price` and `your do not have permission to trade`.
* A field whose value is zero is left out of the response instead of being returned as `0`. For
  example `OpenFee` is not returned when the fee is zero, and `RemainingQty` is not returned when
  it's a full close. Read a missing field as `0`.
* Only the parameters listed for each endpoint are used to build the signature on the server side.
  Any other parameter you send is ignored there, so if you include it in your own signature the
  request will be rejected.

## Sample Python Code
```python
import requests
import time
import hmac
import hashlib

# --- API Configuration ---
BASE_URL = "https://mock-api.roostoo.com"
API_KEY = "YOUR_API_KEY_HERE"      # Replace with your actual API key
SECRET_KEY = "YOUR_SECRET_KEY_HERE"  # Replace with your actual secret key


# ------------------------------
# Utility Functions
# ------------------------------

def _get_timestamp():
    """Return a 13-digit millisecond timestamp as string."""
    return str(int(time.time() * 1000))


def _get_signed_headers(payload: dict = {}):
    """
    Generate signed headers and totalParams for RCL_TopLevelCheck endpoints.
    """
    payload['timestamp'] = _get_timestamp()
    sorted_keys = sorted(payload.keys())
    total_params = "&".join(f"{k}={payload[k]}" for k in sorted_keys)

    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        total_params.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    headers = {
        'RST-API-KEY': API_KEY,
        'MSG-SIGNATURE': signature
    }

    return headers, payload, total_params


# ------------------------------
# Public Endpoints
# ------------------------------

def check_server_time():
    """Check API server time."""
    url = f"{BASE_URL}/v3/serverTime"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking server time: {e}")
        return None


def get_exchange_info():
    """Get exchange trading pairs and info."""
    url = f"{BASE_URL}/v3/exchangeInfo"
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting exchange info: {e}")
        return None


def get_ticker(pair=None):
    """Get ticker for one or all pairs."""
    url = f"{BASE_URL}/v3/ticker"
    params = {'timestamp': _get_timestamp()}
    if pair:
        params['pair'] = pair
    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting ticker: {e}")
        return None


# ------------------------------
# Signed Endpoints
# ------------------------------

def get_balance():
    """Get wallet balances (RCL_TopLevelCheck)."""
    url = f"{BASE_URL}/v3/balance"
    headers, payload, _ = _get_signed_headers({})
    try:
        res = requests.get(url, headers=headers, params=payload)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting balance: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None


def get_pending_count():
    """Get total pending order count."""
    url = f"{BASE_URL}/v3/pending_count"
    headers, payload, _ = _get_signed_headers({})
    try:
        res = requests.get(url, headers=headers, params=payload)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting pending count: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None


def place_order(pair_or_coin, side, quantity, price=None, order_type=None):
    """
    Place a LIMIT or MARKET order.
    """
    url = f"{BASE_URL}/v3/place_order"
    pair = f"{pair_or_coin}/USD" if "/" not in pair_or_coin else pair_or_coin

    if order_type is None:
        order_type = "LIMIT" if price is not None else "MARKET"

    if order_type == 'LIMIT' and price is None:
        print("Error: LIMIT orders require 'price'.")
        return None

    payload = {
        'pair': pair,
        'side': side.upper(),
        'type': order_type.upper(),
        'quantity': str(quantity)
    }
    if order_type == 'LIMIT':
        payload['price'] = str(price)

    headers, _, total_params = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    try:
        res = requests.post(url, headers=headers, data=total_params)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error placing order: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None


def query_order(order_id=None, pair=None, pending_only=None):
    """Query order history or pending orders."""
    url = f"{BASE_URL}/v3/query_order"
    payload = {}
    if order_id:
        payload['order_id'] = str(order_id)
    elif pair:
        payload['pair'] = pair
        if pending_only is not None:
            payload['pending_only'] = 'TRUE' if pending_only else 'FALSE'

    headers, _, total_params = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    try:
        res = requests.post(url, headers=headers, data=total_params)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying order: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None


def cancel_order(order_id=None, pair=None):
    """Cancel specific or all pending orders."""
    url = f"{BASE_URL}/v3/cancel_order"
    payload = {}
    if order_id:
        payload['order_id'] = str(order_id)
    elif pair:
        payload['pair'] = pair

    headers, _, total_params = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    try:
        res = requests.post(url, headers=headers, data=total_params)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error canceling order: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None


# ------------------------------
# Short Endpoints
# ------------------------------

def short_open(pair, collateral, price=None):
    """
    Open a short position. A short is sized by collateral, not quantity.
    Passing 'price' rests a LIMIT order instead of filling at market.
    """
    url = f"{BASE_URL}/v6/short_open"
    payload = {
        'pair': pair,
        'collateral': str(collateral)
    }
    if price is not None:
        payload['order_type'] = 'LIMIT'
        payload['price'] = str(price)

    headers, _, total_params = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    try:
        res = requests.post(url, headers=headers, data=total_params)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error opening short: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None


def short_close(pair, close_qty=None, close_pct=None):
    """
    Close a short position. Sending no size closes the whole position.
    close_qty takes precedence over close_pct, so send only one of them.
    """
    url = f"{BASE_URL}/v6/short_close"
    payload = {'pair': pair}
    if close_qty is not None:
        payload['close_qty'] = str(close_qty)
    elif close_pct is not None:
        payload['close_pct'] = str(close_pct)

    headers, _, total_params = _get_signed_headers(payload)
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    try:
        res = requests.post(url, headers=headers, data=total_params)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error closing short: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None


def get_short_positions():
    """Get all open short positions with live PnL."""
    url = f"{BASE_URL}/v6/short_positions"
    headers, payload, _ = _get_signed_headers({})
    try:
        res = requests.get(url, headers=headers, params=payload)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting short positions: {e}")
        print(f"Response text: {e.response.text if e.response else 'N/A'}")
        return None


# ------------------------------
# Quick Demo Section
# ------------------------------
if __name__ == "__main__":
    print("\n--- Checking Server Time ---")
    print(check_server_time())

    print("\n--- Getting Exchange Info ---")
    info = get_exchange_info()
    if info:
        print(f"Available Pairs: {list(info.get('TradePairs', {}).keys())}")

    print("\n--- Getting Market Ticker (BTC/USD) ---")
    ticker = get_ticker("BTC/USD")
    if ticker:
        print(ticker.get("Data", {}).get("BTC/USD", {}))

    print("\n--- Getting Account Balance ---")
    print(get_balance())

    print("\n--- Checking Pending Orders ---")
    print(get_pending_count())

    # Uncomment these to test trading actions:
    # print(place_order("BTC", "BUY", 0.01, price=95000))  # LIMIT
    print(place_order("BNB/USD", "BUY", 1))      
    print(place_order("BNB/USD", "SELL", 1))             # MARKET       
    print(query_order(pair="BNB/USD", pending_only=False))
    # print(cancel_order(pair="BNB/USD"))

    print("\n--- Getting Short Positions ---")
    print(get_short_positions())

    # Uncomment these to test shorting actions:
    # print(short_open("BTC/USD", 1000))                 # MARKET short, $1000 collateral
    # print(short_open("BTC/USD", 1000, price=62500))    # LIMIT short, rests until filled
    # print(short_close("BTC/USD", close_pct=50))        # close half
    # print(short_close("BTC/USD"))                      # close the rest


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
