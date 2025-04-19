
# -*- coding: UTF-8 -*-


from abc import ABC, abstractmethod
from typing import Union, Optional, Generic, TypeVar
from typing import Iterable, Iterator, AsyncIterator
from typing import Tuple, List, Set, Dict, Any

from pathlib import Path
from dataclasses import dataclass, asdict

from ..core.typing import IMetricKey, ITest, IDut, ITime, IDuration, IValue
from ..core.typing import TMetricKey, TTest, TDut, TTime, TDuration, TValue
from ..core.typing import CMetricKey, CTest, CDut, CTime, CDuration, CValue
from ..core import Time
from ..core import TestId, DutId
from ..core import MetricKey, MetricInfo, MetricEntry
from ..core import MetricDB



def _query(**d: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: v
        if isinstance(v, dict)
        else v
        for k, v in d.items()
        if v is not None
    }


def Query(
    key             : IMetricKey,
    test            : ITest                 = None,
    dut             : IDut                  = None,
    start_time      : ITime                 = None,
    end_time        : ITime                 = None,
) -> Dict[str, Any]:
    return _query(
        key         = CMetricKey(key),
        test        = test and CTest(test),
        dut         = dut and CDut(dut),
        start_time  = start_time and CTime(start_time),
        end_time    = end_time and CTime(end_time),
    )


def MetricInfoUpdateRequest(
    info            : MetricInfo
) -> Dict[str, Any]:
    return _query(
        name        = str(info.name),
        description = str(info.description),
    )


def KeyMetricInfoUpdateRequest(
    info            : MetricInfo
) -> Dict[str, Any]:
    return _query(
        key         = CMetricKey(info.key),
        name        = str(info.name),
        description = str(info.description),
    )


def MetricEntryAddRequest(
    entry           : MetricEntry
) -> Dict[str, Any]:
    return _query(
        time        = CTime(entry.time),
        duration    = CDuration(entry.duration),
        value       = CValue(entry.value),
    )


def KeyMetricEntryAddRequest(
    key             : MetricKey,
    entry           : MetricEntry,
    test            : ITest = None,
    dut             : IDut = None,
) -> Dict[str, Any]:
    return _query(
        key         = CMetricKey(key),
        entry       = _query(
            time    = CTime(entry.time),
            duration = CDuration(entry.duration),
            value   = CValue(entry.value),
        ),
        test        = test and CTest(test),
        dut         = dut and CDut(dut),
    )


