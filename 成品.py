import twstock
import time
import requests
from datetime import datetime

def LINENotify(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    notify = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return notify.status_code

def sendline(stock_id, realprice, token):
    message = f'股票 {stock_id} 的目前股價: {realprice} 元'
    code = LINENotify(token, message)
    if code == 200:
        print(f'訊息發送成功：{message}')
    else:
        print(f'訊息發送失敗：{message}')
    return code

def is_within_trading_hours():
    now = datetime.now()
    start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = now.replace(hour=13, minute=30, second=0, microsecond=0)
    return start_time <= now <= end_time

token = 'egTfTYmc4JpudoG5sy32yKkXEsEN3X3074jG5AETsjC'  # 權杖
stock_ids = ['1519', '6869', '8028','1785']  # 要監控的股票代碼列表
counterError = 0

print('程式開始執行')
while True:
    if is_within_trading_hours():
        for stock_id in stock_ids:
            realdata = twstock.realtime.get(stock_id)
            if realdata['success']:
                realprice = realdata['realtime']['latest_trade_price']  # 目前股價
                if realprice is not None:
                    realprice = float(realprice)
                    sendline(stock_id, realprice, token)
                else:
                    print(f'無法獲取股票 {stock_id} 的最新股價')
            else:
                print(f'twstock 讀取股票 {stock_id} 錯誤, 錯誤原因: {realdata["rtmessage"]}')
                counterError += 1
                if counterError >= 3:
                    print('程式結束')
                    break
    else:
        print('不在交易時間內，程式暫停運行')

    for i in range(300):  # 每5分鐘運行一次
        time.sleep(1)
