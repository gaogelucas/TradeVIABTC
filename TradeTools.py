# -*- coding:utf-8 -*-
# 这是对viabtd.com的API进行的封装。
# author: LucasPHBS
# update: 20170811

##
from __future__ import unicode_literals
from ViabtcAPI import ViabtcData as Data
from ViabtcAPI import ViabtcOrder as Order
import numpy as np
import pandas as pd
import talib
import time


##
class DataStore(object):

    def __init__(self):
        self.__data_types = ["1min", "3min", "15min", "30min", "1hour",
                             "2hour", "4hour", "6hour", "12hour", "1day", "3day", "1week"]
        self.__markets = ["BTCCNY", "BCCCNY", "BCCBTC", "LTCCNY", "ETHCNY", "ZECCNY", "148ETH"]

    __data_types = ["1min", "3min", "15min", "30min", "1hour",
                  "2hour", "4hour", "6hour", "12hour", "1day", "3day", "1week"]

    __markets = ["BTCCNY", "BCCCNY", "BCCBTC", "LTCCNY", "ETHCNY", "ZECCNY", "148ETH"]

    # 1. 储存数据的单次方法
    @staticmethod
    def store_data(data_type, market="BCCCNY"):
        """

        :param data_type:

            1min : 1分钟；
            3min:3分钟；
            5min : 5分钟;
            15min:15分钟；
            30min:30分钟；
            1hour:1小时；
            2hour:2小时；
            4hour:4小时；
            6hour:6小时；
            12hour:12小时；
            1day:1日；
            3day:3日；
            1week:1周；

        :param market: one from market list
        :return:
        """
        target = "data/" + market + "_" + data_type + ".csv"

        # 得到最新的从老到新排列的数据
        candles = Data.get_candles(type=data_type, market=market).get("data")
        candles_df = pd.DataFrame(candles,
                                  columns=["time", "open", "close", "high", "low", "vol"])

        # 得到过去从老到新排列的数据
        try:
            # 如果老数据存在
            old_candles_df = pd.DataFrame.from_csv(target)
            merge_candles = pd.concat([old_candles_df, candles_df])
            csv = merge_candles.drop_duplicates("time", keep="first").reset_index(drop=True)
            print len(csv)
            csv.to_csv(target)
        except:
            # 如果老数据不存在
            print "1st time to store data, just create one."
            csv = candles_df
            print len(csv)
            csv.to_csv(target)

    # 2. 下载数据的持续化方法
    @staticmethod
    def collect_data(data_type, sleeptime, market="BCCCNY"):
        try:
            while 1:
                DataStore.store_data(data_type=data_type, market=market)
                time.sleep(sleeptime)
        except:
            print "something wrong, retry in 5 seconds"
            time.sleep(5)
            DataStore.collect_data(data_type=data_type, market=market)

    # 3. 将数据刷新一次
    @staticmethod
    def refresh_data_in(market="BCCCNY"):
        for i in DataStore.__data_types:
            print "\n# refreshing " + i + " data in " + market + " market #"
            DataStore.store_data(data_type=i, market=market)
        print "\n# " + market + " data-refresing done."

    # 4. 将全部市场数据都刷新一次
    @staticmethod
    def refresh_data_in_all_markets():
        for market in DataStore.__markets:
            DataStore.refresh_data_in(market=market)


##
DataStore.refresh_data_in_all_markets()