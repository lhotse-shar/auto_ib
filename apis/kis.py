import json

import requests

#


def generate_token(baseurl, appkey, appsecret):
    url = baseurl+"/oauth2/tokenP"

    payload = json.dumps({
        "grant_type": "client_credentials",
        "appkey": appkey,
        "appsecret": appsecret
    })
    headers = {
        'content-type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['access_token']

def generate_hashkey(baseurl, appkey, appsecret, account_num):
    url = baseurl+"/uapi/hashkey"

    payload = json.dumps({
        "CANO": account_num,
        "ACNT_PRDT_CD": "01",
        "PDNO": "071050",
        "ORD_DVSN": "01",
        "ORD_QTY": "1",
        "ORD_UNPR": "0"
    })
    headers = {
        'content-type': 'application/json',
        'appkey': appkey,
        'appsecret': appsecret
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['HASH']

# 해외주식 체결기준현재잔고(현재 매입가능 외화잔고를 가져와야하기 때문에 처음에 호출한다.)
def get_overseas_present_balance(baseurl, token, appkey, appsecret, account_num, currency):

    api_name = '해외주식 체결기준현재잔고'

    url = baseurl+f"/uapi/overseas-stock/v1/trading/inquire-present-balance?CANO={account_num}&ACNT_PRDT_CD=01&NATN_CD=840&WCRC_FRCR_DVSN_CD={currency}&TR_MKET_CD=00&INQR_DVSN_CD=00"

    payload = ""
    headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer '+token,
        'appkey': appkey,
        'appsecret': appsecret,
        'tr_id': 'CTRP6504R',
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        # HTTP 오류가 발생하면 예외를 발생시킵니다.
        response.raise_for_status()

        # JSON 응답을 처리하려고 할 때
        data = response.json()

        # API 응답 값이 비어있는지 확인하고, 그렇다면 예외를 발생시킵니다.
        if not data:
            raise ValueError(api_name, " API 결과 값이 없습니다.")

        # 정상적인 응답일 때의 처리 코드
        print(api_name, " API 호출이 성공했습니다:", response)
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"{api_name} HTTP 오류 발생: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"{api_name} 연결 오류 발생: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"{api_name} 타임아웃 오류 발생: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"{api_name} 요청 중 예외 발생: {req_err}")
    except ValueError as val_err:
        print(f"{api_name} 값 오류 발생: {val_err}")
    except Exception as e:
        print(f"{api_name} 알 수 없는 오류 발생: {e}")


# 주문 함수
def post_stock_order(env, baseurl, token, appkey, appsecret, account_num, exchange_cd, ticker, qty, price, buy_or_sell,
                     ord_type):
    url = baseurl + "/uapi/overseas-stock/v1/trading/order"

    if buy_or_sell == "buy":
        tr_id = "VTTT1002U" if env == 'DEV' else "TTTT1002U"
    elif buy_or_sell == "sell":
        tr_id = "VTTT1001U" if env == 'DEV' else "TTTT1006U"

    payload = json.dumps({
        "CANO": account_num,
        "ACNT_PRDT_CD": "01",
        "OVRS_EXCG_CD": exchange_cd,
        "PDNO": ticker,
        "ORD_QTY": qty,
        "OVRS_ORD_UNPR": price,
        "ORD_SVR_DVSN_CD": "0",
        "ORD_DVSN": ord_type
    })
    headers = {
        'content-type': 'application/json',
        'authorization': 'Bearer ' + token,
        'appkey': appkey,
        'appsecret': appsecret,
        'tr_id': tr_id,
        # 'hashkey': hashkey
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    return response.json()
