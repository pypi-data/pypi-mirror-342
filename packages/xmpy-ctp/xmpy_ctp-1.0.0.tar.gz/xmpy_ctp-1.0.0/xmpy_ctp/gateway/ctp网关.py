import sys
from datetime import datetime
from time import sleep
from pathlib import Path
from typing import Dict, List, Set, Tuple

from xmpy.包_事件引擎 import 类_事件引擎
from xmpy.包_交易核心.模块_常数 import (
    类_方向,
    类_开平,
    类_交易所,
    类_委托类型,
    类_产品类型,
    类_状态,
    类_期权类型
)
from xmpy.包_交易核心.模块_网关 import 类_基础网关
from xmpy.包_交易核心.模块_对象 import (
    类_行情数据,
    类_委托数据,
    类_成交数据,
    类_持仓数据,
    类_账户数据,
    类_合约数据,
    类_委托请求,
    类_撤单请求,
    类_订阅请求
)
from xmpy.包_交易核心.模块_工具 import 获取目录路径, ZoneInfo
from xmpy.包_交易核心.模块_事件类型 import (事件类型_定时)

from ..api import (
    MdApi,
    TdApi,
    THOST_FTDC_OST_NoTradeQueueing,
    THOST_FTDC_OST_PartTradedQueueing,
    THOST_FTDC_OST_AllTraded,
    THOST_FTDC_OST_Canceled,
    THOST_FTDC_OST_Unknown,
    THOST_FTDC_D_Buy,
    THOST_FTDC_D_Sell,
    THOST_FTDC_PD_Long,
    THOST_FTDC_PD_Short,
    THOST_FTDC_OPT_LimitPrice,
    THOST_FTDC_OPT_AnyPrice,
    THOST_FTDC_OF_Open,
    THOST_FTDC_OFEN_Close,
    THOST_FTDC_OFEN_CloseYesterday,
    THOST_FTDC_OFEN_CloseToday,
    THOST_FTDC_PC_Futures,
    THOST_FTDC_PC_Options,
    THOST_FTDC_PC_SpotOption,
    THOST_FTDC_PC_Combination,
    THOST_FTDC_CP_CallOptions,
    THOST_FTDC_CP_PutOptions,
    THOST_FTDC_HF_Speculation,
    THOST_FTDC_CC_Immediately,
    THOST_FTDC_FCC_NotForceClose,
    THOST_FTDC_TC_GFD,
    THOST_FTDC_VC_AV,
    THOST_FTDC_TC_IOC,
    THOST_FTDC_VC_CV,
    THOST_FTDC_AF_Delete
)

# 委托状态映射
状态映射_CTP转VT: dict[str, 类_状态] = {
    THOST_FTDC_OST_NoTradeQueueing: 类_状态.未成交,
    THOST_FTDC_OST_PartTradedQueueing: 类_状态.部分成交,
    THOST_FTDC_OST_AllTraded: 类_状态.全部成交,
    THOST_FTDC_OST_Canceled: 类_状态.已撤销,
    THOST_FTDC_OST_Unknown: 类_状态.提交中
}

# 方向映射
方向映射_VT转CTP: dict[类_方向, str] = {
    类_方向.做多: THOST_FTDC_D_Buy,
    类_方向.做空: THOST_FTDC_D_Sell
}
方向映射_CTP转VT: dict[str, 类_方向] = {v: k for k, v in 方向映射_VT转CTP.items()}
方向映射_CTP转VT[THOST_FTDC_PD_Long] = 类_方向.做多
方向映射_CTP转VT[THOST_FTDC_PD_Short] = 类_方向.做空

# 委托类型映射
委托类型映射_VT转CTP: dict[类_委托类型, tuple] = {
    类_委托类型.限价单: (THOST_FTDC_OPT_LimitPrice, THOST_FTDC_TC_GFD, THOST_FTDC_VC_AV),
    类_委托类型.市价单: (THOST_FTDC_OPT_AnyPrice, THOST_FTDC_TC_GFD, THOST_FTDC_VC_AV),
    类_委托类型.立即成交剩余撤销: (THOST_FTDC_OPT_LimitPrice, THOST_FTDC_TC_IOC, THOST_FTDC_VC_AV),
    类_委托类型.全部成交否则撤销: (THOST_FTDC_OPT_LimitPrice, THOST_FTDC_TC_IOC, THOST_FTDC_VC_CV),
}
委托类型映射_CTP转VT: dict[tuple, 类_委托类型] = {v: k for k, v in 委托类型映射_VT转CTP.items()}

# 开平方向映射
开平映射_VT转CTP: dict[类_开平, str] = {
    类_开平.开仓: THOST_FTDC_OF_Open,
    类_开平.平仓: THOST_FTDC_OFEN_Close,
    类_开平.平今: THOST_FTDC_OFEN_CloseToday,
    类_开平.平昨: THOST_FTDC_OFEN_CloseYesterday,
}
开平映射_CTP转VT: dict[str, 类_开平] = {v: k for k, v in 开平映射_VT转CTP.items()}

# 交易所映射
交易所映射_CTP转VT: dict[str, 类_交易所] = {
    "CFFEX": 类_交易所.中金所,
    "SHFE": 类_交易所.上期所,
    "CZCE": 类_交易所.郑商所,
    "DCE": 类_交易所.大商所,
    "INE": 类_交易所.能源中心,
    "GFEX": 类_交易所.广期所
}

# 产品类型映射
产品类型映射_CTP转VT: dict[str, 类_产品类型] = {
    THOST_FTDC_PC_Futures: 类_产品类型.期货,
    THOST_FTDC_PC_Options: 类_产品类型.期权,
    THOST_FTDC_PC_SpotOption: 类_产品类型.期权,
    THOST_FTDC_PC_Combination: 类_产品类型.价差
}

# 期权类型映射
期权类型映射_CTP转VT: dict[str, 类_期权类型] = {
    THOST_FTDC_CP_CallOptions: 类_期权类型.看涨,
    THOST_FTDC_CP_PutOptions: 类_期权类型.看跌
}

# 常量定义
最大浮点数 = sys.float_info.max
中国时区 = ZoneInfo("Asia/Shanghai")       # 中国时区
合约映射表: dict[str, 类_合约数据] = {}


class 类_CTP网关(类_基础网关):
    """CTP期货柜台网关"""

    默认名称: str = "CTP"
    默认配置: dict[str, str] = {
        "用户名": "",
        "密码": "",
        "经纪商代码": "",
        "交易服务器": "",
        "行情服务器": "",
        "产品名称": "",
        "授权编码": ""
    }
    支持交易所: list[类_交易所] = list(交易所映射_CTP转VT.values())

    def __init__(self, 事件引擎: 类_事件引擎, 网关名称: str) -> None:
        super().__init__(事件引擎, 网关名称)

        self.交易接口: "类_CTP交易接口" = 类_CTP交易接口(self)
        self.行情接口: "类_CTP行情接口"  = 类_CTP行情接口(self)

    def 连接(self, 配置: dict) -> None:
        """建立连接"""
        用户名 = 配置["用户名"]
        密码 = 配置["密码"]
        经纪商代码 = 配置["经纪商代码"]
        交易地址 = 配置["交易服务器"]
        行情地址 = 配置["行情服务器"]
        产品名称 = 配置["产品名称"]
        授权编码 = 配置["授权编码"]

        # 补充协议前缀
        if not 交易地址.startswith(("tcp://", "ssl://", "socks")):
            交易地址 = "tcp://" + 交易地址
        if not 行情地址.startswith(("tcp://", "ssl://", "socks")):
            行情地址 = "tcp://" + 行情地址

        self.交易接口.连接(交易地址, 用户名, 密码, 经纪商代码, 授权编码, 产品名称)
        self.行情接口.连接(行情地址, 用户名, 密码, 经纪商代码)
        self.初始化查询()

    def 订阅行情(self, 请求: 类_订阅请求) -> None:
        self.行情接口.订阅(请求)

    def 发送委托(self, 请求: 类_委托请求) -> str:
        return self.交易接口.发送委托(请求)

    def 撤消订单(self, 请求: 类_撤单请求) -> None:
        self.交易接口.撤消订单(请求)

    def 查询账户(self) -> None:
        self.交易接口.查询账户()

    def 查询持仓(self) -> None:
        self.交易接口.查询持仓()

    def 断开连接(self) -> None:
        self.交易接口.关闭()
        self.行情接口.关闭()

    def 记录错误(self, 信息: str, 错误: dict) -> None:
        """记录错误日志"""
        错误码 = 错误["ErrorID"]
        错误信息 = 错误["ErrorMsg"]
        self.记录日志(f"{信息}，代码：{错误码}，信息：{错误信息}")

    def 处理定时事件(self, 事件) -> None:
        """定时任务处理"""
        self.计数器 += 1
        if self.计数器 < 2:
            return
        self.计数器 = 0

        查询函数 = self.查询任务列表.pop(0)
        查询函数()
        self.查询任务列表.append(查询函数)

        self.行情接口.更新日期()

    def 初始化查询(self) -> None:
        """初始化周期查询"""
        self.计数器 = 0
        self.查询任务列表 = [self.查询账户, self.查询持仓]
        self.事件引擎.注册类型处理器(事件类型_定时, self.处理定时事件)


class 类_CTP行情接口(MdApi):
    """CTP行情接口实现"""

    def __init__(self, 网关: 类_CTP网关):
        super().__init__()
        self.网关 = 网关
        self.网关名称 = 网关.网关名称

        self.请求编号 = 0
        self.连接状态 = False
        self.登录状态 = False
        self.订阅集合 = set()

        self.用户号 = ""
        self.密码 = ""
        self.经纪商代码 = ""
        self.当前日期 = datetime.now().strftime("%Y%m%d")

    def onFrontConnected(self):
        """前端连接成功"""
        self.网关.记录日志("行情服务器连接成功")
        self.登录()

    def onFrontDisconnected(self, 原因: int):
        """前端连接断开"""
        self.登录状态 = False
        self.网关.记录日志(f"行情服务器连接断开，原因：{原因}")

    def onRspUserLogin(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """登录回报"""
        if not 错误["ErrorID"]:
            self.登录状态 = True
            self.网关.记录日志("行情服务器登录成功")
            # 重新订阅
            for 代码 in self.订阅集合:
                self.subscribeMarketData(代码) 
        else:
            self.网关.记录错误("行情登录失败", 错误)

    def onRspSubMarketData(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """订阅回报"""
        if 错误["ErrorID"]:
            self.网关.记录错误("行情订阅失败", 错误)

    def onRtnDepthMarketData(self, 数据: dict):
        """行情推送"""
        if not 数据["UpdateTime"]:
            return

        代码 = 数据["InstrumentID"]
        合约 = 合约映射表.get(代码)
        if not 合约:
            return

        # 处理交易日
        if not 数据["ActionDay"] or 合约.交易所 == 类_交易所.大商所:
            日期 = self.当前日期
        else:
            日期 = 数据["ActionDay"]

        # 生成时间戳
        时间戳 = f"{日期} {数据['UpdateTime']}.{数据['UpdateMillisec']}"
        时间对象 = datetime.strptime(时间戳, "%Y%m%d %H:%M:%S.%f").replace(tzinfo=中国时区)

        # 创建行情对象
        tick = 类_行情数据(
            代码=代码,
            交易所=合约.交易所,
            时间戳=时间对象,
            名称=合约.名称,
            成交量=数据["Volume"],
            成交额=数据["Turnover"],
            持仓量=数据["OpenInterest"],
            最新价=调整价格(数据["LastPrice"]),
            涨停价=调整价格(数据["UpperLimitPrice"]),
            跌停价=调整价格(数据["LowerLimitPrice"]),
            开盘价=调整价格(数据["OpenPrice"]),
            最高价=调整价格(数据["HighestPrice"]),
            最低价=调整价格(数据["LowestPrice"]),
            昨收价=调整价格(数据["PreClosePrice"]),
            买一价=调整价格(数据["BidPrice1"]),
            买一量=数据["BidVolume1"],
            卖一价=调整价格(数据["AskPrice1"]),
            卖一量=数据["AskVolume1"],
            网关名称=self.网关名称
        )

        # 处理五档行情
        if 数据["BidVolume2"]:
            tick.买二价 = 调整价格(数据["BidPrice2"])
            tick.买三价 = 调整价格(数据["BidPrice3"])
            tick.买四价 = 调整价格(数据["BidPrice4"])
            tick.买五价 = 调整价格(数据["BidPrice5"])
            tick.卖二价 = 调整价格(数据["AskPrice2"])
            tick.卖三价 = 调整价格(数据["AskPrice3"])
            tick.卖四价 = 调整价格(数据["AskPrice4"])
            tick.卖五价 = 调整价格(数据["AskPrice5"])
            tick.买二量 = 数据["BidVolume2"]
            tick.买三量 = 数据["BidVolume3"]
            tick.买四量 = 数据["BidVolume4"]
            tick.买五量 = 数据["BidVolume5"]
            tick.卖二量 = 数据["AskVolume2"]
            tick.卖三量 = 数据["AskVolume3"]
            tick.卖四量 = 数据["AskVolume4"]
            tick.卖五量 = 数据["AskVolume5"]

        self.网关.推送行情(tick)

    def 连接(self, 地址: str, 用户号: str, 密码: str, 经纪商代码: str):
        """连接服务器"""
        self.用户号 = 用户号
        self.密码 = 密码
        self.经纪商代码 = 经纪商代码

        if not self.连接状态:
            路径 = 获取目录路径(self.网关名称.lower())
            self.createFtdcMdApi(f"{路径}\\Md".encode("GBK"))
            self.registerFront(地址)
            self.init()
            self.连接状态 = True

    def 登录(self):
        """用户登录"""
        请求 = {
            "UserID": self.用户号,
            "Password": self.密码,
            "BrokerID": self.经纪商代码
        }
        self.请求编号 += 1
        self.reqUserLogin(请求, self.请求编号)

    def 订阅(self, 请求: 类_订阅请求):
        """订阅行情"""
        if self.登录状态:
            self.subscribeMarketData(请求.代码)
        self.订阅集合.add(请求.代码)

    def 关闭(self):
        """关闭连接"""
        if self.连接状态:
            self.exit()

    def 更新日期(self):
        """更新当前日期"""
        self.当前日期 = datetime.now().strftime("%Y%m%d")


class 类_CTP交易接口(TdApi):
    """CTP交易接口实现"""

    def __init__(self, 网关: 类_CTP网关):
        super().__init__()
        self.网关 = 网关
        self.网关名称 = 网关.网关名称

        self.请求编号 = 0
        self.委托编号 = 0
        self.连接状态 = False
        self.登录状态 = False
        self.认证状态 = False
        self.合约就绪 = False

        self.用户号 = ""
        self.密码 = ""
        self.经纪商代码 = ""
        self.授权码 = ""
        self.应用编号 = ""

        self.前置编号 = 0
        self.会话编号 = 0
        self.委托缓存 = []
        self.成交缓存 = []
        self.持仓字典 = {}
        self.系统委托映射 = {}

    def onFrontConnected(self):
        """前端连接成功"""
        if self.授权码:
            self.认证()
        else:
            self.登录()

    def onRspAuthenticate(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """认证回报"""
        if not 错误["ErrorID"]:
            self.认证状态 = True
            self.网关.记录日志("交易服务器认证成功")
            self.登录()
        else:
            self.网关.记录错误("交易认证失败", 错误)

    def onRspUserLogin(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """登录回报"""
        if not 错误["ErrorID"]:
            self.前置编号 = 数据["FrontID"]
            self.会话编号 = 数据["SessionID"]
            self.登录状态 = True
            self.网关.记录日志("交易服务器登录成功")

            # 确认结算单
            请求 = {"BrokerID": self.经纪商代码, "InvestorID": self.用户号}
            self.请求编号 += 1
            self.reqSettlementInfoConfirm(请求, self.请求编号)
        else:
            self.网关.记录错误("交易登录失败", 错误)

    def onRspOrderInsert(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """委托失败"""
        委托编号 = f"{self.前置编号}_{self.会话编号}_{self.委托编号}"
        合约 = 合约映射表[数据["InstrumentID"]]

        委托 = 类_委托数据(
            代码=数据["InstrumentID"],
            交易所=合约.交易所,
            委托编号=委托编号,
            方向=方向映射_CTP转VT[数据["Direction"]],
            开平=开平映射_CTP转VT.get(数据["CombOffsetFlag"], 类_开平.NONE),
            价格=数据["LimitPrice"],
            数量=数据["VolumeTotalOriginal"],
            状态=类_状态.已拒单,
            网关名称=self.网关名称
        )
        self.网关.推送订单(委托)
        self.网关.记录错误("委托失败", 错误)

    def onRspOrderAction(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """撤单失败"""
        self.网关.记录错误("撤单失败", 错误)

    def onRspSettlementInfoConfirm(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """结算单确认"""
        self.网关.记录日志("结算单确认成功")
        while True:
            self.请求编号 += 1
            返回值 = self.reqQryInstrument({}, self.请求编号)
            if not 返回值:
                break
            sleep(1)

    def onRspQryInvestorPosition(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """持仓查询回报"""
        if not 数据:
            return

        代码 = 数据["InstrumentID"]
        合约 = 合约映射表.get(代码)
        if not 合约:
            return

        # 处理持仓数据
        键值 = f"{代码},{数据['PosiDirection']}"
        持仓 = self.持仓字典.get(键值)
        if not 持仓:
            持仓 = 类_持仓数据(
                代码=代码,
                交易所=合约.交易所,
                方向=方向映射_CTP转VT[数据["PosiDirection"]],
                网关名称=self.网关名称
            )
            self.持仓字典[键值] = 持仓

        # 处理不同交易所的昨仓
        if 持仓.交易所 in [类_交易所.上期所, 类_交易所.能源中心]:
            if 数据["YdPosition"] and not 数据["TodayPosition"]:
                持仓.昨仓量 = 数据["Position"]
        else:
            持仓.昨仓量 = 数据["Position"] - 数据["TodayPosition"]

        # 计算持仓成本
        合约乘数 = 合约.合约乘数
        持仓成本 = 持仓.价格 * 持仓.数量 * 合约乘数

        持仓.数量 += 数据["Position"]
        持仓.盈亏 += 数据["PositionProfit"]

        if 持仓.数量 and 合约乘数:
            持仓成本 += 数据["PositionCost"]
            持仓.价格 = 持仓成本 / (持仓.数量 * 合约乘数)

        # 更新冻结量
        if 持仓.方向 == 类_方向.做多:
            持仓.冻结量 += 数据["ShortFrozen"]
        else:
            持仓.冻结量 += 数据["LongFrozen"]

        if 最后标识:
            for 持仓 in self.持仓字典.values():
                self.网关.推送持仓(持仓)
            self.持仓字典.clear()

    def onRspQryTradingAccount(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """资金查询回报"""
        账户 = 类_账户数据(
            账户编号=数据["AccountID"],
            余额=数据["Balance"],
            冻结金额=数据["FrozenMargin"] + 数据["FrozenCash"] + 数据["FrozenCommission"],
            网关名称=self.网关名称
        )
        账户.可用金额=数据["Available"]
        self.网关.推送账户(账户)

    def onRspQryInstrument(self, 数据: dict, 错误: dict, 请求编号: int, 最后标识: bool):
        """合约查询回报"""
        产品类型 = 产品类型映射_CTP转VT.get(数据["ProductClass"])
        if 产品类型:
            合约 = 类_合约数据(
                代码=数据["InstrumentID"],
                交易所=交易所映射_CTP转VT[数据["ExchangeID"]],
                名称=数据["InstrumentName"],
                产品类型=产品类型,
                合约乘数=数据["VolumeMultiple"],
                最小价位=数据["PriceTick"],
                最小数量=数据["MinLimitOrderVolume"],
                最大数量=数据["MaxLimitOrderVolume"],
                网关名称=self.网关名称
            )

            # 处理期权合约
            if 合约.产品类型 == 产品类型.期权:
                if 合约.交易所 == 类_交易所.郑商所:
                    合约.期权组合 = 数据["ProductID"][:-1]
                else:
                    合约.期权组合 = 数据["ProductID"]

                合约.标的合约 = 数据["UnderlyingInstrID"]
                合约.期权类型 = 期权类型映射_CTP转VT.get(数据["OptionsType"])
                合约.行权价 = 数据["StrikePrice"]
                合约.上市日 = datetime.strptime(数据["OpenDate"], "%Y%m%d")
                合约.到期日 = datetime.strptime(数据["ExpireDate"], "%Y%m%d")

            self.网关.推送合约(合约)
            合约映射表[合约.代码] = 合约

        if 最后标识:
            self.合约就绪 = True
            self.网关.记录日志("合约信息查询完成")
            self.网关.记录日志("-----------------------------------------")

            # 处理缓存的委托和成交
            for 委托数据 in self.委托缓存:
                self.onRtnOrder(委托数据)
            self.委托缓存.clear()

            for 成交数据 in self.成交缓存:
                self.onRtnTrade(成交数据)
            self.成交缓存.clear()

    def onRtnOrder(self, 数据: dict):
        """委托更新"""
        if not self.合约就绪:
            self.委托缓存.append(数据)
            return

        代码 = 数据["InstrumentID"]
        合约 = 合约映射表[代码]
        委托编号 = f"{数据['FrontID']}_{数据['SessionID']}_{数据['OrderRef']}"

        # 转换状态
        状态 = 状态映射_CTP转VT.get(数据["OrderStatus"])
        if not 状态:
            self.网关.记录日志(f"未知委托状态：{数据['OrderStatus']}")
            return

        # 转换时间
        时间戳 = f"{数据['InsertDate']} {数据['InsertTime']}"
        时间对象 = datetime.strptime(时间戳, "%Y%m%d %H:%M:%S").replace(tzinfo=中国时区)

        # 转换委托类型
        类型元组 = (数据["OrderPriceType"], 数据["TimeCondition"], 数据["VolumeCondition"])
        委托类型 = 委托类型映射_CTP转VT.get(类型元组)
        if not 委托类型:
            self.网关.记录日志(f"未知委托类型：{类型元组}")
            return

        委托 = 类_委托数据(
            代码=代码,
            交易所=合约.交易所,
            委托编号=委托编号,
            类型=委托类型,
            方向=方向映射_CTP转VT[数据["Direction"]],
            开平=开平映射_CTP转VT[数据["CombOffsetFlag"]],
            价格=数据["LimitPrice"],
            数量=数据["VolumeTotalOriginal"],
            已成交=数据["VolumeTraded"],
            状态=状态,
            时间戳=时间对象,
            网关名称=self.网关名称
        )
        self.网关.推送订单(委托)
        self.系统委托映射[数据["OrderSysID"]] = 委托编号

    def onRtnTrade(self, 数据: dict):
        """成交推送"""
        if not self.合约就绪:
            self.成交缓存.append(数据)
            return

        代码 = 数据["InstrumentID"]
        合约 = 合约映射表[代码]
        委托编号 = self.系统委托映射[数据["OrderSysID"]]

        时间戳 = f"{数据['TradeDate']} {数据['TradeTime']}"
        时间对象 = datetime.strptime(时间戳, "%Y%m%d %H:%M:%S").replace(tzinfo=中国时区)

        成交 = 类_成交数据(
            代码=代码,
            交易所=合约.交易所,
            订单编号=委托编号,
            成交编号=数据["TradeID"],
            方向=方向映射_CTP转VT[数据["Direction"]],
            开平=开平映射_CTP转VT[数据["OffsetFlag"]],
            价格=数据["Price"],
            数量=数据["Volume"],
            时间戳=时间对象,
            网关名称=self.网关名称
        )
        self.网关.推送成交(成交)

    def 连接(self, 地址: str, 用户号: str, 密码: str, 经纪商代码: str, 授权码: str, 应用编号: str):
        """连接交易服务器"""
        self.用户号 = 用户号
        self.密码 = 密码
        self.经纪商代码 = 经纪商代码
        self.授权码 = 授权码
        self.应用编号 = 应用编号

        if not self.连接状态:
            路径 = 获取目录路径(self.网关名称.lower())
            self.createFtdcTraderApi(f"{路径}\\Td".encode("GBK"))
            self.subscribePrivateTopic(0)
            self.subscribePublicTopic(0)
            self.registerFront(地址)
            self.init()
            self.连接状态 = True
        else:
            self.认证()

    def 认证(self):
        """发起认证"""
        请求 = {
            "UserID": self.用户号,
            "BrokerID": self.经纪商代码,
            "AuthCode": self.授权码,
            "AppID": self.应用编号
        }
        self.请求编号 += 1
        self.reqAuthenticate(请求, self.请求编号)

    def 登录(self):
        """用户登录"""
        请求 = {
            "UserID": self.用户号,
            "Password": self.密码,
            "BrokerID": self.经纪商代码
        }
        self.请求编号 += 1
        self.reqUserLogin(请求, self.请求编号)

    def 发送委托(self, 请求: 类_委托请求) -> str:
        """处理委托请求"""
        if 请求.开平 not in 开平映射_VT转CTP:
            self.网关.记录日志("无效开平方向")
            return ""

        if 请求.类型 not in 委托类型映射_VT转CTP:
            self.网关.记录日志(f"不支持的委托类型：{请求.类型}")
            return ""

        self.委托编号 += 1
        价格类型, 时间条件, 成交量条件 = 委托类型映射_VT转CTP[请求.类型]

        委托请求 = {
            "InstrumentID": 请求.代码,
            "ExchangeID": 请求.交易所.value,
            "LimitPrice": 请求.价格,
            "VolumeTotalOriginal": int(请求.数量),
            "OrderPriceType": 价格类型,
            "Direction": 方向映射_VT转CTP[请求.方向],
            "CombOffsetFlag": 开平映射_VT转CTP[请求.开平],
            "OrderRef": str(self.委托编号),
            "InvestorID": self.用户号,
            "BrokerID": self.经纪商代码,
            "CombHedgeFlag": THOST_FTDC_HF_Speculation,
            "ContingentCondition": THOST_FTDC_CC_Immediately,
            "ForceCloseReason": THOST_FTDC_FCC_NotForceClose,
            "IsAutoSuspend": 0,
            "TimeCondition": 时间条件,
            "VolumeCondition": 成交量条件,
            "MinVolume": 1
        }

        self.请求编号 += 1
        返回值 = self.reqOrderInsert(委托请求, self.请求编号)
        if 返回值:
            self.网关.记录日志(f"委托请求发送失败，错误码：{返回值}")
            return ""

        # 生成委托记录
        委托编号 = f"{self.前置编号}_{self.会话编号}_{self.委托编号}"
        委托 = 请求.生成委托数据(委托编号, self.网关名称)
        self.网关.推送订单(委托)
        return 委托.订单唯一标识

    def 撤消订单(self, 请求: 类_撤单请求):
        """处理撤单请求"""
        前置号, 会话号, 委托引用 = 请求.订单编号.split("_")
        撤单请求 = {
            "InstrumentID": 请求.代码,
            "ExchangeID": 请求.交易所.value,
            "OrderRef": 委托引用,
            "FrontID": int(前置号),
            "SessionID": int(会话号),
            "ActionFlag": THOST_FTDC_AF_Delete,
            "BrokerID": self.经纪商代码,
            "InvestorID": self.用户号
        }
        self.请求编号 += 1
        self.reqOrderAction(撤单请求, self.请求编号)

    def 查询账户(self):
        """查询资金"""
        self.请求编号 += 1
        self.reqQryTradingAccount({}, self.请求编号)

    def 查询持仓(self):
        """查询持仓"""
        if not 合约映射表:
            return

        请求 = {"BrokerID": self.经纪商代码, "InvestorID": self.用户号}
        self.请求编号 += 1
        self.reqQryInvestorPosition(请求, self.请求编号)

    def 关闭(self):
        """关闭连接"""
        if self.连接状态:
            self.exit()


def 调整价格(价格: float) -> float:
    """处理异常价格"""
    return 0 if 价格 == 最大浮点数 else 价格
