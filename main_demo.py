# -*- coding:utf-8 -*-
# 这是对viabtd.com的API进行的封装。
# author: LucasPHBS
# update: 20170811
##
from __future__ import unicode_literals
from TradeVIABTC import ViabtcOrder as Order
from TradeVIABTC import ViabtcData as Data

##
# 记录我的ID和KEY
access_id = "*******"
secret_key = "***************"
##
Data.get_current_data()

##
Data.get_candles()

##
Data.get_market_depth()

##
Data.get_deals()

##
order = Order(access_id, secret_key)

##
order.get_account_info()

##
order.get_unfinished_orders()

##
order.get_finished_orders()

##
order.get_order_status(order_id=123455)

##
order.order_limit("buy", amount=0.01, price=1100)

##
# 市价订单的amount，buy是金额，这是唯一特殊的一个
order.order_market("buy", amount=100)

##
order.order_withdraw(order_id=17623215)