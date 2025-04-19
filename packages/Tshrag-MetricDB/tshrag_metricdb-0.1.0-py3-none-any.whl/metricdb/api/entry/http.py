
# -*- coding: UTF-8 -*-


from typing import List

from fastapi import APIRouter
from fastapi import Query

from ..model import *



def MetricEntryHttpRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.get("/metric/entry")
    @router.get("/metric/entry/{key}")
    @router.get("/metric/entry/{test}/{key}")
    def query_metric_entry(
        key         : str,
        test        : TTest                 = None,
        dut         : TDut                  = Query(None),
        start_time  : TTime                 = Query(None),
        end_time    : TTime                 = Query(None),
    ) -> List[TMetricEntry]:
        response = [
            TMetricEntry.fromcore(entry)
            for entry in mdb.query_metric_entry(
                key         = str(key),
                test        = test and TestId(test),
                dut         = dut and {DutId(d) for d in dut},
                start_time  = start_time and Time(start_time),
                end_time    = end_time and Time(end_time),
            )
        ]
        return response


    @router.post("/metric/entry")
    @router.post("/metric/entry/{key}")
    @router.post("/metric/entry/{test}/{key}")
    def add_metric_entry(
        key         : TMetricKey,
        test        : TTest                 = None,
        dut         : TDut                  = Query(None),
        request     : MetricEntryAddRequest = None,
    ) -> TMetricEntry:
        entry = request.tocore()
        mdb.add_metric_entry(
            key     = MetricKey(key),
            entry   = entry,
            test    = test and TestId(test),
            dut     = dut and {DutId(d) for d in dut},
        )
        response = TMetricEntry.fromcore(entry)
        return response


    return router


