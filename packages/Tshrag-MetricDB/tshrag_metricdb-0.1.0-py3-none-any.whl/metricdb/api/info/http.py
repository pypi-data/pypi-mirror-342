
# -*- coding: UTF-8 -*-


from typing import List

from fastapi import APIRouter

from ..model import *



def MetricInfoHttpRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.get("/metric/infos")
    def list_metric_info(
    ) -> List[TMetricInfo]:
        response = [
            TMetricInfo.fromcore(info)
            for info in mdb.list_metric_info()
        ]
        return response


    @router.get("/metric/info")
    @router.get("/metric/info/{key}")
    def query_metric_info(
        key         : TMetricKey
    ) -> TMetricInfo:
        info = mdb.query_metric_info(
            key     = str(key),
        )
        response = TMetricInfo.fromcore(info)
        return response


    @router.post("/metric/info")
    @router.post("/metric/info/{key}")
    def update_metric_info(
        key         : TMetricKey,
        request     : MetricInfoUpdateRequest
    ) -> TMetricInfo:
        info = request.tocore(key=key)
        mdb.update_metric_info(
            info    = info,
        )
        response = TMetricInfo.fromcore(info)
        return response


    return router

