# -*- coding:utf-8 -*-
# 这是对viabtd.com的API进行的封装。
# author: LucasPHBS
# update: 20170811

##
from __future__ import unicode_literals
import urllib2
import json
import hashlib
# viabtc给出的请求demo和库，用于POST和DELETE请求
# https://github.com/viabtc/viabtc_exchange_cn_api_cn
from oauth import RequestClient
import time
import os
import multiprocessing
##


# 行情数据函数集 ViabtcData
class ViabtcData(object):
    """
        调用行情数据的静态方法集，不需要也不可以实例化。

        # 1. 获取当前的行情数据
        @staticmethod
        get_current_data(market="BCCCNY", header=_header)

        # 2. 获取当前的委托行情
        @staticmethod
        get_market_depth(market="BCCCNY", merge=1, limit=10, header=_header)

        # 3. 获取K线信息
        @staticmethod
        get_candles(market="BCCCNY", type="15min", header=_header)

        # 4. 获取最新成交数据
        @staticmethod
        get_deals(market="BCCCNY", last_id=0, header=_header)
    """
    # 记录请求头中的User-Agent信息
    # 若要修改请求头信息，请直接在函数中修改header=""参数
    _header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/39.0.2171.71 Safari/537.36",
               "Content-Type": "application/json"}

    # 初始化
    def __init__(self):
        self.markets = ["BTCCNY", "BCCCNY", "BCCBTC", "LTCCNY", "ETHCNY", "ZECCNY", "148ETH"]

    markets = ["BTCCNY", "BCCCNY", "BCCBTC", "LTCCNY", "ETHCNY", "ZECCNY", "148ETH"]

    # 1. 获取当前的行情数据
    @staticmethod
    def get_current_data(market="BCCCNY", header=_header):
        """ (market:str, header:str) -> dict

        获取当前的市场信息，返回一个Json dict。

        :param market: str, ="BCCCNY"
            市场代码，可选：
            ["BCCCNY", "BTCCNY", "LTCCNY", "ETHCNY", "ZECCNY"]

        :param header: 默认载入头文件

        :return: current_data: dict,
            代表市场数据的Json数据集，形如：
            {
                u'code': 0,
                u'data':
                {
                    u'date': 1502443868201,  #时间戳
                    u'ticker':
                    {
                        u'buy': u'2073',                 #最近买单价格
                        u'high': u'2099',                #最近卖单价格
                        u'last': u'2083.36',             #最近成交价格
                        u'low': u'1836.66',              #当日最低价格
                        u'sell': u'2083.36',             #最近卖单价格
                        u'vol': u'7740.9045'
                    }
                },          #当日成交量
                u'message': u'Ok'
             }
        """

        # 行情数据链接
        url = "https://www.viabtc.com/api/v1/market/ticker?market=" + market
        # 请求并读取行情数据
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        # 解析行情数据
        current_data = json.loads(response)
        # 返回行情数据
        return current_data

    # 2. 获取当前的委托行情
    @staticmethod
    def get_market_depth(market="BCCCNY", merge=0, limit=100, header=_header):
        """ (market:str, merge:int, limit:int, header:str) -> dict

        获取当前的委托行情

        :param market: str, ="BCCCNY"
            市场代码，可选：
            ["BCCCNY", "BTCCNY", "LTCCNY", "ETHCNY", "ZECCNY"]

        :param merge: int,
            合并深度，可选：
            {
                BTCCNY:0/1/5/10,
                BCCCNY:0/1/5/10,
                ETHCNY:0/0.1/1/5,
                ETHBTC:0/0.00001/0.0001/0.0005
            }

        :param limit: int,
            最多返回几档行情，可选1/5/10/20/30/50/100。

        :param header: 默认载入头文件

        :return: market_depth: dict,
            返回档口行情，形如：
            {
                u'code': 0,
                u'data':
                {
                    u'asks':
                    [
                        [u'2150', u'8.97'],
                        [u'2151', u'0.0928'],
                        [u'2153', u'0.232'],
                        [u'2156', u'0.0463'],
                        [u'2161', u'0.0462'],
                        [u'2177', u'3'],
                        [u'2187', u'9'],
                        [u'2188', u'2'],
                        [u'2189', u'4.568'],
                        [u'2191', u'3.7172']
                    ],
                    u'bids':
                    [
                        [u'2135', u'4.5468'],
                        [u'2130', u'17.3888'],
                        [u'2116', u'2.2104'],
                        [u'2100', u'8.385'],
                        [u'2099', u'2.7049'],
                        [u'2086', u'0.2094'],
                        [u'2061', u'63.0788'],
                        [u'2055', u'32.8939'],
                        [u'2053', u'0.575'],
                        [u'2050', u'36.7207']
                    ]
                },
                u'message': u'Ok'
            }
        """

        # 委托行情链接
        url = "https://www.viabtc.com/api/v1/market/depth" \
                           "?market=" + market + \
                           "&limit=" + str(limit) + \
                           "&merge=" + str(merge)
        # 请求并读取行情数据
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        # 解析行情数据
        market_depth = json.loads(response)
        # 返回行情数据
        return market_depth

    # 3. 获取K线信息
    @staticmethod
    def get_candles(market="BCCCNY", type="15min", header=_header):
        """ (market:str, type:str, header:str) -> dict

        获取最近2000条K线数据

        :param market: str, ="BCCCNY"
            市场代码，可选：
            ["BCCCNY", "BTCCNY", "LTCCNY", "ETHCNY", "ZECCNY"]

        :param type: str, 可选如下选项：
            {
                1min : 1分钟,
                3min:3分钟,
                5min : 5分钟,
                15min:15分钟,
                30min:30分钟,
                1hour:1小时,
                2hour:2小时,
                4hour:4小时,
                6hour:6小时,
                12hour:12小时,
                1day:1日,
                3day:3日,
                1week:1周
            }

        :param header: 默认载入头文件

        :return: candles: dic,
        2000条形如这样的数据：
        {
            "code": 0,
            "data": [
                        [
                          1492358400, # 时间
                          "7000.0",   # 开盘
                          "7000.0",   # 收盘
                          "7000.0",   # 最高
                          "7000.0",   # 最低
                          "0"         # 成交量
                        ],
                        [
                          1492358400, # 时间
                          "7000.0",   # 开盘
                          "7000.0",   # 收盘
                          "7000.0",   # 最高
                          "7000.0",   # 最低
                          "0"         # 成交量
                        ]
                    ],
            "message": "Ok"
        }
        """

        # TODO: 找到如何只提取最近的candle数据。

        # K线数据链接
        url = "https://www.viabtc.com/api/v1/market/kline" \
                      "?market=" + market + \
                      "&type=" + type
        # 请求并读取K线数据
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        # 解析K线数据
        candles = json.loads(response)
        # 返回K线数据
        return candles

    # 4. 获取最新成交数据
    @staticmethod
    def get_deals(market="BCCCNY", last_id=0, header=_header):
        """

        获取最近1000条成交记录

        :param last_id: int, =0
            我也没搞明白是干什么用的

        :param market: str, ="BCCCNY"
            市场代码，可选：
            ["BCCCNY", "BTCCNY", "LTCCNY", "ETHCNY", "ZECCNY"]

        :param header: 默认载入头文件

        :return: deals:
            {
              "code": 0,
              "data": [
                {
                  "amount": "0.0001",       # 交易数量
                  "date": 1494214689,       # 交易时间（秒）
                  "date_ms": 1494214689067, # 交易时间（毫秒）
                  "id": 5,                  # 交易编号
                  "price": "7200.00",       # 交易价格
                  "type": "buy"             # 交易类型：主动买、主动卖
                },
                {
                  "amount": "0.0001",       # 交易数量
                  "date": 1494214689,       # 交易时间（秒）
                  "date_ms": 1494214689067, # 交易时间（毫秒）
                  "id": 5,                  # 交易编号
                  "price": "7200.00",       # 交易价格
                  "type": "buy"             # 交易类型：主动买、主动卖
                }
              ],
              "message": "Ok"
            }

        """

        # 成交记录链接
        url = "https://www.viabtc.com/api/v1/market/deals" \
                    "?market=" + market + \
                    "&last_id=" + str(last_id)
        # 请求并读取成交记录数据
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        # 解析成交记录数据
        deals = json.loads(response)
        # 返回成交记录数据
        return deals

##


# 交易系统函数集 ViabtcOrder
class ViabtcOrder(object):
    """
    1. 查询账户信息
    get_account_info(self)

    2. 获取未完成订单列表
    get_unfinished_orders(self, market="BCCCNY", limit=100, page=1)

    3. 获取已完成订单列表
    get_finished_orders(self, market="BCCCNY", limit=100, page=1)

    4. 获取订单状态
    get_order_status(self, order_id, market="BCCCNY")

    5. 下市价单
    order_market(self, order_type, amount, market="BCCCNY")

    6. 下限价单
    order_limit(self, order_type, amount, price, market="BCCCNY")

    7. 撤销订单
    order_withdraw(self, order_id, market="BCCCNY")

    """
    # 记录请求头中的User-Agent信息
    # 若要修改请求头信息，请直接在函数中修改header=""参数
    _header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/39.0.2171.71 Safari/537.36",
               "Content-Type": "application/json",
               "Authorization": ""}

    # 初始化实例需要用到的 Access_ID and Secret_Key
    access_id = ""
    secret_key = ""

    # 最小交易单位
    min_unit = 0.01

    # 初始化
    def __init__(self, acs_id, scr_key):
        self.access_id = acs_id
        self.secret_key = scr_key
        self.markets = ["BTCCNY", "BCCCNY", "BCCBTC", "LTCCNY", "ETHCNY", "ZECCNY", "148ETH"]

    # 制作请求链接
    @staticmethod
    def url(req_url, api, api_list):
        url = req_url

        for key in api_list:

            if key == "secret_key":
                continue

            if url == req_url:
                url += ("?" + key + "=" + api[key])
            else:
                url += ("&" + key + "=" + api[key])

        return url

    # 制作&哈希signature
    @staticmethod
    def signature(api, api_list):
        signature = ""

        for key in api_list:
            if signature == "":
                signature += (key + "=" + api[key])
            else:
                signature += ("&" + key + "=" + api[key])

        md5 = hashlib.md5()
        md5.update(signature)

        signature_md5 = str.upper(md5.hexdigest())

        return signature_md5

    # 1. 查询账户信息
    def get_account_info(self):
        """() -> dict

        获取账户信息

        :return: account_info: dict
            返回账户信息形如：
            {
                 "code": 0,
                 "data": {
                   "BTC": {                     # 比特币账户
                     "available": "13.60109",   # 比特币可用金额
                     "frozen": "0.00000"        # 比特币冻结金额
                   },
                   "CNY": {                     # 人民币账户
                     "available": "32590.16",   # 人民币可用金额
                     "frozen": "7000.00"        # 人民币冻结金额
                   },
                   "ETH": {                     # 以太坊账户
                     "available": "5.06000",    # 以太坊可用金额
                     "frozen": "0.00000"        # 以太坊冻结金额
                   }
                 },
                 "message": "Ok"
            }
        """

        # api信息
        api = {"access_id": self.access_id,
               "secret_key": self.secret_key}
        api_list = ["access_id", "secret_key"]

        # account_info链接
        url = self.url("https://www.viabtc.com/api/v1/balance/", api, api_list)

        # 将签名写入header
        header = self._header
        header["Authorization"] = self.signature(api, api_list)

        # 请求并读取account_info数据
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        # 解析account_info数据
        account_info = json.loads(response)
        # 返回account_info数据
        return account_info

    # 2. 获取未完成订单列表
    def get_unfinished_orders(self, market="BCCCNY", limit=100, page=1):
        """

        获取未完成列表信息

        :param market: 市场类别
        :param limit: 每页打印限制 1-100
        :param page: 从第几页开始 1-
        :return: unfinished_orders，形如：
            {
              "code": 0,
              "data": {
                "count": 1,                   # 当前页行数
                "curr_page": 1,               # 当前页
                "data": [                     # 按下单时间逆序返回,最新下的单，在最前面
                  {
                    "amount": "1.00",         # 委托数量
                    "avg_price": "0.00",      # 平均成交价格
                    "create_time": 1494320533,# 下单时间
                    "deal_amount": "0.001",   # 成交数量
                    "deal_fee": "130.3792",   # 交易手续费用
                    "deal_money": "65189.6",  # 成交金额
                    "id": 32,                 # 订单编号
                    "left": 32,               # 未成交数量
                    "maker_fee_rate": "0",    # maker费率
                    "market": "BTCCNY",       # 市场类型
                    "order_type": "limit",    # 订单类型
                    "price": "7000.00",       # 委托价格
                    "status": "not_deal",     # 订单状态
                    "taker_fee_rate": "0.002",# taker费率
                    "type": "sell"            # 买卖类型
                  }
                ],
                "has_next": true              # 是否有下一页
              },
              "message": "Ok"
            }
        """

        # api信息
        api = {"access_id": self.access_id,
               "limit": str(limit),
               "market": market,
               "page": str(page),
               "secret_key": self.secret_key}
        api_list = ["access_id", "limit", "market", "page", "secret_key"]

        # 链接信息
        url = self.url("https://www.viabtc.com/api/v1/order/pending", api, api_list)

        # 将签名写入header
        header = self._header
        header["Authorization"] = self.signature(api, api_list)

        # 请求并读取数据
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        # 解析数据
        unfinished_orders = json.loads(response)
        # 返回数据
        return unfinished_orders

    # 3. 获取已完成订单列表
    def get_finished_orders(self, market="BCCCNY", limit=100, page=1):
        """

        获取已完成列表信息

        :param market: 市场类别
        :param limit: 每页打印限制 1-100
        :param page: 从第几页开始 1-
        :return: finished_orders，形如：
            {
              "code": 0,
              "data": {
                "count": 1,                   # 当前页行数
                "curr_page": 1,               # 当前页数
                "data": [                     # 按完成(全部成交)时间逆序返回,最新完成的单，在最前面
                   {
                    "amount": "1.00",            # 委托数量
                    "avg_price": "0.00",         # 平均成交价格
                    "create_time": 1494320533,   # 下单时间
                    "deal_amount": "0.001",      # 成交数量
                    "deal_fee": "130.3792",      # 交易手续费用
                    "deal_money": "65189.6",     # 成交金额
                    "finished_time": 1494320533, # 下单时间
                    "id": 32,                    # 订单编号
                    "maker_fee_rate": "0",       # maker费率
                    "market": "BTCCNY",          # 市场类型
                    "order_type": "limit",       # 订单类型
                    "price": "7000.00",          # 委托价格
                    "status": "not_deal",        # 订单状态
                    "taker_fee_rate": "0.002",   # taker费率
                    "type": "sell"               # 买卖类型
                  }
                ],
                "has_next": true              # 是否有下一页
              },
              "message": "Ok"
            }
        """

        # api信息
        api = {"access_id": self.access_id,
               "limit": str(limit),
               "market": market,
               "page": str(page),
               "secret_key": self.secret_key}
        api_list = ["access_id", "limit", "market", "page", "secret_key"]

        # 链接信息
        url = self.url("https://www.viabtc.com/api/v1/order/finished", api, api_list)

        # 将签名写入header
        header = self._header
        header["Authorization"] = self.signature(api, api_list)

        # 请求并读取数据
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        # 解析数据
        finished_orders = json.loads(response)
        # 返回数据
        return finished_orders

    # 4. 获取订单状态
    def get_order_status(self, order_id, market="BCCCNY"):
        """

        :param order_id: 从订单中获取的一串数字信息
        :param market: 市场列表
        :return: order_status，形如：
            {
              "code": 0,
              "data": {                           # 订单数据
                "amount": "1000",                 # 委托数量
                "avg_price": "11782.28",          # 平均成交价格
                "create_time": 1496761108,        # 下单时间
                "deal_amount": "1000",            # 成交数量
                "deal_fee": "23564.5798468",      # 交易手续费用
                "deal_money": "11782289.9234",    # 成交金额
                "id": 300021,                     # 订单编号
                "left": "9.4",                    # 未成交数量
                "maker_fee_rate": "0.001",        # maker费率
                "market": "BTCCNY",               # 市场
                "order_type": "limit",            # 委托类型
                "price": "7000",                  # 委托价格
                "status": "done",                 # 订单状态
                "taker_fee_rate": "0.002",        # taker费率
                "type": "sell"                    # 订单类型
                }
              },
              "message": "Ok"
            }
        """

        # api信息
        api = {"access_id": self.access_id,
               "id": str(order_id),
               "market": market,
               "secret_key": self.secret_key}
        api_list = ["access_id", "id", "market", "secret_key"]

        # 链接信息
        url = self.url("https://www.viabtc.com/api/v1/order/", api, api_list)

        # 将签名写入header
        header = self._header
        header["Authorization"] = self.signature(api, api_list)

        # 请求并读取数据
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        # 解析数据
        order_status = json.loads(response)
        # 返回数据
        return order_status

    # 5. 下市价单
    def order_market(self, order_type, amount, market="BCCCNY"):
        """

        下市价单

        :param order_type: "buy" or "sell"
        :param amount: > 0.01               #市价单时，sell的amount是数量，buy的amount是金额。
        :param market: one from market list
        :return:
        {
          "code": 0,
          "data": {
            "amount": "56.5",              # 委托数量
            "avg_price": "11641.3",        # 平均成交价格
            "create_time": 1496798479,     # 下单时间
            "deal_amount": "56.5",         # 成交数量
            "deal_money": "657733.4561",   # 成交金额
            "id": 300032,                  # 订单编号
            "left": "0",                   # 未成交数量
            "maker_fee_rate": "0",         # maker手续费率
            "market": "BTCCNY",            # 市场
            "order_type": "market",        # 委托类型：limit:限价单；market:市价单；
            "price": "0",                  # 委托价格
            "source_id": "123",            # 用户自定义编号
            "status": "done",              # 订单状态：done:已成交；part_deal:部分成交；not_deal:未成交；
            "taker_fee_rate": "0.002",     # taker手续费率
            "type": "sell"                 # 订单类型：sell:卖出订单；buy:买入订单；
          },
          "message": "Ok"
        }
        """
        request_client = RequestClient(
            access_id=self.access_id,
            secret_key=self.secret_key
        )

        data = {
            "amount": str(amount),
            "type": order_type,
            "market": market
        }

        result = request_client.request(
            'POST',
            'https://www.viabtc.com/api/v1/order/market',
            json=data,
        )
        return result.json()

    # 6. 下限价单
    def order_limit(self, order_type, amount, price, market="BCCCNY"):
        """

        下限价单

        :param order_type: "buy" or "sell"
        :param amount: > 0.01               #限价单时，amount一直表示数量。
        :param price: > 0
        :param market: one from market list
        :return:
        {
          "code": 0,
          "data": {
            "amount": "56.5",              # 委托数量
            "avg_price": "11641.3",        # 平均成交价格
            "create_time": 1496798479,     # 下单时间
            "deal_amount": "56.5",         # 成交数量
            "deal_fee": "1315.4669122",    # 交易手续费用
            "deal_money": "657733.4561",   # 成交金额
            "id": 300032,                  # 订单编号
            "left": "0",                   # 未成交数量
            "maker_fee_rate": "0.001",     # maker手续费率
            "market": "BTCCNY",            # 市场
            "order_type": "limit",         # 委托类型：limit:限价单；market:市价单；
            "price": "7000",               # 委托价格
            "source_id": "123",            # 用户自定义编号
            "status": "done",              # 订单状态：done:已成交；part_deal:部分成交；not_deal:未成交；
            "taker_fee_rate": "0.002",     # taker手续费率
            "type": "sell"                 # 订单类型：sell:卖出订单；buy:买入订单；
          },
          "message": "Ok"
        }
        """
        request_client = RequestClient(
            access_id=self.access_id,
            secret_key=self.secret_key
        )

        data = {
            "amount": str(amount),
            "price": str(price),
            "type": order_type,
            "market": market
        }

        result = request_client.request(
            'POST',
            'https://www.viabtc.com/api/v1/order/limit',
            json=data,
        )
        return result.json()

    # 7. 撤销订单
    def order_withdraw(self, order_id, market="BCCCNY"):
        """
        撤销订单
        :param order_id: 需要提前获取订单id
        :param market: 市场代码
        :return:
        {
          "code": 0,
          "data": {
            "amount": "56.5",              # 委托数量
            "avg_price": "11641.3",        # 平均成交价格
            "create_time": 1496798479,     # 下单时间
            "deal_amount": "56.5",         # 成交数量
            "deal_fee": "1315.4669122",    # 交易手续费用
            "deal_money": "657733.4561",   # 成交金额
            "id": 300032,                  # 订单编号
            "left": "0",                   # 未成交数量
            "maker_fee_rate": "0.001",     # maker手续费率
            "market": "BTCCNY",            # 市场
            "order_type": "limit",         # 委托类型：limit:限价单；market:市价单；
            "price": "7000",               # 委托价格
            "source_id": "123",            # 用户自定义编号
            "status": "done",              # 订单状态：done:已成交；part_deal:部分成交；not_deal:未成交；
            "taker_fee_rate": "0.002",     # taker手续费率
            "type": "sell"                 # 订单类型：sell:卖出订单；buy:买入订单；
          },
          "message": "Ok"
        }
        """
        request_client = RequestClient(
            access_id=self.access_id,
            secret_key=self.secret_key
        )

        data = {
            "order_id": str(order_id),
            "market": market
        }

        result = request_client.request(
            'DELETE',
            'https://www.viabtc.com/api/v1/order/pending',
            json=data,
        )
        return result.json()

    # #####高级指令#####
    def withdraw_all(self, market="BCCCNY"):
        uo = self.get_unfinished_orders(market=market)
        ids = [i.get("id") for i in uo.get("data").get("data")]
        if not ids:
            print "no unfinished orders"
        else:
            for i in ids:
                self.order_withdraw(i, market=market)
            print "order_withdraw done."

    def buy_limit(self, price, amount_percent=1, market="BCCCNY"):
        if amount_percent > 1.0 or amount_percent < 0.0:
            print "amount_percent should from 0 to 1"
            return
        ai = self.get_account_info()
        cnyleft = float(ai.get("data").get("CNY").get("available"))
        amount = (cnyleft / float(price)-0.001) * amount_percent
        if amount >= 0.01:
            self.order_limit("buy", amount=amount, price=price, market=market)
            print "order done."
        else:
            print "your money is not enough to buy 0.01 unit"

    def buy_market(self, amount_percent=1, market="BCCCNY"):
        if amount_percent > 1.0 or amount_percent < 0.0:
            print "amount_percent should from 0 to 1"
            return
        ai = self.get_account_info()
        cnyleft = float(ai.get("data").get("CNY").get("available"))
        amount = cnyleft * amount_percent
        try:
            self.order_market("buy", amount=amount, market=market)
            print "order done."
        except:
            print "your money is not enough to buy 0.01 unit"
            print "UNDONE."

    def sell_limit(self, price, amount_percent=1, market="BCCCNY"):
        if amount_percent > 1 or amount_percent < 0.0:
            print "amount_percent should from 0 to 1"
            return
        ai = self.get_account_info()
        cointype = market[:3]
        amount = float(ai.get("data").get(cointype).get("available")) * amount_percent
        if amount >= 0.01:
            self.order_limit("sell", amount, price, market=market)
            print "order done."
        else:
            print "amount not enough to sell"

    def sell_market(self, amount_percent=1, market="BCCCNY"):
        if amount_percent > 1.0 or amount_percent < 0.0:
            print "amount_percent should from 0 to 1"
            return
        ai = self.get_account_info()
        cointype = market[:3]
        amount = float(ai.get("data").get(cointype).get("available")) * amount_percent
        if amount >= 0.01:
            self.order_market("sell", amount, market=market)
            print "order done."
        else:
            print "amount not enough to sell"


class ViabtcAutotrade(object):
    def __init__(self, access_id, secret_key, market="BCCCNY"):
        self.order = ViabtcOrder(access_id, secret_key)
        self.market = market

    # withdraw
    def withdraw(self, od_id=""):
        if od_id == "":
            self.order.withdraw_all(market=self.market)
        else:
            self.order.order_withdraw(order_id=od_id, market=self.market)

    # 持续向下报价
    def pull_down(self, step=0.01, amount=0.01):
        last_id = ""
        last_price = 0
        while 1:
            time.sleep(0.5)
            print "0"
            market_depth = ViabtcData.get_market_depth(limit=1, market=self.market)
            bid_price, bid_amount = map(float, market_depth["data"]["bids"][0])
            ask_price, ask_amount = map(float, market_depth["data"]["asks"][0])

            # 先写一个追踪策略
            if ask_price > bid_price + step:
                if last_id != "":
                    print "1"
                    self.order.order_withdraw(last_id, market=self.market)
                    if last_price <= bid_price + step:
                        print "4"
                        break
                    sell1 = self.order.order_limit("sell",
                                                   price=min([ask_price, last_price]) - step,
                                                   amount=amount,
                                                   market=self.market)
                    print sell1
                    last_id = sell1["data"]["id"]
                    last_price = float(sell1["data"]["price"])
                else:
                    print "2"
                    sell1 = self.order.order_limit("sell",
                                                   price=ask_price - step,
                                                   amount=amount,
                                                   market=self.market)
                    print sell1
                    last_id = sell1["data"]["id"]
                    last_price = float(sell1["data"]["price"])
            else:
                print "3"
                self.order.withdraw_all(market=self.market)
                break

    # 持续向上报价
    def pull_up(self, step=0.01, amount=0.01):
        last_id = ""
        last_price = 0
        while 1:
            time.sleep(0.5)
            print "0"
            market_depth = ViabtcData.get_market_depth(limit=1, market=self.market)
            bid_price, bid_amount = map(float, market_depth["data"]["bids"][0])
            ask_price, ask_amount = map(float, market_depth["data"]["asks"][0])

            # 先写一个追踪策略
            if ask_price > bid_price + step:
                if last_id != "":
                    print "1"
                    self.order.order_withdraw(last_id, market=self.market)
                    if last_price + step >= ask_price:
                        print "4"
                        break
                    buy1 = self.order.order_limit("buy",
                                                  price=max([bid_price, last_price]) + step,
                                                  amount=amount,
                                                  market=self.market)
                    print buy1
                    last_id = buy1["data"]["id"]
                    last_price = float(buy1["data"]["price"])
                else:
                    print "2"
                    buy1 = self.order.order_limit("buy",
                                                  price=bid_price + step,
                                                  amount=amount,
                                                  market=self.market)
                    print buy1
                    last_id = buy1["data"]["id"]
                    last_price = float(buy1["data"]["price"])
            else:
                print "3"
                self.order.withdraw_all(market=self.market)
                break

    # 清楚level即之前位置的买单
    def clean_bid(self, level=1):
        market_depth = ViabtcData.get_market_depth(market=self.market)
        asks = market_depth["data"]["asks"][:level]
        bids = market_depth["data"]["bids"][:level]
        for i in bids:
            self.order.order_limit("sell", float(i[1]), float(i[0]), market=self.market)

    # 清楚level即之后位置的买单
    def clean_ask(self, level=1):
        market_depth = ViabtcData.get_market_depth(market=self.market)
        asks = market_depth["data"]["asks"][:level]
        bids = market_depth["data"]["bids"][:level]
        for i in asks:
            self.order.order_limit("buy", float(i[1]), float(i[0]), market=self.market)

    # 引诱买单，看看是否有机器跟单
    def lure_bid(self, amount=0.01, price=0):
        market_depth = ViabtcData.get_market_depth(limit=1, market=self.market)
        bid_price, bid_amount = map(float, market_depth["data"]["bids"][0])
        ask_price, ask_amount = map(float, market_depth["data"]["asks"][0])

        if price == 0:
            price = ask_price - 0.01

        od = self.order.order_limit("buy", amount=amount, price=price, market=self.market)
        od_price = float(od["data"]["price"])
        od_id = od["data"]["id"]

        time.sleep(0.5)

        market_depth = ViabtcData.get_market_depth(limit=5, market=self.market)
        bid_price1, bid_amount1 = map(float, market_depth["data"]["bids"][0])
        ask_price1, ask_amount1 = map(float, market_depth["data"]["asks"][0])
        bid_price2, bid_amount2 = map(float, market_depth["data"]["bids"][1])
        ask_price2, ask_amount2 = map(float, market_depth["data"]["asks"][1])

        if bid_price1 != od_price:
            print "Shit, the deal has been eaten."
        else:
            if bid_amount1 != amount or bid_price2 == od_price - 0.01:
                print "There is a follower, let's crush him!"
                self.order.order_withdraw(order_id=od_id, market=self.market)
            else:
                print "There is no follower, peace."
                self.order.order_withdraw(order_id=od_id, market=self.market)

    # 引诱卖单，看看是否有机器跟单
    def lure_ask(self, amount=0.01, price=0):

        market_depth = ViabtcData.get_market_depth(limit=1, market=self.market)
        bid_price, bid_amount = map(float, market_depth["data"]["bids"][0])
        ask_price, ask_amount = map(float, market_depth["data"]["asks"][0])

        if price == 0:
            price = bid_price + 0.01

        od = self.order.order_limit("sell", amount=amount, price=price, market=self.market)
        od_price = float(od["data"]["price"])
        od_id = od["data"]["id"]

        time.sleep(0.5)

        market_depth = ViabtcData.get_market_depth(limit=5, market=self.market)
        bid_price1, bid_amount1 = map(float, market_depth["data"]["bids"][0])
        ask_price1, ask_amount1 = map(float, market_depth["data"]["asks"][0])
        bid_price2, bid_amount2 = map(float, market_depth["data"]["bids"][1])
        ask_price2, ask_amount2 = map(float, market_depth["data"]["asks"][1])

        if ask_price1 != od_price:
            print "Shit, the deal has been eaten."
        else:
            if ask_amount1 != amount or ask_price2 == od_price + 0.01:
                print "There is a follower, let's crush him!"
                self.order.order_withdraw(order_id=od_id, market=self.market)
            else:
                print "There is no follower, peace."
                self.order.order_withdraw(order_id=od_id, market=self.market)

    # 自买自卖，强行成交
    def self_deal(self, price, amount=0.01):
        market_depth = ViabtcData.get_market_depth(limit=1, market=self.market)
        bid_price, bid_amount = map(float, market_depth["data"]["bids"][0])
        ask_price, ask_amount = map(float, market_depth["data"]["asks"][0])

        if price > ask_price or price < bid_price:
            print "Shit, your deal is going to be eaten, change your price."
            return 0

        self.order.order_limit("buy",
                               price=price,
                               amount=amount,
                               market=self.market)
        self.order.order_limit("sell",
                               price=price,
                               amount=amount,
                               market=self.market)
        self.order.withdraw_all(market=self.market)

    # 返回买1的价格
    def bid1_price(self):
        market_depth = ViabtcData.get_market_depth(limit=1, market=self.market)
        bid_price, bid_amount = map(float, market_depth["data"]["bids"][0])
        ask_price, ask_amount = map(float, market_depth["data"]["asks"][0])
        return bid_price + 0.01

    # 返回买2的价格
    def ask1_price(self):
        market_depth = ViabtcData.get_market_depth(limit=1, market=self.market)
        bid_price, bid_amount = map(float, market_depth["data"]["bids"][0])
        ask_price, ask_amount = map(float, market_depth["data"]["asks"][0])
        return ask_price - 0.01

    # 在买方持续抢跑
    def bid_runner(self, step=0.01, amount=0.01):
        def bid_runner_temp(step=step, amount=amount):
            last_id = ""
            last_price = 0.0
            while 1:
                print "0"

                time.sleep(0.1)

                market_depth = ViabtcData.get_market_depth(limit=5, market=self.market)
                bid_price, bid_amount = map(float, market_depth["data"]["bids"][0])
                ask_price, ask_amount = map(float, market_depth["data"]["asks"][0])
                bid_price2, bid_amount2 = map(float, market_depth["data"]["bids"][1])
                ask_price2, ask_amount2 = map(float, market_depth["data"]["asks"][1])

                print bid_price, last_price

                # 判断是否是领跑者或虚高者
                if bid_price == last_price:  # 领跑了，但别虚高，回退一点点
                    print "peace, you are the first runner!"
                    if bid_price - bid_price2 > 1.5 * step:
                        base_price = bid_price2
                    else:
                        continue
                elif bid_price > last_price:
                    print "you got a Follower, you need run faster!"
                    base_price = bid_price
                else:
                    print "be careful, your order may have been eaten!"
                    base_price = bid_price

                if base_price + step >= ask_price:
                    print "Shit, your order may be eaten. withdraw all, start over."
                    self.withdraw()
                    last_price = 0.0
                    last_id = ""
                    continue

                if last_id == "":
                    self.order.withdraw_all(market=self.market)
                else:
                    self.order.order_withdraw(last_id, market=self.market)

                od = self.order.order_limit("buy",
                                            amount=amount,
                                            price=base_price + step,
                                            market=self.market)
                last_id = od["data"]["id"]
                last_price = float(od["data"]["price"])

        try:
            bid_runner_temp(step, amount)
        except:
            print "No enough money to buy"
            while 1:
                time.sleep(5)

                account = self.order.get_account_info()
                cny = float(account["data"]["CNY"]["available"])
                price = float(self.bid1_price())
                how_much_can_i_buy = cny / price

                if how_much_can_i_buy >= step:
                    self.bid_runner(step, amount)
                else:
                    continue

    # 在卖方持续抢跑
    def ask_runner(self, step=0.01, amount=0.01):
        def ask_runner_temp(step=step, amount=amount):
            last_id = ""
            last_price = 0.0
            while 1:
                print "0"

                time.sleep(0.1)

                market_depth = ViabtcData.get_market_depth(limit=5, market=self.market)
                bid_price, bid_amount = map(float, market_depth["data"]["bids"][0])
                ask_price, ask_amount = map(float, market_depth["data"]["asks"][0])
                bid_price2, bid_amount2 = map(float, market_depth["data"]["bids"][1])
                ask_price2, ask_amount2 = map(float, market_depth["data"]["asks"][1])

                print ask_price, last_price

                if ask_price == last_price:
                    print "peace, you are the first runner!"
                    if ask_price2 - ask_price > 1.5 * step:
                        base_price = ask_price2
                    else:
                        continue
                elif ask_price < last_price:
                    print "you got a Follower, you need run faster!"
                    base_price = ask_price
                else:
                    print "be careful, your order may have been eaten!"
                    base_price = ask_price

                if base_price - step <= bid_price:
                    print "Shit, your order may be eaten. withdraw all, start over."
                    self.withdraw()
                    last_price = 0.0
                    last_id = ""
                    continue

                if last_id == "":
                    self.order.withdraw_all(market=self.market)
                else:
                    self.order.order_withdraw(last_id, market=self.market)

                od = self.order.order_limit("sell", amount=amount,
                                            price=base_price - step,
                                            market=self.market)
                last_id = od["data"]["id"]
                last_price = float(od["data"]["price"])

        try:
            ask_runner_temp(step, amount)
        except:
            print "No enough coin to sell"
            while 1:
                time.sleep(5)

                account = self.order.get_account_info()
                coin = float(account["data"][self.market[:3]]["available"])

                if coin >= step:
                    self.ask_runner(step, amount)
                else:
                    continue

    # 套利交易测试机 测试是否存在套利交易
    @staticmethod
    def arbitrage_machine():
        market_depth = ViabtcData.get_market_depth(market="BCCCNY", limit=1)
        bid_priceBCCCNY, bid_amountBCCCNY = map(float, market_depth["data"]["bids"][0])
        ask_priceBCCCNY, ask_amountBCCCNY = map(float, market_depth["data"]["asks"][0])

        market_depth = ViabtcData.get_market_depth(market="BTCCNY", limit=1)
        bid_priceBTCCNY, bid_amountBTCCNY = map(float, market_depth["data"]["bids"][0])
        ask_priceBTCCNY, ask_amountBTCCNY = map(float, market_depth["data"]["asks"][0])

        market_depth = ViabtcData.get_market_depth(market="BCCBTC", limit=1)
        bid_priceBCCBTC, bid_amountBCCBTC = map(float, market_depth["data"]["bids"][0])
        ask_priceBCCBTC, ask_amountBCCBTC = map(float, market_depth["data"]["asks"][0])

        md = {
            "BCC-CNY-bid": bid_priceBCCCNY,
            "BCC-CNY-ask": ask_priceBCCCNY,
            "BTC-CNY-bid": bid_priceBTCCNY,
            "BTC-CNY-ask": ask_priceBTCCNY,
            "BCC-BTC-bid": bid_priceBCCBTC,
            "BCC-BTC-ask": ask_priceBCCBTC
        }

        cny_bcc_btc_cny = 1 / md["BCC-CNY-ask"] * 0.999 \
                          * md["BCC-BTC-bid"] * 0.999 \
                          * md["BTC-CNY-bid"] * 0.999

        cny_btc_bcc_cny = 1 / md["BTC-CNY-ask"] * 0.999 \
                          / md["BCC-BTC-ask"] * 0.999 \
                          * md["BCC-CNY-bid"] * 0.999

        return cny_bcc_btc_cny, cny_btc_bcc_cny

    def market_maker(self, step=0.01, amount=0.01):

        bidr = multiprocessing.Process(target=self.bid_runner,
                                       args=(step, amount,))
        askr = multiprocessing.Process(target=self.ask_runner,
                                       args=(step, amount,))
        bidr.start()
        askr.start()




