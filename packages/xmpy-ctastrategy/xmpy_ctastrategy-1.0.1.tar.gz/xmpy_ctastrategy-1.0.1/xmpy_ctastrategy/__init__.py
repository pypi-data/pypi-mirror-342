from pathlib import Path
from typing import Type
import importlib_metadata
from xmpy.包_交易核心.模块_应用 import 类_基础应用
from xmpy.包_交易核心.模块_对象 import 类_行情数据,类_K线数据,类_成交数据,类_委托数据
from xmpy.包_交易核心.模块_常数 import 类_方向,类_开平
from xmpy.包_交易核心.模块_工具 import 类_K线生成器, 类_数组管理器

from .模块_基础 import 应用名称, 类_停止单
from .模块_CTA引擎 import 类_CTA引擎
from .模块_模板 import 类_CTA策略模板,类_CTA信号,类_目标仓位模板

try:
    __版本__ = importlib_metadata.version("xmpy_ctastrategy")
except importlib_metadata.PackageNotFoundError:
    __版本__ = "开发版"


class 类_CTA策略应用(类_基础应用):
    """CTA策略交易应用"""
    from .包_国际化 import _

    应用名称: str = 应用名称
    应用模块: str = __module__
    应用路径: Path = Path(__file__).parent
    显示名称: str = _("CTA策略")
    引擎类: Type[类_CTA引擎] = 类_CTA引擎
    组件名称: str = "CTA管理界面"
    图标名称: str = str(应用路径.joinpath("ui", "cta.ico"))
