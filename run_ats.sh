#!/bin/bash

# bash ~/z_mac/ws_python/ats_prod/run_ats.sh DEV
# bash ~/z_mac/ws_python/ats_prod/run_ats.sh PROD 64552937
ENV=$1
account=${2:-"68112231"}  # 첫 번째 인자를 account로 사용

if [ "$ENV" == 'DEV' ]; then
 source /opt/anaconda3/etc/profile.d/conda.sh
 conda activate ats_prod_py39
 cd ~/z_mac/github/action_ib
fi

# account 값에 따라 APP_KEY를 설정합니다.
case "$account" in
  "68112231")
    DEPOSIT=34111
    PARTITIONS=40
    THRESHOLD=12
    TICKER="NAIL"
    ;;
  "64552937")  # TO-DO: 해당 계좌 사용 안 할 예정이라 구조 바꿔야 함
    sleep 90
    account="68112231"
    DEPOSIT=23087
    PARTITIONS=40
    THRESHOLD=12
    TICKER="SOXL"
    ;;
  *)
    echo "Invalid account. Please specify a valid account."
    exit 1
    ;;
esac

python3 main.py --env "$ENV" --account "$account" --deposit $DEPOSIT --partitions $PARTITIONS --threshold $THRESHOLD --ticker $TICKER

if [ "$ENV" == 'DEV' ]; then
 conda deactivate
fi
