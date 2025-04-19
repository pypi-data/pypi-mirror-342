
# -*- coding: UTF-8 -*-


from abc import ABC, abstractmethod
from typing import Iterator, AsyncIterator, List

from ..core.typing import IMetricKey, ITest, IDut, ITime, IDuration, IValue
from ..core.typing import TMetricKey, TTest, TDut, TTime, TDuration, TValue
from ..core.typing import CMetricKey, CTest, CDut, CTime, CDuration, CValue
from ..core import Time
from ..core import TestId, DutId
from ..core import MetricKey, MetricInfo, MetricEntry
from ..core import MetricDB



async def _aiterator(iterable: Iterator) -> AsyncIterator:
    for item in iterable:
        yield item


class _MdbClient(ABC):


    @abstractmethod
    def list_metric_info(
        self
    ) -> List[MetricInfo]:
        """List all metric info."""
        pass


    @abstractmethod
    def query_metric_info(
        self,
        key         : MetricKey
    ) -> MetricInfo:
        """Query metric info by key."""
        pass


    @abstractmethod
    def update_metric_info(
        self,
        info        : MetricInfo
    ) -> MetricInfo:
        """Update metric info."""
        pass


    @abstractmethod
    async def async_update_metric_info(
        self,
        info        : MetricInfo
    ) -> MetricInfo:
        """Async update metric info."""
        pass


    @abstractmethod
    def query_metric_entry(
        self,
        key         : str,
        test        : ITest                 = None,
        dut         : IDut                  = None,
        start_time  : ITime                 = None,
        end_time    : ITime                 = None,
    ) -> List[MetricEntry]:
        """Query metric entry by key."""
        pass


    @abstractmethod
    def add_metric_entry(
        self,
        key         : MetricKey,
        entry       : MetricEntry,
        test        : ITest                 = None,
        dut         : IDut                  = None,
    ) -> MetricEntry:
        """Add metric entry."""
        pass


    @abstractmethod
    async def async_add_metric_entry(
        self,
        key         : MetricKey,
        entry       : MetricEntry,
        test        : ITest                 = None,
        dut         : IDut                  = None,
    ) -> MetricEntry:
        """Async add metric entry."""
        pass


    def batch_update_metric_info(
        self,
        info        : Iterator[MetricInfo]
    ) -> List[MetricInfo]:
        """Batch update metric info."""
        return [self.update_metric_info(i) for i in info]


    async def abatch_update_metric_info(
        self,
        info        : AsyncIterator[MetricInfo]
    ) -> List[MetricInfo]:
        """Async batch update metric info."""
        return [await self.async_update_metric_info(i) for i in info]


    def batch_add_metric_entry(
        self,
        key         : MetricKey,
        entry       : Iterator[MetricEntry],
        test        : ITest                 = None,
        dut         : IDut                  = None,
    ) -> List[MetricEntry]:
        """Batch add metric entry."""
        return [self.add_metric_entry(key, i, test, dut) for i in entry]


    async def abatch_add_metric_entry(
        self,
        key         : MetricKey,
        entry       : AsyncIterator[MetricEntry],
        test        : ITest                 = None,
        dut         : IDut                  = None,
    ) -> List[MetricEntry]:
        """Async batch add metric entry."""
        return [await self.async_add_metric_entry(key, i, test, dut) for i in entry]


