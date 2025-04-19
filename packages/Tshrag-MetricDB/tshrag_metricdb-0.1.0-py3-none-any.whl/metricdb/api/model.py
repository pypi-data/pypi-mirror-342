
# -*- coding: UTF-8 -*-


from dataclasses import asdict

from pydantic import BaseModel

from ..core.typing import IMetricKey, ITest, IDut, ITime, IDuration, IValue
from ..core.typing import TMetricKey, TTest, TDut, TTime, TDuration, TValue
from ..core.typing import CMetricKey, CTest, CDut, CTime, CDuration, CValue
from ..core import Time
from ..core import TestId, DutId
from ..core import MetricKey, MetricInfo, MetricEntry
from ..core import MetricDB



def _CoreMixin(cls):
    class _CoreMixin:

        def tocore(self, **kwargs):
            return cls(**kwargs, **self.model_dump())

        @classmethod
        def fromcore(cls, obj, **kwargs):
            return cls(**kwargs, **asdict(obj))

    return _CoreMixin


class TMetricInfo(BaseModel, _CoreMixin(MetricInfo)):
    key             : TMetricKey
    name            : str
    description     : str


class MetricInfoUpdateRequest(BaseModel, _CoreMixin(MetricInfo)):
    name            : str
    description     : str


class KeyMetricInfoUpdateRequest(BaseModel, _CoreMixin(MetricInfo)):
    key             : TMetricKey
    name            : str
    description     : str


class TMetricEntry(BaseModel, _CoreMixin(MetricEntry)):
    time            : TTime
    duration        : TDuration
    value           : TValue


class MetricEntryAddRequest(BaseModel, _CoreMixin(MetricEntry)):
    time            : TTime
    duration        : TDuration
    value           : TValue


class KeyMetricEntryAddRequest(BaseModel):
    key             : TMetricKey
    entry           : TMetricEntry
    test            : TTest                 = None
    dut             : TDut                  = None


