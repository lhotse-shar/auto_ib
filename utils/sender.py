from datetime import datetime, timedelta
import json

import requests

#


def send_msg_on_success(env, webhook_url, info):
    # DEV or PROD
    channel = "#alarm-ats-result-dev" if env == "DEV" else "#alarm-ats-result-prod"

    # 매수/매도 텍스트 설정
    action_text = ":red_circle: 매수" if info['is_buy'] else ":large_blue_circle: 매도"

    today = (datetime.now() + timedelta(hours=9)).strftime("%Y-%m-%d(%a.) %H:%M:%S")

    # Slack 메시지 블록 구성
    message = {
        "channel": channel,
        "username": "자동무매봇",
        "icon_emoji": ":moneybag:",
        "blocks": [
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*({action_text})[{info['partitions']}분할 {info['t']}회차 주문접수 완료]*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*[{today}]*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*[증권사: {info['broker_name']}]*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*[계좌번호: {info['account_no']}]*"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*종목:* {info['ticker']}"
                    },
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*매수 방법:* {info['order_type']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*주문가:* {info['order_price']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*주문수:* {info['order_quantity']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*현재평단가:* {info['avg_price']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*초기원금:* {info['init_deposit']}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*남은원금:* {info['remain_deposit']}"
                    }
                ]
            }
        ]
    }

    # Slack에 메시지 전송
    response = requests.post(
        webhook_url, data=json.dumps(message),
        headers={'Content-Type': 'application/json'}
    )

    # 응답 확인
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")


def send_msg_on_fail(env, webhook_url, info):
    # DEV or PROD
    channel = "#alarm-ats-result-dev" if env == "DEV" else "#alarm-ats-result-prod"

    # 매수/매도 텍스트 설정
    action_text = ":red_circle: 매수" if info['is_buy'] else ":large_blue_circle: 매도"

    today = (datetime.now() + timedelta(hours=9)).strftime("%Y-%m-%d(%a.) %H:%M:%S")

    # Slack 메시지 블록 구성
    message = {
        "channel": channel,
        "username": "자동무매봇",
        "icon_emoji": ":moneybag:",
        "blocks": [
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*({action_text})[{info['partitions']}분할 {info['t']}회차 주문접수 실패]*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*[{today}]*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*[증권사: {info['broker_name']}]*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*[계좌번호: {info['account_no']}]*"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*종목:* {info['ticker']}"
                    },
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*사유:* {info['reason']}"
                    },
                ]
            }
        ]
    }

    # Slack에 메시지 전송
    response = requests.post(
        webhook_url, data=json.dumps(message),
        headers={'Content-Type': 'application/json'}
    )

    # 응답 확인
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message: {response.status_code}, {response.text}")
