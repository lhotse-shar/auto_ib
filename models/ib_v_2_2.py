import math

#

import apis.kis as kis
import common.config as config


# 별포인트 퍼센트로 loc 매수 할 주식 개수
def get_loc_buy_cnt(loc_buy_price, top_buy_price, progress_rate, purchase_amount, remain_deposit):
    loc_buy_cnt = 0

    if loc_buy_price > top_buy_price:
        print("[Warn] LOC 매수 안 합니다.")
    else:
        if progress_rate < 50:  # 전반전
            loc_buy_cnt = math.floor(purchase_amount / 2 / loc_buy_price)
        else:  # 후반전

            if remain_deposit < purchase_amount:
                loc_buy_cnt = math.floor(remain_deposit / loc_buy_price)
            else:
                loc_buy_cnt = math.floor(purchase_amount / loc_buy_price)

    # if loc_buy_cnt <= 0:
    #     raise ValueError("매수 개수가 0이거나 음수입니다.")

    print("[info] LOC 매수 개수: ", loc_buy_cnt)

    return loc_buy_cnt


# 큰 수 매수 할 주식 개수
def get_top_buy_cnt(loc_buy_price, top_buy_price, avg_purchase_price, purchase_amount, remain_deposit, current_quantity):
    top_buy_cnt = 0

    if current_quantity <= 0:
        print("[Warn] 큰수 매수 안합니다.")
        return top_buy_cnt

    if loc_buy_price < top_buy_price:
        print("[Warn] 큰수 매수 안 합니다.")
    else:
        if remain_deposit < purchase_amount:
            top_buy_cnt = math.floor(remain_deposit / top_buy_price)
        else:
            if avg_purchase_price < top_buy_price:
                top_buy_cnt = math.floor(purchase_amount / top_buy_price)
            else:
                top_buy_cnt = math.floor(purchase_amount / 2 / top_buy_price)

    print("[info] 큰수 매수 개수: ", top_buy_cnt)
    return top_buy_cnt


# 평단가로 LOC 매수 걸 주식 개수
def get_avg_buy_cnt(average_purchase_price, loc_buy_price, top_buy_price, progress_rate, purchase_amount, loc_buy_cnt,
                    top_buy_cnt):
    avg_buy_cnt = 0

    if average_purchase_price > top_buy_price:
        print("[Warn] 평단가 매수 안 합니다.")
    else:
        if progress_rate < 50:
            if loc_buy_price < top_buy_price:
                avg_buy_cnt = math.floor(purchase_amount / average_purchase_price) - loc_buy_cnt
            else:
                avg_buy_cnt = math.floor(purchase_amount / average_purchase_price) - top_buy_cnt
        else:
            print("[Warn] 평단가 매수 안 합니다.")

    print("[info] 평단가 매수 개수: ", avg_buy_cnt)
    return avg_buy_cnt


# 매일 계산되는 값
def calc_daily_value(api_values, invest_value):
    sell_threshold_percentage = invest_value['SELL_THRESHOLD_PERCENTAGE']
    num_buy_partitions = invest_value['NUM_BUY_PARTITIONS']
    purchase_amount = invest_value['PURCHASE_AMOUNT']

    present_balance = kis.get_overseas_present_balance(
        api_values['BASE_URL'],
        api_values['TOKEN'],
        api_values['APPKEY'],
        api_values['APPSECRET'],
        api_values['ACCOUNT_NUM'],
        config.Currency.USD.value,
    )

    current_purchase_amount = round(float(present_balance['output1'][0]['frcr_pchs_amt']), 2)  # 현재매입금액
    average_purchase_price = round(float(present_balance['output1'][0]['avg_unpr3']), 2)  # 평단가

    t = math.ceil(current_purchase_amount / purchase_amount * 10) / 10
    if 39 < t <= 40:
        raise print('[Warn] T가 39 초과 40 이하입니다. MOC 매도만 있습니다.')

    progress_rate = t / num_buy_partitions
    print('='*30)
    print("[info] 현재 매입금액(사용한 금액): $", current_purchase_amount)
    print("[info] 현재 평단가: $", average_purchase_price)

    print('=' * 30)
    remain_deposit = round(invest_value['INIT_DEPOSIT'] - current_purchase_amount, 2)
    current_quantity = float(present_balance['output1'][0]['ccld_qty_smtl1'])  # 현재 보유수량
    print("[info] 현재 보유수량: ", current_quantity, '주')
    print("[info] 남은 예수금: ", remain_deposit)
    print("[info] 1일 매수 금액: ", purchase_amount)
    print("[info] 현재 가격: ", present_balance['output1'][0]['ovrs_now_pric1'])

    print('=' * 30)
    print("[info] T: ", t, ' 회차')
    print("[info] PROGRESS_RATE: ", round(progress_rate * 100, 1), "%")

    print('=' * 30)
    star_point_percent = sell_threshold_percentage-t*sell_threshold_percentage/20*(40/num_buy_partitions)
    print("[info] 별포인트 퍼센트: ", star_point_percent, '%')
    loc_buy_price = round(average_purchase_price*(1+star_point_percent/100), 2)
    print("[info] LOC 매수 가격: ", loc_buy_price)
    top_buy_price = round(float(present_balance['output1'][0]['ovrs_now_pric1'])*(1.15), 2)
    print("[info] 큰수 매수 가격: ", top_buy_price)
    loc_sell_price = round(average_purchase_price*(1+(config.TRADE_COST/100)+(star_point_percent/100)), 2)
    print("[info] LOC 매도 가격: ", loc_sell_price)
    sell_threshold_price = round(average_purchase_price*(1+(config.TRADE_COST/100)+(sell_threshold_percentage/100)), 2)
    print("[info] 매도 기준 가격: ", sell_threshold_price)

    print('=' * 30)
    # loc 매수 개수
    loc_buy_cnt = get_loc_buy_cnt(loc_buy_price, top_buy_price, progress_rate, purchase_amount, remain_deposit)

    # 큰수 매수 개수
    top_buy_cnt = get_top_buy_cnt(loc_buy_price, top_buy_price, average_purchase_price,  purchase_amount, remain_deposit, current_quantity)

    # 평단가 매수 개수
    avg_buy_cnt = get_avg_buy_cnt(average_purchase_price, loc_buy_price, top_buy_price, progress_rate, purchase_amount, loc_buy_cnt, top_buy_cnt)


    # 매도 지점
    loc_sell_cnt = int(round(current_quantity/4, 0))
    print("[info] LOC 매도 개수: ", loc_sell_cnt)

    sell_threshold_cnt = int(current_quantity-loc_sell_cnt)
    print("[info] 매도 기준의 매도 개수: ", sell_threshold_cnt)

    return {
        't': t,
        'average_purchase_price': average_purchase_price,
        'remain_deposit': remain_deposit,

        'loc_buy_price': loc_buy_price,
        'top_buy_price': top_buy_price,
        'loc_sell_price': loc_sell_price,
        'sell_threshold_price': sell_threshold_price,

        'loc_buy_cnt': loc_buy_cnt,
        'top_buy_cnt': top_buy_cnt,
        'avg_buy_cnt': avg_buy_cnt,
        'loc_sell_cnt': loc_sell_cnt,
        'sell_threshold_cnt': sell_threshold_cnt,
    }
