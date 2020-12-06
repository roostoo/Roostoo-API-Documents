# RoostooPartnerAPI

# API SERVICE

* REST API URL: `https://mock-api.roostoo.com`

* [Python Demo](partner_python_demo.py)

- [RoostooPartnerAPI](#roostoopartnerapi)
- [API SERVICE](#api-service)
- [Important](#important)
  - [Partner API_KEY & SECRET_KEY](#partner-api_key--secret_key)
  - [RCL_TopLevelCheck (SIGNED) Endpoint security](#rcl_toplevelcheck-signed-endpoint-security)
  - [Timing security](#timing-security)
  - [SIGNED Endpoint Examples for POST `/v2/gen_join_code`](#signed-endpoint-examples-for-post-v2gen_join_code)
    - [Example 1: As a request body (POST endpoint)](#example-1-as-a-request-body-post-endpoint)
    - [Example 2: As a query string (GET endpoint)](#example-2-as-a-query-string-get-endpoint)
- [API for Roostoo Partner](#api-for-roostoo-partner)
  - [Add one-time-join-code](#add-one-time-join-code)
  - [Add multi one-time-join-code](#add-multi-one-time-join-code)
  - [Get Leader Board information](#get-leader-board-information)
  - [Create API Key Pair for User](#create-api-key-pair-for-user)

# Important


## Partner API_KEY & SECRET_KEY 

This pair of keys will generate and send when Roostoo offer you partner promission

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

## SIGNED Endpoint Examples for POST `/v2/gen_join_code`
Here is a step-by-step example of how to send a vaild signed payload from the
Linux command line using `echo`, `openssl`.

Key | Value
------------ | ------------
apiKey | USEAPIKEYASMYID
secretKey | S1XP1e3UZj6A7H5fATj0jNhqPtmdSJYdInClVN65XAbvqqMKjVHjA7PZj4W12oep


Parameter | Value
------------ | ------------
bind_email | lzhao302@usc.edu
timestamp | 1579870368000

### Example 1: As a request body (POST endpoint)

* **sortParamsByKey, connect with their value by `=` and connect each param by `&`:** bind_email=lzhao302@usc.edu&timestamp=1579870392000

* **requestBody:** bind_email=lzhao302@usc.edu&timestamp=1579870392000
* **HMAC SHA256 signature:**

    ```
    [linux]$ echo -n "bind_email=lzhao302@usc.edu&timestamp=1579870392000" | openssl dgst -sha256 -hmac "S1XP1e3UZj6A7H5fATj0jNhqPtmdSJYdInClVN65XAbvqqMKjVHjA7PZj4W12oep"
    (stdin)= a55766cece32a0db944bfc8e94ddfbcbfc65cd7d1c497aa891d0a2326ba67dcb
    ```

So:
* **Http Header:**:
`Content-Type` = `application/x-www-form-urlencoded`
`RST-API-KEY` = `USEAPIKEYASMYID`
`MSG-SIGNATURE` = `a55766cece32a0db944bfc8e94ddfbcbfc65cd7d1c497aa891d0a2326ba67dcb`

### Example 2: As a query string (GET endpoint)
* **queryString:** bind_email=lzhao302@usc.edu&timestamp=1579870392000
* **HMAC SHA256 signature:**

    ```
    [linux]$ echo -n "bind_email=lzhao302@usc.edu&timestamp=1579870392000" | openssl dgst -sha256 -hmac "S1XP1e3UZj6A7H5fATj0jNhqPtmdSJYdInClVN65XAbvqqMKjVHjA7PZj4W12oep"
    (stdin)= a55766cece32a0db944bfc8e94ddfbcbfc65cd7d1c497aa891d0a2326ba67dcb
    ```

So:
* **Http Header:**:
`RST-API-KEY` = `USEAPIKEYASMYID`
`MSG-SIGNATURE` = `a55766cece32a0db944bfc8e94ddfbcbfc65cd7d1c497aa891d0a2326ba67dcb`


# API for Roostoo Partner


## Add one-time-join-code

```
POST /v2/gen_join_code
Auth RCL_TopLevelCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING_OF_INT | YES | Used with 13-digits millsecomd timestamp
bind_email | STRING | NO | `Used with email address for locking user. (None) means the first user who entry this code can use it. (With email) means the the first specific user who register Roostoo APP with this email address can use it.`

**Response if success**
```json
{
  "Success": true,
  "ErrMsg": "",
  "NewJoinCode": "wYrNLjYNpKM6rNFbTs",
  "ExpireTS": 1579870392,
  "BindEmail": "lzhao302@usc.edu"
}
```

**Response if fail**
```json
{
  "Success": false,
  "ErrMsg": "you do not have this permission",
  "NewJoinCode": "",
  "ExpireTS": 0,
  "BindEmail": ""
}
```


**Return Explain**

Name | Type | Description
------------ | ------------ | ------------
Success | BOOL | Indicates is this request success
ErrMsg | STRING | Error message, if "" means it's passed(Success=true), othervice it tells you about problem.
NewJoinCode | STRING | The random string which is used for join your competition. 
ExpireTS | STRING | The 10-digits second timestamp which marks the competition end time.
BindEmail | STRING | Same as your passed `bind_email` parameter.


Other info:

* None



## Add multi one-time-join-code

```
POST /v2/gen_multi_join_code
Auth RCL_TopLevelCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING_OF_INT | YES | Used with 13-digits millsecomd timestamp
number | STRING | YES | number of code you need, must within 1~50

**Response if success**
```json
{
  "Success": true,
  "ErrMsg": "",
  "Codes": [
    {
      "NewJoinCode": "7VCP3JQRUQM7ND5WNA",
      "ExpireTS": 1596436053
    },
    {
      "NewJoinCode": "UPXXJAEINCNMMR9N05",
      "ExpireTS": 1596436053
    },
    {
      "NewJoinCode": "KW1IIPTVTPAAYEI75E",
      "ExpireTS": 1596436053
    },
    {
      "NewJoinCode": "VBHY12RJSU9PRA1NZW",
      "ExpireTS": 1596436053
    },
    {
      "NewJoinCode": "4S9PQGYPYSLXNACSNQ",
      "ExpireTS": 1596436053
    }
  ]
}
```


**Return Explain**

Name | Type | Description
------------ | ------------ | ------------
Success | BOOL | Indicates is this request success
ErrMsg | STRING | Error message, if "" means it's passed(Success=true), othervice it tells you about problem.
NewJoinCode | STRING | The random string which is used for join your competition. 
ExpireTS | STRING | The 10-digits second timestamp which marks the competition end time.


Other info:

* Please note that you cannot bind code for spicific email



## Get Leader Board information

```
GET /v2/leader_board
Auth RCL_TopLevelCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING_OF_INT | YES | Used with 13-digits millsecomd timestamp
lb_level | STRING | NO | `Used with OVERALL/24HOURS/7DAYS/30DAYS, the default is OVERALL`

**Response**

```json
{
  "Success": true,
  "ErrMsg": "",
  "Level":"OVERALL",
  "LastUpdate": 1579871672843,
  "UpdateInterval": 5,
  "PublicRank": [
    {
      "Rank": 1,
      "UserCode": "XX1",
      "JoinCode": "xxxxxxxx",
      "Email": "zh***@usc.edu",
      "DisplayName": "",
      "CountryCode": "US",
      "PhotoURL": "",
      "InitBal": 50000,
      "CurrBal": 98623.87,
      "TradeVolume": 379807.14,
      "Profit": 0.9725
    },
    {
      "Rank": 2,
      "UserCode": "XX2",
      "JoinCode": "xxxxxxxx",
      "Email": "na***@gmail.com",
      "DisplayName": "",
      "CountryCode": "US",
      "PhotoURL": "",
      "InitBal": 50000,
      "CurrBal": 64175.54,
      "TradeVolume": 56469.05,
      "Profit": 0.2835
    },
    {
      "Rank": 3,
      "UserCode": "XX3",
      "JoinCode": "xxxxxxxx",
      "Email": "dy***@gmail.com",
      "DisplayName": "",
      "CountryCode": "",
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
JoinCode | STRING | The code user used when join this competition.
DisplayName | STRING | The display name which is set by user OR auto set by OAUTH provider, such as Google OAuth. It could be "" if it is not set.
CountryCode | STRING | ISO-3166 2-alpha uppercase country code, it could be empty.
PhotoURL | STRING | The URL for user photo which is set by user or OAuth provider. It could be "" if it is not set.
InitBal | FLOAT | The user's wallet when join this competition (unit: USD).
CurrBal | FLOAT | The user's wallet when last update time of leader board (unit: USD).
TradeVolume | FLOAT | The user's total trade volume during this competition (unit: USD).
Profit | FLOAT | User profit change since the competition began. (CurrBal-InitBal) / InitBal


Other info:

* The total amount of rank list length is the count of participants but no more than 100.
* `TotalProfit = 0.0070` means the user total wallet value `increase 0.07%`.
* `Profit24hr = -0.0107` means the user total wallet value `drop 1.07%`.
* You can get country flag image from `https://static.roostoo.com/national-flag/{LowercaseCountryCode}.png` (provide by CDN fast network)
* `lb_level` please make sure the competition has the specific level, everyone will have `OVERALL`. Other levels are not guaranteed.




## Create API Key Pair for User

```
POST /v2/create_api
Auth RCL_TopLevelCheck
```

**Parameters**

Name | Type | Mandatory | Description
------------ | ------------ | ------------ | ------------
timestamp | STRING_OF_INT | YES | Used with 13-digits millsecomd timestamp
email | STRING | YES | user's email address

**Response**

```json
{
  "Success": true,
  "ErrMsg": "",
  "APIKey": "64lengthKEY",
  "APISecret": "64lengthSecret"
}

```

**Response if fail**
```json
{
  "Success": false,
  "ErrMsg": "your partner access is terminated",
  "APIKey": 0,
  "APISecret": 0
}
```
