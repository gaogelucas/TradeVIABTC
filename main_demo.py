##
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from ViabtcAPI import ViabtcOrder as Order
from ViabtcAPI import ViabtcData as Data
from TradeTools import DataStore as DS
import time
##
# 记录我的ID和KEY
access_id = "*******"
secret_key = "***************"
##

def refresh_and_restore_candles():
    DS.refresh_data_in_all_markets()


##


if __name__ == "__main__":
    while 1:  # 出问题后已经会自动刷新了，不需要重写自动刷新业务
        refresh_and_restore_candles()
        print "######################################## "
        time.sleep(1800)
