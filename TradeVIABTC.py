# -*- coding:utf-8 -*-
# 这是对viabtd.com的API进行的封装。
# author: LucasPHBS
# update: 20170811

##
import urllib2
import json
import hashlib

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
        pass

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
    def get_market_depth(market="BCCCNY", merge=1, limit=10, header=_header):
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
                    "&last_id=" + last_id
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

    # 哈希signature
    @staticmethod
    def md5(signature):
        md5 = hashlib.md5()
        md5.update(signature)
        return str.upper(md5.hexdigest())

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
        # account_info链接
        url = "https://www.viabtc.com/api/v1/balance/?" + \
              "access_id=" + self.access_id

        # 获取对应的签名
        signature_before_md5 = "access_id=" + self.access_id + \
                               "&secret_key=" + self.secret_key
        signature = self.md5(signature_before_md5)

        # 将签名写入header
        header = self._header
        header["Authorization"] = signature

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

        # 链接信息
        url = "https://www.viabtc.com/api/v1/order/pending" \
              "?page=" + str(page) + \
              "&limit=" + str(limit) + \
              "&market=" + market + \
              "&access_id=" + self.access_id

        # 获取对应的签名
        signature_before_md5 = "access_id=" + self.access_id + \
                               "&limit=" + str(limit) + \
                               "&market=" + market + \
                               "&page=" + str(page) +\
                               "&secret_key=" + self.secret_key
        signature = self.md5(signature_before_md5)

        # 将签名写入header
        header = self._header
        header["Authorization"] = signature

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

        # 链接信息
        url = "https://www.viabtc.com/api/v1/order/finished" \
              "?page=" + str(page) + \
              "&limit=" + str(limit) + \
              "&market=" + market + \
              "&access_id=" + self.access_id

        # 获取对应的签名
        signature_before_md5 = "access_id=" + self.access_id + \
                               "&limit=" + str(limit) + \
                               "&market=" + market + \
                               "&page=" + str(page) + \
                               "&secret_key=" + self.secret_key
        signature = self.md5(signature_before_md5)

        # 将签名写入header
        header = self._header
        header["Authorization"] = signature

        # 请求并读取数据
        req = urllib2.Request(url, headers=header)
        response = urllib2.urlopen(req).read()
        # 解析数据
        finished_orders = json.loads(response)
        # 返回数据
        return finished_orders
##
