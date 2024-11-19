from enum import Enum

#

import apis.kis as kis


TRADE_COST = 0.25  # 거래 수수료

class OrderType(Enum):
    LIMIT = "00"
    LOC = "34"

class Currency(Enum):
    USD = "02"
    KRW = "01"


# api 호출 하기 전 초기 값 세팅
def set_init_api_params(env, account_num, appkey, appsecret):

    base_url = "https://openapivts.koreainvestment.com:29443" if env == 'DEV' else "https://openapi.koreainvestment.com:9443"
    account_num = "50116567" if env == 'DEV' else account_num

    return {
        'BASE_URL': base_url,
        'ACCOUNT_NUM': account_num,
        'APPKEY': appkey,
        'APPSECRET': appsecret,
        'TOKEN': kis.generate_token(base_url, appkey, appsecret),
        'HASH': kis.generate_hashkey(base_url, appkey, appsecret, account_num)
    }

# 무매법 시작하기 전 초기 설정 값 세팅
def set_init_invest_params(init_deposit, num_buy_partitions, sell_threshold_percentage):

    purchase_amount = init_deposit/num_buy_partitions

    return {
        'INIT_DEPOSIT': init_deposit,                               # 원금
        'NUM_BUY_PARTITIONS': num_buy_partitions,                   # 분할
        'PURCHASE_AMOUNT': purchase_amount,                         # 1일 매수 금
        'SELL_THRESHOLD_PERCENTAGE': sell_threshold_percentage,     # 매도 지점
    }
