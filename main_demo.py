##
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from ViabtcAPI import ViabtcOrder as Order
from ViabtcAPI import ViabtcData as Data
from ViabtcAPI import ViabtcAutotrade as Auto
from TradeTools import DataStore as DS
import time

# 记录我的ID和KEY
access_id = "******"
secret_key = "******"

#
# if __name__ == "__main__":
#     while 1:  # 出问题后已经会自动刷新了，不需要重写自动刷新业务
#         refresh_and_restore_candles()
#         print "######################################## "
#         time.sleep(1800)


order = Order(access_id, secret_key)
ltc = Auto(access_id, secret_key, "LTCCNY")
bcc = Auto(access_id, secret_key, "BCCCNY")
btc = Auto(access_id, secret_key, "BTCCNY")

#
# def moving_losing_stop():
#     try:
#         top_price = 0.0
#         last_price = 0.0
#
#         while 1:
#             time.sleep(5)
#
#             bid_price = float(ltc.bid1_price())
#
#             if last_price == 0.0:
#                 last_price = bid_price
#                 top_price = bid_price
#
#             first_price = top_price - 100
#             first_price_2 = top_price - 80
#             second_price = top_price - 200
#             second_price_2 = top_price - 160
#
#             if last_price >= first_price > bid_price >= second_price:
#                 order.sell_market(0.5)
#                 print "回撤100，卖出一半"
#             elif last_price >= second_price > bid_price:
#                 order.sell_market(1)
#                 print "回撤200，全部清仓"
#             elif last_price < second_price_2 <= bid_price < first_price_2:
#                 order.buy_market(0.5)
#                 print "收复距高点160，买回一半"
#             elif last_price < first_price_2 <= bid_price:
#                 order.buy_market(1)
#                 print "收复距高点80，全仓买入"
#             else:
#                 print "Peace."
#
#             if bid_price > top_price:
#                 top_price = bid_price
#
#             last_price = bid_price
#     except:
#         time.sleep(5)
#         print "发生了不好的事情，重新启动"
#         moving_losing_stop()
