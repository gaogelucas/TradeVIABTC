# -*- coding:utf-8 -*-
# 这是对ITCHAT的调用。
# author: LucasPHBS
# update: 20170811

##
import itchat
import time
import TradeVIABTC

##

time_format = "%Y-%m-%d %X"


def send_last_price():
    last_last_price = 0
    while 1:
        try:
            last_price = float(TradeVIABTC.ViabtcData.get_current_data()
                               .get("data")
                               .get("ticker")
                               .get("last"))
            last_last_price = last_price
        except:
            last_price = last_last_price

        current_time = time.strftime(time_format, time.localtime())
        current_price = u" || 当前价格为: ￥" + str(last_price)
        return_ratio = u" || 投资收益率为：%.2f%%" % ((last_price / 2080 - 1) * 100)

        msg = current_time + current_price + return_ratio
        print msg

        itchat.send(msg, 'filehelper')
        time.sleep(30)

##

itchat.auto_login(hotReload=True)

##
send_last_price()