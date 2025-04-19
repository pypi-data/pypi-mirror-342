
# -*- coding: UTF-8 -*-


import os
from pathlib import Path


from ._client import _MdbClient
from .local import MdbLocalClient
from .remote import MdbRemoteClient
from .model import *



class MdbClient(_MdbClient):

    def __init__(
        self,
        uri: str = None
    ):

        if uri is None:
            uri = os.environ.get("MDB_URI", "")

        if not uri:
            raise ValueError("URI must be provided via argument or MDB_URI environment variable")

        if uri.startswith(("http://", "https://")):
            self.impl = MdbRemoteClient(uri)
        else:
            self.mdb = MetricDB(Path(uri))
            self.impl = MdbLocalClient(self.mdb)


    def list_metric_info(
        self
    ) -> List[MetricInfo]:
        return self.impl.list_metric_info()


    def query_metric_info(
        self,
        key         : MetricKey
    ) -> MetricInfo:
        return self.impl.query_metric_info(key)


    def update_metric_info(
        self,
        info        : MetricInfo
    ) -> MetricInfo:
        return self.impl.update_metric_info(info)


    async def async_update_metric_info(
        self,
        info        : MetricInfo
    ) -> MetricInfo:
        return await self.impl.async_update_metric_info(info)


    def query_metric_entry(
        self,
        key         : str,
        test        : ITest                 = None,
        dut         : IDut                  = None,
        start_time  : ITime                 = None,
        end_time    : ITime                 = None,
    ) -> List[MetricEntry]:
        return self.impl.query_metric_entry(key, test, dut, start_time, end_time)


    def add_metric_entry(
        self,
        key         : MetricKey,
        entry       : MetricEntry,
        test        : ITest                 = None,
        dut         : IDut                  = None,
    ) -> MetricEntry:
        return self.impl.add_metric_entry(key, entry, test, dut)


    async def async_add_metric_entry(
        self,
        key         : MetricKey,
        entry       : MetricEntry,
        test        : ITest                 = None,
        dut         : IDut                  = None,
    ) -> MetricEntry:
        return await self.impl.async_add_metric_entry(key, entry, test, dut)


    def batch_update_metric_info(
        self,
        infos       : Iterator[MetricInfo]
    ) -> List[MetricInfo]:
        return self.impl.batch_update_metric_info(infos)


    async def abatch_update_metric_info(
        self,
        infos       : AsyncIterator[MetricInfo]
    ) -> List[MetricInfo]:
        return await self.impl.abatch_update_metric_info(infos)


    def batch_add_metric_entry(
        self,
        key         : MetricKey,
        entries     : Iterator[MetricEntry],
        test        : ITest                 = None,
        dut         : IDut                  = None,
    ) -> List[MetricEntry]:
        return self.impl.batch_add_metric_entry(key, entries, test, dut)


    async def abatch_add_metric_entry(
        self,
        key         : MetricKey,
        entries     : AsyncIterator[MetricEntry],
        test        : ITest                 = None,
        dut         : IDut                  = None,
    ) -> List[MetricEntry]:
        return await self.impl.abatch_add_metric_entry(key, entries, test, dut)


