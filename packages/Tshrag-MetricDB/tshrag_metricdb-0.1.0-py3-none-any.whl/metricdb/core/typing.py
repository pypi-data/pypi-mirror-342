
# -*- coding: UTF-8 -*-

from typing import Union, Optional, Generic, TypeVar
from typing import Iterable, Iterator, AsyncIterator
from typing import Tuple, List, Set, Dict, Any

from .time import Time
from .identifier import TestId, DutId
from .metric import MetricKey, MetricInfo, MetricEntry


IMetricKey          = MetricKey
ITest               = Optional[TestId]
IDut                = Optional[Union[DutId, Iterable[DutId]]]
ITime               = Optional[Time]
IDuration           = Optional[int]
IValue              = Any


TMetricKey          = str
TTest               = Optional[str]
TDut                = Optional[List[str]]
TTime               = Optional[Union[int, str]]
TDuration           = Optional[int]
TValue              = Union[int, float, str]


def _CDut(dut: IDut) -> TDut:
    return dut and (
        [str(d) for d in set(dut)]
        if isinstance(dut, (tuple, list, set))
        else str(dut)
    )


def _CValue(value: IValue) -> TValue:
    for _t in [int, float, str]:
        try:
            return _t(value)
        except:
            pass
    raise ValueError("Invalid value")


CMetricKey          = str
CTest               = str
CDut                = _CDut
CTime               = int
CDuration           = int
CValue              = _CValue


