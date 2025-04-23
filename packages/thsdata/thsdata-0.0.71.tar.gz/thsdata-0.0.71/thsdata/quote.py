import pytz
import json
import random
import requests
import datetime
import pandas as pd
from typing import List, Tuple
from datetime import datetime, time

from thsdk import THS

china_tz = pytz.timezone('Asia/Shanghai')


class Adjust:
    """Class to represent adjustment types for stock data."""
    FORWARD = "Q"  # 前复权
    BACKWARD = "B"  # 后复权
    NONE = ""  # 不复权

    @classmethod
    def all_types(cls):
        """Return all adjustment types as a list."""
        return [cls.FORWARD, cls.BACKWARD, cls.NONE]


class Interval:
    """Class to represent Kline period types."""
    MIN_1 = 0x3001  # 1分钟k
    MIN_5 = 0x3005  # 5分钟k
    MIN_15 = 0x300f  # 15分钟k
    MIN_30 = 0x301e  # 30分钟k
    MIN_60 = 0x303c  # 60分钟k
    MIN_120 = 0x3078  # 120分钟k
    DAY = 0x4000  # 日k
    WEEK = 0x5001  # 周k
    MONTH = 0x6001  # 月k
    QUARTER = 0x6003  # 季k
    YEAR = 0x7001  # 年k

    @classmethod
    def minute_intervals(cls):
        """Return all minute-level intervals."""
        return [
            cls.MIN_1, cls.MIN_5, cls.MIN_15, cls.MIN_30,
            cls.MIN_60, cls.MIN_120
        ]

    @classmethod
    def day_and_above_intervals(cls):
        """Return all day-level and above intervals."""
        return [
            cls.DAY, cls.WEEK, cls.MONTH,
            cls.QUARTER, cls.YEAR
        ]

    @classmethod
    def all_types(cls):
        """Return all Kline period types as a list."""
        return [
            cls.MIN_1, cls.MIN_5, cls.MIN_15, cls.MIN_30, cls.MIN_60, cls.MIN_120,
            cls.DAY, cls.WEEK, cls.MONTH, cls.QUARTER, cls.YEAR
        ]


def time_2_int(t: datetime) -> int:
    dst = (t.minute +
           (t.hour << 6) +
           (t.day << 11) +
           (t.month << 16) +
           (t.year << 20) -
           0x76c00000)
    return dst


class Quote:
    def __init__(self, ops: dict = None):
        self.ops = ops
        self._zhu_quote = None
        self._fu_quote = None
        self._zx_quote = None
        self._bk_quote = None
        self.__share_instance = random.randint(80000000, 99999999)

    @property
    def share_instance(self):
        self.__share_instance += 1  # Increment on access
        return self.__share_instance

    @property
    def main_quote(self):
        if self._zhu_quote is None:
            self._zhu_quote = THS(self.ops)
            self._zhu_quote.connect()
        return self._zhu_quote

    @property
    def secondary_quote(self):
        if self._fu_quote is None:
            addr = "default_fu_addr"
            ops_with_addr = {**self.ops, "addr": addr} if self.ops else {"addr": addr}
            self._fu_quote = THS(ops_with_addr)
            self._fu_quote.connect()
        return self._fu_quote

    @property
    def info_quote(self):
        if self._zx_quote is None:
            addr = "default_info_addr"
            ops_with_addr = {**self.ops, "addr": addr} if self.ops else {"addr": addr}
            self._zx_quote = THS(ops_with_addr)
            self._zx_quote.connect()
        return self._zx_quote

    @property
    def block_quote(self):
        if self._bk_quote is None:
            addr = "default_block_addr"
            ops_with_addr = {**self.ops, "addr": addr} if self.ops else {"addr": addr}
            self._bk_quote = THS(ops_with_addr)
            self._bk_quote.connect()
        return self._bk_quote

    def connect(self):
        self.main_quote
        self.secondary_quote
        self.info_quote
        self.block_quote

    def disconnect(self):
        if self._zhu_quote:
            self._zhu_quote.disconnect()
        if self._fu_quote:
            self._fu_quote.disconnect()
        if self._zx_quote:
            self._zx_quote.disconnect()
        if self._bk_quote:
            self._bk_quote.disconnect()

    def about(self):
        about = "\n\nabout me: 本项目基于thsdk二次开发。仅用于个人对网络协议的研究和习作，不对外提供服务。请勿用于非法用途，对此造成的任何问题概不负责。 \n\n"

        thsdk_about = "\n\n"
        if self._zhu_quote:
            thsdk_about = self._zhu_quote.about()
        elif self._fu_quote:
            thsdk_about = self._fu_quote.about()
        elif self._zx_quote:
            thsdk_about = self._zx_quote.about()
        elif self._bk_quote:
            thsdk_about = self._bk_quote.about()
        return about

    def _main_quote_query_data(self, req: str):
        try:
            reply = self.main_quote.query_data(req)
            if reply.err_code != 0:
                print(f"Query error: {reply.err_code}, Message: {reply.err_message}")
                return pd.DataFrame()  # Return an empty DataFrame on error
            resp = reply.resp
            df = pd.DataFrame(resp.data)
            return df

        except Exception as e:
            print(f"An exception occurred: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on exception

    def _block_data(self, block_id: int):
        try:
            reply = self.block_quote.get_block_data(block_id)
            if reply.err_code != 0:
                print(f"Query error: {reply.err_code}, Message: {reply.err_message}")
                return pd.DataFrame()  # Return an empty DataFrame on error
            resp = reply.resp
            df = pd.DataFrame(resp.data)
            return df
        except Exception as e:
            print(f"An exception occurred: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on exception

    def _get_block_components(self, block_code: str) -> pd.DataFrame:
        try:
            reply = self.block_quote.get_block_components(block_code)
            if reply.err_code != 0:
                print(f"Query error: {reply.err_code}, Message: {reply.err_message}")
                return pd.DataFrame()  # Return an empty DataFrame on error
            resp = reply.resp
            df = pd.DataFrame(resp.data)
            return df
        except Exception as e:
            print(f"An exception occurred: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on exception

    def stock_codes(self) -> pd.DataFrame:
        """获取股票市场代码.

        :return: pandas.DataFrame

        Example::

            code        name
            USHA600519  贵州茅台
            USZA300750  宁德时代
            USTM832566    梓橦宫
        """
        return self._block_data(0xC6A6)

    def cbond_codes(self) -> pd.DataFrame:
        """获取可转债市场代码.

        :return: pandas.DataFrame

        Example::

            code        name
            USHD113037   紫银转债
            USZD123158   宙邦转债
            USHD110094   众和转债
        """
        return self._block_data(0xCE14)

    def etf_codes(self) -> pd.DataFrame:
        """获取ETF基金市场代码.

        :return: pandas.DataFrame

        Example::

            code        name
            USHJ589660       综指科创
            USZJ159201   自由现金流ETF
            USHJ510410      资源ETF
        """
        return self._block_data(0xCFF3)

    def security_bars(self, code: str, start: datetime, end: datetime, adjust: str, period: int) -> pd.DataFrame:
        """获取指定证券的K线数据.
        支持日k线、周k线、月k线，以及5分钟、15分钟、30分钟和60分钟k线数据.

        :param code: 证券代码，例如 'USHA600519'
        :type code: str
        :param start: 开始时间，格式为 datetime 对象
        :type start: datetime.datetime
        :param end: 结束时间，格式为 datetime 对象
        :type end: datetime.datetime
        :param adjust: 复权类型， :const:`Q`, :const:`B`, :const:``
        :type adjust: str
        :param period: 数据类型，
        :type period: int

        :return: pandas.DataFrame

        Example::

                time    close   volume    turnover     open     high      low
            2024-01-02  1685.01  3215644  5440082500  1715.00  1718.19  1678.10
            2024-01-03  1694.00  2022929  3411400700  1681.11  1695.22  1676.33
            2024-01-04  1669.00  2155107  3603970100  1693.00  1693.00  1662.93
        """
        m_period = {0x3001, 0x3005, 0x300f, 0x301e, 0x303c, 0x3078, }

        if period in m_period:
            start_int = time_2_int(start)
            end_int = time_2_int(end)
        else:
            if start.tzinfo is None:
                # If naive, localize to Beijing timezone
                start = china_tz.localize(start)
            else:
                # Convert to Beijing timezone
                start = start.astimezone(china_tz)

            if end.tzinfo is None:
                # If naive, localize to Beijing timezone
                end = china_tz.localize(end)
            else:
                # Convert to Beijing timezone
                end = end.astimezone(china_tz)

            start_int = int(start.strftime('%Y%m%d'))
            end_int = int(end.strftime('%Y%m%d'))

        reply = self.main_quote.security_bars(code, start_int, end_int, adjust, period)
        if reply.err_code != 0:
            print(f"查询错误:{reply.err_code}, 信息:{reply.err_message}")
            return

        resp = reply.resp
        return pd.DataFrame(resp.data)

    def ths_industry_block(self) -> pd.DataFrame:
        """获取同花顺行业板块.

        :return: pandas.DataFrame

        Example::

                      code   name
            0   URFI881165     综合
            1   URFI881171  自动化设备
            2   URFI881118   专用设备
            3   URFI881141     中药
            4   URFI881157     证券
            ..         ...    ...
            85  URFI881138   包装印刷
            86  URFI881121    半导体
            87  URFI881131   白色家电
            88  URFI881273     白酒
            89  URFI881271   IT服务
        """
        return self._block_data(0xCE5F)

    def ths_industry_sub_block(self) -> pd.DataFrame:
        """获取同花顺三级行业板块.

        :return: pandas.DataFrame

        Example::

                       code    name
            0    URFA884270  综合环境治理
            1    URFA884164    自然景点
            2    URFA884065    装饰园林
            3    URFA884161    专业连锁
            4    URFA884068    专业工程
            ..          ...     ...
            225  URFA884091   半导体材料
            226  URFA884160    百货零售
            227  URFA884294    安防设备
            228  URFA884045      氨纶
            229  URFA884095     LED
        """
        return self._block_data(0xc4b5)

    def ths_concept_block(self) -> pd.DataFrame:
        """获取同花顺概念板块.

        :return: pandas.DataFrame

        Example::

                       code       name
            0    URFI885580       足球概念
            1    URFI885758       租售同权
            2    URFI885764      自由贸易港
            3    URFI885760      装配式建筑
            4    URFI885877        转基因
            ..          ...        ...
            391  URFI886037       6G概念
            392  URFI885556         5G
            393  URFI885537       3D打印
            394  URFI886088  2024三季报预增
            395  URFI886097   2024年报预增
        """
        return self._block_data(0xCE5E)

    def ths_block_components(self, block_code: str) -> pd.DataFrame:
        """查询行业，行业三级，概念板块成分股.

        :param block_code: 板块代码，例如 'URFI881157'

        :return: pandas.DataFrame

        Example::

                      code   name
            0   USHA601375  中原证券
            1   USHA601696  中银证券
            2   USHA600030  中信证券
            ..          ...     ...
            46  USZA002939  长城证券
            47  USHA601108  财通证券
            48  USHA600906  财达证券
        """
        return self._get_block_components(block_code)

    def stock_cur_market_data(self, codes: List[str]) -> pd.DataFrame:
        """股票当前时刻市场数据

        :param codes: 证券代码，例如 'USHA600519, USHA600036' 注意只能同一市场
        :type codes: List[str]

        :return: pandas.DataFrame

        Example::
                price  deal_type   volume  volume_ratio  ...  limit_down    high    low   开盘涨幅
            0  669.54         21  4168728        0.5324  ...       541.6  677.31  663.1 -1.034


        """

        market = codes[0][:4]

        # 检查所有代码是否属于同一市场
        for code in codes:
            if len(code) != 10:
                raise ValueError("证券代码长度不足")
            if code[:4] != market:
                raise ValueError("只能同一市场的证券代码")

        short_codes = [code[4:] for code in codes]  # 剔除前4位
        short_code = ','.join(short_codes)  # 用逗号连接

        req = f"id=200&instance={self.share_instance}&zipversion=2&codelist={short_code}&market={market}&datatype=5,6,8,9,10,12,13,402,19,407,24,30,48,49,69,70,3250,920371,55,199112,264648,1968584,461256,1771976,3475914,3541450,526792,3153,592888,592890"

        data = self._main_quote_query_data(req)

        return data

    def cbond_cur_market_data(self, codes: List[str]) -> pd.DataFrame:
        """可转债当前时刻市场数据

        :param codes: 证券代码，例如 'USHD600519, USHD600036' 注意只能同一市场
        :type codes: List[str]

        :return: pandas.DataFrame

        Example::
                price  deal_type   volume  volume_ratio  ...  limit_down    high    low   开盘涨幅
            0  669.54         21  4168728        0.5324  ...       541.6  677.31  663.1 -1.034


        """

        market = codes[0][:4]

        # 检查所有代码是否属于同一市场
        for code in codes:
            if len(code) != 10:
                raise ValueError("证券代码长度不足")
            if code[:4] != market:
                raise ValueError("只能同一市场的证券代码")

        short_codes = [code[4:] for code in codes]  # 剔除前4位
        short_code = ','.join(short_codes)  # 用逗号连接

        req = f"id=200&instance={self.share_instance}&zipversion=2&codelist={short_code}&market={market}&datatype=5,55,10,80,49,13,19,25,31,24,30,6,7,8,9,12,199112,264648,48,1771976,1968584,527527"

        data = self._main_quote_query_data(req)

        return data

    def call_auction(self, code: str) -> pd.DataFrame:
        """集合竞价

        :param code: 证券代码，例如 'USHA600519'
        :type code: str

        :return: pandas.DataFrame

        Example::

                                    time    price    bid2_vol    ask2_vol  cur_volume
            0  2025-03-04 09:15:07+08:00  1487.02  2147483648  2147483648         500
            1  2025-03-04 09:15:10+08:00  1487.46         900  2147483648        1100
            2  2025-03-04 09:15:13+08:00  1487.46         997  2147483648        1203
            3  2025-03-04 09:15:16+08:00  1487.46         797  2147483648        1503
            4  2025-03-04 09:15:19+08:00  1487.46         697  2147483648        1603
            ..                       ...      ...         ...         ...         ...
            74 2025-03-04 09:24:46+08:00  1487.00         447  2147483648       11353
            75 2025-03-04 09:24:49+08:00  1487.00          47  2147483648       11953
            76 2025-03-04 09:24:52+08:00  1487.00         147  2147483648       12153
            77 2025-03-04 09:24:55+08:00  1487.00  2147483648         353       12300
            78 2025-03-04 09:24:58+08:00  1485.00  2147483648         253       13100

        """

        now = datetime.now()
        # 使用当前日期，构造当天的 9:15:00 和 9:25:00
        start = datetime.combine(now.date(), time(9, 15, 0))  # 9:15:00
        end = datetime.combine(now.date(), time(9, 25, 0))  # 9:25:00

        # 获取 Unix 时间戳（秒）
        start_unix = int(start.timestamp())
        end_unix = int(end.timestamp())
        market = code[:4]
        short_code = code[4:]
        req = f"id=204&instance={self.share_instance}&zipversion=2&code={short_code}&market={market}&datatype=1,10,27,33,49&start={start_unix}&end={end_unix}"

        data = self._main_quote_query_data(req)
        data['time'] = pd.to_datetime(data['time'], unit='s').dt.tz_localize('UTC').dt.tz_convert(china_tz)

        return data

    def corporate_action(self, code: str) -> pd.DataFrame:
        """权息资料

        :param code: 证券代码，例如 'USHA600519'
        :type code: str

        :return: pandas.DataFrame

        Example::

                    time                                               权息资料
            0   20020725                   2002-07-25(每十股 转增1.00股 红利6.00元)$
            1   20030714                    2003-07-14(每十股 送1.00股 红利2.00元)$
            2   20040701                   2004-07-01(每十股 转增3.00股 红利3.00元)$
            3   20050805                   2005-08-05(每十股 转增2.00股 红利5.00元)$
            4   20060519                           2006-05-19(每十股 红利3.00元)$
            5   20060525  2006-05-25(  每10股对价现金41.3200元 ,每10股对价股票12.4000股)$
            6   20070713                           2007-07-13(每十股 红利7.00元)$
            7   20080616                           2008-06-16(每十股 红利8.36元)$
            8   20090701                          2009-07-01(每十股 红利11.56元)$
            9   20100705                          2010-07-05(每十股 红利11.85元)$
            10  20110701                   2011-07-01(每十股 送1.00股 红利23.00元)$
            11  20120705                          2012-07-05(每十股 红利39.97元)$
            12  20130607                          2013-06-07(每十股 红利64.19元)$
            13  20140625                   2014-06-25(每十股 送1.00股 红利43.74元)$
            14  20150717                   2015-07-17(每十股 送1.00股 红利43.74元)$
            15  20160701                          2016-07-01(每十股 红利61.71元)$
            16  20170707                          2017-07-07(每十股 红利67.87元)$
            17  20180615                         2018-06-15(每十股 红利109.99元)$
            18  20190628                         2019-06-28(每十股 红利145.39元)$
            19  20200624                         2020-06-24(每十股 红利170.25元)$
            20  20210625                         2021-06-25(每十股 红利192.93元)$
            21  20220630                         2022-06-30(每十股 红利216.75元)$
            22  20221227                         2022-12-27(每十股 红利219.10元)$
            23  20230630                         2023-06-30(每十股 红利259.11元)$
            24  20231220                         2023-12-20(每十股 红利191.06元)$
            25  20240619                         2024-06-19(每十股 红利308.76元)$
            26  20241220                         2024-12-20(每十股 红利238.82元)$
        """

        market = code[:4]
        short_code = code[4:]
        req = f"id=211&instance={self.share_instance}&zipversion=2&code={short_code}&market={market}&start=-36500&end=0&fuquan=Q&datatype=471&period=16384"

        data = self._main_quote_query_data(req)

        return data

    def transaction_history(self, code: str, date: datetime) -> pd.DataFrame:
        """tick3秒l1快照数据

        :param code: 证券代码，例如 'USHA600519'
        :type code: str

        :param date: 指定日期
        :type date: datetime

        :return: pandas.DataFrame

        Example::

                                      time    price  ...  transaction_count  cur_volume
            0    2025-04-11 09:15:06+08:00  1544.00  ...                  0         100
            1    2025-04-11 09:15:09+08:00  1546.90  ...                  0         500
            2    2025-04-11 09:15:12+08:00  1546.90  ...                  0         700
            3    2025-04-11 09:15:15+08:00  1546.90  ...                  0         800
            4    2025-04-11 09:15:18+08:00  1550.98  ...                  0        5500
            ...                        ...      ...  ...                ...         ...
            4842 2025-04-11 14:59:51+08:00  1565.30  ...              23044           0
            4843 2025-04-11 14:59:54+08:00  1565.30  ...              23044           0
            4844 2025-04-11 14:59:57+08:00  1565.30  ...              23044           0
            4845 2025-04-11 15:00:00+08:00  1565.30  ...              23044           0
            4846 2025-04-11 15:00:03+08:00  1568.98  ...              23616      159400
        """
        # Ensure the date is in Beijing timezone
        if date.tzinfo is None:
            # If naive, localize to Beijing timezone
            date = china_tz.localize(date)
        else:
            # Convert to Beijing timezone
            date = date.astimezone(china_tz)

        # 构造当天的 09:15 和 15:30 时间
        start = datetime.combine(date.date(), time(9, 15, 0)).astimezone(china_tz)
        end = datetime.combine(date.date(), time(15, 30, 0)).astimezone(china_tz)

        # 转换为 Unix 时间戳（秒）
        start_unix = int(start.timestamp())
        end_unix = int(end.timestamp())

        market = code[:4]
        short_code = code[4:]
        req = f"id=205&instance={self.share_instance}&zipversion=2&code={short_code}&market={market}&start={start_unix}&end={end_unix}&datatype=1,5,10,12,18,49&TraceDetail=0"

        data = self._main_quote_query_data(req)
        data['time'] = pd.to_datetime(data['time'], unit='s').dt.tz_localize('UTC').dt.tz_convert(china_tz)

        return data

    def level5_order_book(self, code: str) -> dict:
        """5档盘口

        :param code: 证券代码，例如 'USHA600519'
        :type code: str

        :return: dict

        Example::
            {'bid4': 1585, 'bid4_vol': 1900, 'ask4': 1586.3, 'ask4_vol': 200, 'bid5': 1584.92, 'bid5_vol': 100, 'ask5': 1586.6, 'ask5_vol': 100, 'bid1': 1585.21, 'bid1_vol': 2, 'bid2': 1585.2, 'bid2_vol': 100, 'bid3': 1585.01, 'bid3_vol': 400, 'ask1': 1585.62, 'ask1_vol': 1100, 'ask2': 1585.65, 'ask2_vol': 100, 'ask3': 1586, 'ask3_vol': 1400, 'code': 'USHA600519'}


        """

        market = code[:4]
        short_code = code[4:]
        req = f"id=200&instance={self.share_instance}&zipversion=2&codelist={short_code}&market={market}&datatype=24,25,26,27,28,29,150,151,154,155,30,31,32,33,34,35,152,153,156,157"

        data = self._main_quote_query_data(req)

        return data.iloc[0].to_dict()

    def moneyflow_major(self, code: str) -> pd.DataFrame:
        # todo  https://zx.10jqka.com.cn/marketinfo/moneyflow/graph/major?code=600519&start=20250101&end=20250314
        pass

    def wencai(self, condition: str) -> Tuple[List[str], Exception]:
        """问财速查API.

        :param condition: 条件选股
        :return:
        """

        url = "https://eq.10jqka.com.cn/dataQuery/query"

        # 定义请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Referer": "https://eq.10jqka.com.cn/",  # 可选，模拟来源页面
            "Connection": "keep-alive"
        }

        # Prepare query parameters
        params = {"query": condition}

        try:
            # Make HTTP GET request
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Raise exception for bad status codes

            # Parse JSON response
            data = response.json()

            # Check status_msg
            if data.get("status_msg") != "success":
                return None, Exception(data.get("status_msg"))

            ret = []

            # Get stockList array
            stock_list = data.get("stockList", [])

            # Iterate through stockList
            for item in stock_list:
                stock_code = item.get("stock_code", "")
                market_id = item.get("marketid", "")

                d = stock_code
                if market_id == "17":
                    d = "USHA" + d
                    ret.append(d)
                elif market_id == "21":
                    d = "USHP" + d
                    ret.append(d)
                elif market_id == "22":
                    d = "USHT" + d
                    ret.append(d)
                elif market_id == "33":
                    d = "USZA" + d
                    ret.append(d)
                elif market_id == "37":
                    d = "USZP" + d
                    ret.append(d)
                elif market_id == "151":
                    d = "USTM" + d
                    ret.append(d)
                else:
                    d = "todo" + d
                    print(f"todo market {condition} {d}")

            return ret, None

        except requests.RequestException as e:
            return [], e
        except json.JSONDecodeError as e:
            return [], e

    def download(self, code: str, start=None, end=None, adjust=Adjust.NONE, period="max", interval=Interval.DAY,
                 count=-1) -> pd.DataFrame:
        """获取历史k线数据。

       :param period:  str max
       :param code: 证券代码，必须是10个字符长，并以'USHA'或'USZA'开头。
       :param count: 需要的数量，推荐使用此参数
       :param start: 开始时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
       :param end: 结束时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
       :param adjust: 复权类型，必须是有效的复权值之一。
       :param interval: 周期类型，必须是有效的周期值之一。

       :return: pandas.DataFrame

        Example::

                time    close   volume    turnover     open     high      low
            2024-01-02  1685.01  3215644  5440082500  1715.00  1718.19  1678.10
            2024-01-03  1694.00  2022929  3411400700  1681.11  1695.22  1676.33
            2024-01-04  1669.00  2155107  3603970100  1693.00  1693.00  1662.93
        """

        return self.main_quote.download(code, start, end, adjust, period, interval, count)
