#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------#
# Filename:     ths_api.py
#
# Description:  export finance API
# Version:      1.0
# Created:      2018/2/30 15:46
# Author:
# Company:
#
# -----------------------------------------#

import os
import re
import json
import random
import ctypes
import datetime
import platform
from typing import Any, Dict

from ._guest_ import rand_account

__all__ = ['THS', 'ZhuTHS', 'FuTHS', 'InfoTHS', 'BlockTHS',
           'AdjustedType', 'KlinePeriod',
           'MARKETS', 'DATA_CLASS_LIST', 'DATA_OP_TYPE', 'SUB_OP_TYPE',
           'Response', 'ResponseData',
           'QuoteLib']


def _ths_int2time(scr: int) -> datetime:
    m = scr & 63
    h = (scr & 1984) >> 6
    dd = (scr & 63488) >> 11
    mm = (scr & 983040) >> 16
    yyyy = (scr & 133169152) >> 20
    yyyy = 2000 + yyyy % 100

    time_str = f"{yyyy}-{mm:02d}-{dd:02d} {h:02d}:{m:02d}:00"

    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")


def _convert_data_keys(data):
    converted_data = []

    for entry in data:
        converted_entry = {}
        for key, value in entry.items():
            if int(key) in FieldNameMap:
                converted_entry[FieldNameMap[int(key)]] = value
            else:
                converted_entry[int(key)] = value
        converted_data.append(converted_entry)

    return converted_data


def _market_code2str(market_code: str) -> str:
    if market_code == "17":  # 沪
        return "USHA"
    elif market_code == "22":  # 沪退
        return "USHT"
    elif market_code == "33":  # 深圳退
        return "USZA"
    elif market_code == "37":  # 深圳退
        return "USZP"
    elif market_code == "49":  # 指数
        return "URFI"
    elif market_code == "151":  # 北交所
        return "USTM"
    else:
        raise ValueError("未找到")


def _market_str(market_code: str) -> str:
    try:
        return _market_code2str(market_code)
    except ValueError:
        return ""


# 市场代码列表，深圳没有USZT，USOO和UZOO为个股期权
MARKETS = ['USH', 'USHI', 'USHA', 'USHB', 'USHD', 'USHJ', 'USHP', 'USHT', 'USZ', 'USZI', 'USZA', 'USZB', 'USZD', 'USZJ',
           'USZP', 'USOO', 'UZOO']


class AdjustedType:
    """Class to represent adjustment types for stock data."""
    FORWARD = "Q"  # 前复权
    BACKWARD = "B"  # 后复权
    NONE = ""  # 不复权

    @classmethod
    def all_types(cls):
        """Return all adjustment types as a list."""
        return [cls.FORWARD, cls.BACKWARD, cls.NONE]


class KlinePeriod:
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
    def all_periods(cls):
        """Return all Kline period types as a list."""
        return [
            cls.MIN_1, cls.MIN_5, cls.MIN_15, cls.MIN_30, cls.MIN_60, cls.MIN_120,
            cls.DAY, cls.WEEK, cls.MONTH, cls.QUARTER, cls.YEAR
        ]


# 订阅数据类型：1-指数快照，2-证券快照，3-委托队列，4-逐笔委托，5-逐笔成交，5-极速盘口
DATA_CLASS_LIST = [1, 2, 3, 4, 5, 6]
DATA_CLASS_NAMES = ['index', 'stock', 'queue', 'order', 'trans', 'superstock']
# 数据类型：0xf-数据类型，0x0-交易所原始数据，0x1-使用压缩，0xf0-数据类型，0x10-更新补全后的数据
DATA_OP_TYPE = [0xf, 0x0, 0x1, 0xf0, 0x10]
# 订阅操作类型：1-全新订阅，2-取消订阅，3-该市场增加订阅代码，4-该市场删除订阅代码
SUB_OP_TYPE = [1, 2, 3, 4]

zhu_addr = 'default_zhu_addr'
fu_addr = 'default_fu_addr'
info_addr = 'default_info_addr'
block_addr = 'default_block_addr'

MarketUSHI = "USHI"  # 上海指数
MarketUSHA = "USHA"  # 上海A股
MarketUSHB = "USHB"  # 上海B股
MarketUSHD = "USHD"  # 上海可转债
MarketUSHJ = "USHJ"  # 上海基金
MarketUSHT = "USHT"  # 上海ST风险警示板
MarketUSHP = "USHP"  #
MarketUZZI = "UZZI"  #
MarketURFI = "URFI"  # 沪深板块？
MarketURFA = "URFA"  # 沪深板块？

MarketUIFF = "UIFF"  # 股指期货

MarketUFII = "UFII"  # 国外指数
MarketUCMI = "UCMI"  # 国外指数

MarketUNQS = "UNQS"  # 美股
MarketUNYN = "UNYN"  # 美股
MarketUNQQ = "UNQQ"  # 美股
MarketUNYA = "UNYA"  # 美股
MarketUUSD = "UUSD"  # 美股
MarketUUSA = "UUSA"  # 美股

MarketUFXB = "UFXB"  # 外汇
MarketUFXC = "UFXC"  # 外汇
MarketUFXR = "UFXR"  # 外汇

MarketUCMN = "UCMN"  # 国外期货
MarketUCMS = "UCMS"  # 国外期货
MarketUFIS = "UFIS"  # 国外期货

MarketUCFS = "UCFS"  # 国内期货
MarketUCFD = "UCFD"  # 国内期货
MarketUCFZ = "UCFZ"  # 国内期货

MarketUSTA = "USTA"  # 股转
MarketUSTB = "USTB"  # 股转
MarketUSTT = "USTT"  # 股转

MarketUSTI = "USTI"  # 股转指数

MarketUSOO = "USOO"  # 期权
MarketUZOO = "UZOO"  # 期权
MarketUCFT = "UCFT"  # 期权
MarketUCFL = "UCFL"  # 期权
MarketUCFX = "UCFX"  # 期权
MarketUIFB = "UIFB"  # 期权

MarketUHKI = "UHKI"  # 港股指数
MarketUSZI = "USZI"  # 深圳指数
MarketUSZA = "USZA"  # 深圳A股
MarketUSZB = "USZB"  # 深圳B股
MarketUSZJ = "USZJ"  # 深圳基金
MarketUSZD = "USZD"  # 深圳债券
MarketUSZP = "USZP"  # 深圳退市整理

MarketUSTM = "USTM"  # 北交所

# =======================
FieldNameMap = {
    1: "time",  # 时间 根据周期，不同格式
    5: "code",  # 代码
    6: "prev_close",  # 昨收
    7: "open",  # 开盘
    8: "high",  # 最高
    9: "low",  # 最低
    10: "price",  # 现价
    11: "close",  # 收盘价
    12: "deal_type",  # 成交量分类 1是卖，5是买  委托中 2:委卖 1:委买
    13: "volume",  # 总量(手)
    14: "outer_volume",  # 外盘(手)
    15: "inner_volume",  # 内盘(手)
    16: "对倒成交量",  # 对倒成交量
    17: "开盘成交量",  # 开盘成交量 适用周期：K线
    18: "transaction_count",  # 交易笔数
    19: "turnover",  # 总金额 (元）
    20: "bid",  # 本次成交时的委托买入价 买价 在美元/人民币 看到用到
    21: "ask",  # 本次成交时的委托卖出价 卖价 在美元/人民币 看到用到
    22: "委买",  # 委买 #委托买入量 #对于个股：三档买入数量之和  #对于指数：本类指数所有股票的买入数量之和
    23: "委卖",  # 委卖  #委托卖出量 #对于个股：三档卖出数量之和 #对于指数：本类指数所有股票的卖出数量之和
    24: "bid1",  # 买一价
    25: "bid1_vol",  # 买一量(股)
    26: "bid2",
    27: "bid2_vol",
    28: "bid3",
    29: "bid3_vol",
    30: "ask1",  # 卖一价
    31: "ask1_vol",  # 卖一量
    32: "ask2",
    33: "ask2_vol",
    34: "ask3",
    35: "ask3_vol",
    36: "指数种类",  # 0-综合指数 1-A股 2-B股
    37: "本类股票总数",
    38: "涨家数",
    39: "跌家数",
    40: "领先指标",
    41: "上涨趋势",
    42: "下跌趋势",
    43: "最近一笔成交金额",  # 最近一笔成交金额(现额)
    44: "证券名称(繁体中文)",  # 证券名称(繁体中文)
    45: "五日成交总量",
    46: "证券名称(英文)",  # 证券名称(英文)
    47: "证券名称(Unicode)",  # 证券名称(Unicode)
    48: "rise_rate",  # 涨速
    49: "cur_volume",  # 当前量(手) 现量
    50: "代码(港)",
    53: "委比",
    54: "均价(中金所专用)",
    55: "name",
    56: "order_time",  # 挂单时间
    60: "H股昨收",
    61: "异动类型",
    64: "状态",
    65: "持仓",
    66: "昨结",  # ??
    69: "limit_up",  # 涨停
    70: "limit_down",  # 跌停
    71: "现增仓",
    72: "今结",
    73: "昨持仓",
    74: "bid_order_id",  # 暂时在L2中看到
    75: "ask_order_id",  # 暂时在L2中看到
    80: "利息",
    82: "撤单时间",
    84: "所属行业",
    85: "盈利情况",
    89: "转让状态相关参数",
    90: "流通市值",
    91: "市盈率",
    92: "总市值",
    93: "交易单位",
    95: "52周最高",
    96: "52周最低",
    100: "现价(港)",
    102: "bid6",  # 买6
    103: "bid6_vol",  # 买6量
    104: "ask6",
    105: "ask6_vol",
    106: "bid7",
    107: "bid7_vol",
    108: "ask7",
    109: "ask7_vol",
    110: "bid8",
    111: "bid8_vol",
    112: "ask8",
    113: "ask8_vol",
    114: "bid9",
    115: "bid9_vol",
    116: "ask9",
    117: "ask9_vol",
    118: "bid10",
    119: "bid10_vol",
    120: "ask10",
    121: "ask10_vol",
    122: "委买均价",  # 全档接口
    123: "总委买量",  # 全档接口
    124: "委卖均价",  # 全档接口
    125: "总委卖量",  # 全档接口
    130: "总手(港)",
    141: "波动性中断参考价格",  # 波动性中断参考价格
    142: "波动性中断集合竞价虚拟匹配量",  # 波动性中断集合竞价虚拟匹配量
    143: "合约代码",  # 合约代码
    144: "标的证券代码",  # 标的证券代码
    145: "基础证券证券名称",  # 基础证券证券名称
    146: "标的证券类型",  # 标的证券类型
    147: "欧式美式",  # 欧式美式
    148: "认购认沽",  # 认购认沽
    149: "合约单位",  # 合约单位
    150: "bid4",
    151: "bid4_vol",
    152: "ask4",
    153: "ask4_vol",
    154: "bid5",
    155: "bid5_vol",
    156: "ask5",
    157: "ask5_vol",
    160: "市场分层",
    191: "买差价",
    192: "卖差价",
    201: "主动买入特大单量",  # 主动买入特大单量
    202: "主动卖出特大单量",  # 主动卖出特大单量
    203: "主动买入大单量",  # 主动买入大单量
    204: "主动卖出大单量",  # 主动卖出大单量
    205: "主动买入中单量",  # 主动买入中单量
    206: "主动卖出中单量",  # 主动卖出中单量
    207: "被动买入特大单量",  # 被动买入特大单量
    208: "被动卖出特大单量",  # 被动卖出特大单量
    209: "被动买入大单量",  # 被动买入大单量
    210: "被动卖出大单量",  # 被动卖出大单量
    211: "被动买入中单量",  # 被动买入中单量
    212: "被动卖出中单量",  # 被动卖出中单量
    213: "主动买入小单量",  # 主动买入小单量
    214: "主动卖出小单量",  # 主动卖出小单量
    215: "主动买入特大单笔数",  # 主动买入特大单笔数
    216: "主动卖出特大单笔数",  # 主动卖出特大单笔数
    217: "主动买入大单笔数",  # 主动买入大单笔数
    218: "主动卖出大单笔数",  # 主动卖出大单笔数
    219: "被动买入特大单笔数",  # 被动买入特大单笔数
    220: "被动卖出特大单笔数",  # 被动卖出特大单笔数
    221: "被动买入大单笔数",  # 被动买入大单笔数
    222: "被动卖出大单笔数",  # 被动卖出大单笔数
    223: "主动买入特大单金额",
    224: "主动卖出特大单金额",
    225: "主动买入大单金额",
    226: "主动卖出大单金额",
    227: "被动买入特大单金额",
    228: "被动卖出特大单金额",
    229: "被动买入大单金额",
    230: "被动卖出大单金额",
    231: "买入单数量",
    232: "卖出单数量",
    233: "资金流入",
    234: "资金流出",
    235: "大单净量正",
    236: "大单净量负",
    237: "主动买入小单金额",
    238: "主动卖出小单金额",
    239: "成交笔数",
    240: "昨日收盘收益率",  # 昨日收盘收益率
    241: "昨日加权平均收益率",  # 昨日加权平均收益率
    242: "开盘收益率",  # 开盘收益率
    243: "最高收益率",  # 最高收益率
    244: "最低收益率",  # 最低收益率
    245: "最新收益率",  # 最新收益率
    246: "当日加权平均收益率",  # 当日加权平均收益率
    250: "委托买入前五档金额",
    251: "委托卖出前五档金额",
    252: "委托买入前十档金额",
    253: "委托卖出前十档金额",
    255: "主动买入中单笔数",  # 主动买入中单笔数
    256: "主动卖出中单笔数",  # 主动卖出中单笔数
    257: "被动买入中单笔数",  # 被动买入中单笔数
    258: "被动卖出中单笔数",  # 被动卖出中单笔数
    259: "主动买入中单金额",  # 主动买入中单金额
    260: "主动卖出中单金额",  # 主动卖出中单金额
    261: "被动买入中单金额",  # 被动买入中单金额
    262: "被动卖出中单金额",  # 被动卖出中单金额
    271: "五十二周最高日期",  # ?
    272: "五十二周最低日期",  # ?
    273: "年度最高日期",  # ?
    274: "年度最低日期",  # ?
    275: "领涨股",  # ?
    276: "涨停家数",  # ?
    277: "跌停家数",  # ?
    278: "盘后最新价",  # ?
    279: "港股指数人民币成交金额",  # ?
    # 仅对个股期权有效
    280: "期权行权价",  # 期权行权价
    281: "首个交易日",  # 首个交易日
    282: "最后交易日",  # 最后交易日
    283: "期权行权日",  # 期权行权日
    284: "期权到期日",  # 期权到期日
    285: "合约版本号",  # 合约版本号
    286: "行权交割日",  # 行权交割日
    288: "标的证券前收盘",  # 标的证券前收盘
    289: "涨跌幅限制类型",  # 涨跌幅限制类型
    290: "保证金计算比例参数一",  # 保证金计算比例参数一
    291: "保证金计算比例参数二",  # 保证金计算比例参数二
    292: "单位保证金",  # 单位保证金
    294: "整手数",  # 整手数
    295: "单笔限价申报下限",  # 单笔限价申报下限
    296: "单笔限价申报上限",  # 单笔限价申报上限
    297: "单笔市价申报下限",  # 单笔市价申报下限
    298: "单笔市价申报上限",  # 单笔市价申报上限
    299: "期权合约状态信息标签",  # 期权合约状态信息标签
    402: "总股本",
    407: "流通股本",
    410: "流通B股",
    471: "权息资料",
    497: "转股价",  # 可以用于计算可转债溢价
    499: "债券余额",  # 万
    520: "流动资产",
    543: "资产总计",
    593: "公积金",
    602: "主营收入",
    605: "营业利润",
    615: "利润总额",
    619: "净利润",
    672: "申购限额(万股)",
    675: "实际涨幅",
    676: "首日振幅",
    873: "引伸波幅",
    874: "对冲值",
    875: "街货占比",
    876: "街货量",
    877: "最后交易日",
    879: "回收价",
    880: "牛熊证种类",
    881: "标的证券",
    882: "权证类型",
    887: "行使价",
    888: "换股比率",
    890: "到期日",
    899: "财务数据项",
    900: "流通股变动量",
    981: "港元->人民币汇率",
    1002: "每股收益",
    1005: "每股净资产",
    1015: "净资产收益",
    1024: "债券规模",  # 可转债 单位亿
    1047: "转股起始日",  # 可转债
    1110: "星级",
    1121: "标记",
    1322: "利率%",
    1384: "融资余额",  # 单位元
    1385: "融券余额",  # 单位元
    1386: "融资买入",  # 单位元
    1387: "融劵卖出",  # 单位股
    1566: "净利润",
    1606: "发行价",
    1612: "中签率%",
    1670: "股东总数",
    1674: "流通A股",
    2026: "评级",  # 可转债
    2039: "纯债价值",  # 可转债
    2041: "期权价值",  # 可转债
    2570: "卖出信号",
    2579: "机构持股比例",
    2719: "人均持股数",
    2942: "市盈(动)",
    2946: "市盈(静)",
    2947: "市净率",
    3153: "市盈TTM",
    3250: "5日涨幅",
    3251: "10日涨幅",
    3252: "20日涨幅",
    3397: "净值",
    9810: "溢价率",
    32772: "时间戳",
    68107: "板块主力净量",  # 板块 又是板块净量？ 和68285 相同
    68166: "板块主力流入",
    68167: "板块主力流出",
    68213: "板块主力净流入",  # 板块 68166-68167
    68285: "板块主力净量",  # 板块
    68759: "板块开盘价",  # 板块
    133702: "细分行业",
    133778: "基差",
    133964: "日增仓",
    134071: "市销TTM",
    134072: "净资产收益TTM",
    134141: "净利润增长率",
    134143: "营业收入增长率",
    134152: "市盈率(静态)",
    134160: "换股比率",
    134162: "折溢率",
    134237: "杠杆比率",
    134238: "溢价",
    199112: "change_rate",  # 涨幅%
    199643: "大单净量",
    264648: "change",  # 涨幅
    330321: "异动类型",
    330322: "竞价评级",
    330325: "涨停类型",
    330329: "涨停状态",
    331070: "今日主力增仓占比%",
    331077: "2日主力增仓占比%",
    331078: "3日主力增仓占比%",
    331079: "5日主力增仓占比%",
    331080: "10日主力增仓占比%",
    331124: "2日主力增仓排名",
    331125: "3日主力增仓排名",
    331126: "5日主力增仓排名",
    331127: "10日主力增仓排名",
    331128: "今日主力增仓排名",
    395720: "委比",
    461256: "委比%",
    461346: "年初至今涨幅",
    461438: "涨速%(10分)",
    461439: "涨速%(15分)",
    462057: "散户数量",
    526792: "amplitude",  # 振幅%
    527198: "uk_527198",
    527526: "涨速%(3分)",
    527527: "涨速%(1分)",
    592544: "贡献度",
    592920: "市净率-1",
    592741: "机构动向",
    592888: "主力净量",
    592890: "主力净流入",
    592893: "5日大单净量",
    592894: "10日大单净量",
    592946: "多空比",
    625362: "每股公积金",
    625295: "dealNum",  # ??
    658784: "金叉个数",
    658785: "利好",
    658786: "利空",
    920371: "开盘涨幅",
    920372: "实体涨幅",
    920428: "股票分类标记",
    1149395: "市净率-2",
    1378761: "avg_price",  # 均价 可以使用看看有没有穿过均价
    1509847: "户均持股数",
    1640904: "手/笔",
    1771976: "volume_ratio",  # 量比
    1968584: "turnover_rate",  # 换手%
    1991120: "涨幅(港)",
    2034120: "市盈(动)",
    2034121: "资产负债率",
    2097453: "流通股",
    2263506: "流通比例%",
    2427336: "均笔额",
    2646480: "H股涨跌",
    2820564: "内盘",
    3082712: "涨幅(结)%",
    3475914: "流通市值",
    3541450: "总市值",
    3934664: "涨速%",  # block 涨速
    4065737: "买价",
    4099083: "日增仓",
    4131273: "卖价",
    4525375: "小单流入",
    4525376: "中单流入",
    4525377: "大单流入",
    7000001: "占基金规模",
    7000002: "持股变动",
    7000003: "基金规模",
    7000004: "代码",
    7000005: "涨幅%",
    7000006: "持股变动",
    7000007: "占基金规模",
    7000008: "业绩表现",
    7000009: "近一年收益",
    7000010: "近一周收益",
    7000011: "近一月收益",
    7000012: "近三月收益",
    7000013: "今年以来收益",
    7000014: "成立以来",
    7000015: "产品类型",
    7000016: "基金规模",
    7000017: "基金公司",
    7000018: "投资类型",
    7000019: "基金经理",
    7000020: "资产占比",
    7000021: "较上期",
    8311855: "类别",
    8719679: "小单流出",
    8719680: "中单流出",
    8719681: "大单流出",
    12345671: "A股关联主题",
    12913983: "小单净额",
    12913984: "中单净额",
    12913985: "大单净额",
    17108287: "小单净额占比%",
    17108288: "中单净额占比%",
    17108289: "大单净额占比%",
    18550831: "成分股数",
    20190901: "标签",
    21302591: "小单总额",
    21302592: "中单总额",
    21302593: "大单总额",
    25496895: "小单总额占比%",
    25496896: "中单总额占比%",
    25496897: "大单总额占比%",
    189546735: "计算数据项",
    2018090319: "竞价评级",
    2018090320: "竞价异动类型及说明颜色判断字段",
    2018090410: "异动说明",
    2018090411: "竞价涨幅",
}


class QuoteLib:
    def __init__(self, ops: dict = ()):
        self.__lib_path = self._get_lib_path()

        self._lib = ctypes.CDLL(self.__lib_path)
        self._lib.NewQuote.argtypes = [ctypes.c_char_p]
        self._lib.NewQuote.restype = None
        self._lib.Connect.restype = ctypes.c_char_p
        self._lib.DisConnect.restype = ctypes.c_char_p
        self._lib.QueryData.argtypes = [ctypes.c_char_p]
        self._lib.QueryData.restype = ctypes.c_char_p
        self._lib.About.restype = ctypes.c_char_p
        self._lib.NewQuote(json.dumps(ops).encode('utf-8'))

    def _get_lib_path(self):
        # todo M芯片暂未支持
        system = platform.system()
        arch = platform.machine()
        if system == 'Linux':
            lib_path = os.path.join(os.path.dirname(__file__), 'libquote.so')
        elif system == 'Darwin':  # intel
            lib_path = os.path.join(os.path.dirname(__file__), 'libquote.dylib')
        elif system == 'Windows':
            lib_path = os.path.join(os.path.dirname(__file__), 'libquote.dll')
        else:
            raise OSError('Unsupported operating system')
        return lib_path

    def connect(self):
        return self._lib.Connect()

    def disconnect(self):
        return self._lib.DisConnect()

    def query_data(self, req: str):
        return self._lib.QueryData(req.encode('utf-8'))

    def about(self):
        # 版本信息 About
        return self._lib.About()


class ResponseData:
    _fields_ = ["type", "data", "dic_extra", "extra"]

    def __init__(self, data_dict: dict):
        self.type = data_dict.get('type', "")
        self.data = data_dict.get('data', [])
        self.dic_extra = data_dict.get('dic_extra', {})
        self.extra = data_dict.get('extra', None)

    def __repr__(self):
        return f"ResponseData(type={self.type}, data={self.data}, dic_extra={self.dic_extra}, extra={self.extra})"

    def is_empty(self) -> bool:
        """Check if the data field is empty."""
        return not bool(self.data)

    def get_extra_value(self, key: str, default=None):
        """Retrieve a value from dic_extra with a default fallback."""
        return self.dic_extra.get(key, default)

    def to_dict(self) -> dict:
        """Convert the object to a dictionary."""
        return {
            "type": self.type,
            "data": self.data,
            "dic_extra": self.dic_extra,
            "extra": self.extra,
        }


class Response:
    _fields_ = ["err_code", "err_message", "resp"]

    def __init__(self, json_str: str):
        try:
            data_dict: Dict[str, Any] = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

        self.err_code: int = data_dict.get("err_code", 0)
        self.err_message: str = data_dict.get("err_message", "")
        self.resp: ResponseData = ResponseData(data_dict.get("data", {}))

    def __repr__(self):
        return f"Response(err_code={self.err_code}, err_message={self.err_message}, data={self.resp})"

    def convert_data(self):
        """Convert the keys of the data field using a utility function."""
        self.resp.data = _convert_data_keys(self.resp.data or [])

    def is_success(self) -> bool:
        """Check if the response indicates success."""
        return self.err_code == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dictionary."""
        return {
            "err_code": self.err_code,
            "err_message": self.err_message,
            "resp": self.resp.to_dict() if self.resp else None,
        }


class THS:
    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', zhu_addr)
        account = rand_account()
        ops.setdefault("username", account[0])
        ops.setdefault("password", account[1])

        self.ops = ops
        self._lib = QuoteLib(ops)
        self._login = False
        self.__share_instance = random.randint(6666666, 8888888)

    @property
    def zip_version(self):
        return 2

    @property
    def share_instance(self):
        self.__share_instance += 1
        return self.__share_instance

    def connect(self):
        """
        连接到行情服务器
        :return:
        """
        response = self._lib.connect()
        if response == "" or response is None or response == b'':
            raise ValueError("No data found.")

        rs = Response(response)
        if rs.err_code == 0:
            self._login = True
        return rs

    def disconnect(self):
        """
        断开与行情服务器的连接
        :return:
        """
        self._login = False

        response = self._lib.disconnect()
        rs = Response(response)
        return rs

    def about(self):
        """
        关于信息
        :return:
        """
        about = self._lib.about()
        return about.decode('utf-8')

    @staticmethod
    def login_required(func):
        def wrapper(self, *args, **kwargs):
            if not self._login:
                print("请先登录.")
                reply = Response("{}")
                return reply
            return func(self, *args, **kwargs)

        return wrapper

    @login_required
    def history_minute_time_data(self, code: str, date: str, fields: list = None):
        # 检查code的长度和前四位         # if len(code) != 10 or not (code.startswith('USHA') or code.startswith('USZA')):
        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        # 检查date的格式
        if not re.match(r'^\d{8}$', date):
            raise ValueError("Date must be in the format YYYYMMDD, e.g. 20241220.")

        data_type = "1,10,13,19,40"
        market = code[:4]
        short_code = code[4:]
        req = f"id=207&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&datatype={data_type}&date={date}"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No history data found.")

        reply = Response(response)
        reply.convert_data()

        for entry in reply.resp.data:
            if "time" in entry:  # 检查是否存在 "time" 键
                entry["time"] = _ths_int2time(entry["time"])

        if fields:
            reply.resp.data = [entry for entry in reply.resp.data if all(field in entry for field in fields)]

        return reply

    @login_required
    def security_bars(self, code: str, start: int, end: int, adjust: str, period: int):
        """
        获取k线数据。

        :param code: 证券代码，必须是10个字符长，并以'USHA'或'USZA'开头。
        :param start: 开始时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
        :param end: 结束时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
        :param adjust: 复权类型，必须是有效的复权值之一。
        :param period: 周期类型，必须是有效的周期值之一。
        """

        valid_fuquan = AdjustedType.all_types()
        valid_periods = KlinePeriod.all_periods()

        if adjust not in valid_fuquan:
            raise ValueError("Invalid adjust.")

        if period not in valid_periods:
            raise ValueError("Invalid period.")

        m_period = {KlinePeriod.MIN_1, KlinePeriod.MIN_5, KlinePeriod.MIN_15, KlinePeriod.MIN_30, KlinePeriod.MIN_60,
                    KlinePeriod.MIN_120}

        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        data_type = "1,7,8,9,11,13,19"
        market = code[:4]
        short_code = code[4:]
        req = f"id=210&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&start={start}&end={end}&fuquan={adjust}&datatype={data_type}&period={period}"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No history data found.")

        reply = Response(response)
        reply.convert_data()

        if period in m_period:
            for entry in reply.resp.data:
                if "time" in entry:  # 检查是否存在 "time" 键
                    entry["time"] = _ths_int2time(entry["time"])
        else:
            for entry in reply.resp.data:
                if "time" in entry:  # 检查是否存在 "time" 键
                    entry["time"] = datetime.datetime.strptime(str(entry["time"]), "%Y%m%d")

        return reply

    @login_required
    def get_block_data(self, block_id: int):
        """
        :param block_id: 板块代码，必须是有效的板块代码。
            0xC6A6 # 全部A股
            0xE # 沪深A股
            0x15 # 沪市A股
            0x1B # 深市A股
            0xC5E3 # 北京A股
            0xCFE4 # 创业板
            0xCBE5 # 科创板
            0xDBC6 # 风险警示
            0xDBC7 # 退市整理
            0xF026 # 行业和概念
            0xCE5E # 概念
            0xCE5F # 行业
            0xc4b5 # 行业二级 0xc4b5/0xcd1a/ 0xf04c
            0xc4b7 # 行业一二级 0xc4b7
            0xdffb # 地域
            0xD385 # 国内外重要指数
            0xDB5E # 股指期货
            0xCBBE # 科创板
            0xCBBD #blockDataFromBlockServer(
            0xD2 # 全部指数
            0xCE3F # 上证系列指数
            0xCE3E # 深证系列指数
            0xCE3D # 中证系列指数
            0xC2B0 # 北证系列指数
            0xCFF3 # ETF基金
            0x6 # 沪深封闭式基金
            0x4 # 沪封闭式基金
            0x5 # 深封闭式基金
            0xEF8C # LOF基金
            0xD811 # 分级基金
            0xD90C # T+0 基金
            0xC7B1 # 沪REITs
            0xC7A0 # 深REITs
            0xC89C # 沪深REITs
            0xCE14 # 可转债
            0xCE17 # 国债
            0xCE0B # 上证债券
            0xCE0A # 深证债券
            0xCE12 # 回购
            0xCE11 # 贴债
            0xCE16 # 地方债
            0xCE15 # 企业债
            0xD8D4 # 小公募
        :return: 包含成分股信息的 Reply 对象。
        """
        if not block_id:
            raise ValueError("Block Id must be provided.")

        if 'addr' in self.ops:
            addr = self.ops['addr']
            if addr != block_addr:
                raise ValueError("Block data can only be queried from block server.")

        req = f"id=7&instance={self.share_instance}&zipversion={self.zip_version}&sortbegin=0&sortcount=0&sortorder=D&sortid=55&blockid={block_id:x}&reqflag=blockserver"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No sector components data found.")

        reply = Response(response)
        reply.convert_data()

        return reply

    @login_required
    def get_block_components(self, block_code: str):
        """
        获取板块成分股数据

        :param block_code: 板块代码 eg:URFI881273
        :return:
        """
        if not block_code:
            raise ValueError("Block code must be provided.")

        req = f"id=7&instance={self.share_instance}&zipversion={self.zip_version}&sortbegin=0&sortcount=0&sortorder=D&sortid=55&linkcode={block_code}"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No sector components data found.")

        reply = Response(response)
        reply.convert_data()

        return reply

    @login_required
    def get_transaction_data(self, code: str, start: int, end: int):
        """
        获取股票3秒tick成交数据
        :param code: 股票代码
        :param start: 时间戳/倒序
        :param end: 时间戳/倒序
        :return:  Reply 对象。
        """

        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        data_type = "1,5,10,12,18,49"
        market = code[:4]
        short_code = code[4:]
        req = f"id=205&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&start={start}&end={end}&datatype={data_type}&TraceDetail=0"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No data found." + req)

        reply = Response(response)
        reply.convert_data()

        return reply

    @login_required
    def get_super_transaction_data(self, code: str, start: int, end: int):
        """
        获取股票3秒超级盘口数据，带委托档位
        :param code: 股票代码
        :param start: 时间戳
        :param end: 时间戳
        :return:  Reply 对象。
        """
        if start >= end:
            raise ValueError("Start timestamp must be less than end timestamp.")

        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        data_type = "1,5,7,10,12,13,14,18,19,20,21,25,26,27,28,29,31,32,33,34,35,49,69,70,92,123,125,150,151,152,153,154,155,156,157,45,66,661,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,123,125"
        market = code[:4]
        short_code = code[4:]
        req = f"id=205&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&start={start}&end={end}&datatype={data_type}&TraceDetail=0"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No data found." + req)

        reply = Response(response)
        reply.convert_data()

        return reply

    @login_required
    def get_l2_transaction_data(self, code: str, start: int, end: int):
        """
        获取股票l2成交数据

        :param code: 股票代码
        :param start: 时间戳
        :param end: 时间戳
        :return:  Reply 对象。
        """

        if len(code) != 10:
            raise ValueError("Code must be 10 characters long and start with 'USHA' or 'USZA'.")

        data_type = "5,10,12,13"
        market = code[:4]
        short_code = code[4:]
        req = f"id=220&instance={self.share_instance}&zipversion={self.zip_version}&code={short_code}&market={market}&start={start}&end={end}&datatype={data_type}"
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No data found." + req)

        reply = Response(response)
        reply.convert_data()

        return reply

    def query_ths_industry(self):
        """
        获取行业板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xCE5F)

    def query_ths_sub_industry(self):
        """
        获取细分三级行业板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xc4b5)

    def query_ths_concept(self):
        """
        获取概念板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xCE5E)

    def query_ths_bond(self):
        """
        获取可转债板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xCE14)

    def query_ths_index(self):
        """
        获取指数板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xD2)

    def query_ths_etf(self):
        """
        获取ETF板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xCFF3)

    def query_ths_etf_t0(self):
        """
        获取ETF T0板块

        :return:  Reply 对象。
        """
        return self.get_block_data(0xD90C)

    @login_required
    def query_data(self, req: str, ):
        response = self._lib.query_data(req)
        if response == "" or response is None or response == b'':
            raise ValueError("No data found." + req)

        reply = Response(response)
        reply.convert_data()

        return reply


class ZhuTHS(THS):
    """
        ZhuThsQuote 主行情数据
        """

    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', zhu_addr)
        super().__init__(ops)


class FuTHS(THS):
    """
    FuThsQuote 副行情数据
    """

    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', fu_addr)
        super().__init__(ops)


class InfoTHS(THS):
    """
    InfoThsQuote 获取资讯信息类型数据
    """

    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', info_addr)
        super().__init__(ops)


class BlockTHS(THS):
    """
    BlockThsQuote 获取板块类型数据
    """

    def __init__(self, ops: dict = None):
        ops = ops or {}
        ops.setdefault('addr', block_addr)
        super().__init__(ops)
