# RoostooPartnerAPI

# API SERVICE

* API SERVICE BASED ON GOLANG `gin`

* REST API URL: `https://mock-api.roostoo.com`

* [Python Demo](python_demo.py)


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

## SIGNED Endpoint Examples for POST `/v2/add_join_code`
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


## Add ont-time-join-code

```
POST /v2/add_join_code
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


## Get Leader Board information

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
DisplayName | STRING | The display name which is set by user OR auto set by OAUTH provider, such as Google OAuth. It could be "" if it is not set.
PhotoURL | STRING | The URL for user photo which is set by user or OAuth provider. It could be "" if it is not set.
InitBal | FLOAT | The user's wallet when join this competition (unit: USD).
CurrBal | FLOAT | The user's wallet when last update time of leader board (unit: USD).
TradeVolume | FLOAT | The user's total trade volume during this competition (unit: USD).
Profit | FLOAT | User profit change since the competition began. (CurrBal-InitBal) / InitBal


Other info:

* The total amount of rank list length is the count of participants but no more than 100.
* `TotalProfit = 0.0070` means the user total wallet value `increase 0.07%`.
* `Profit24hr = -0.0107` means the user total wallet value `drop 1.07%`.