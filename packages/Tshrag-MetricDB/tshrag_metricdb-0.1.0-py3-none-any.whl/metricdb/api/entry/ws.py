
# -*- coding: UTF-8 -*-


from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from ..model import *



def MetricEntryWsRouter(mdb: MetricDB) -> APIRouter:

    router = APIRouter()


    @router.websocket("/metric/entry")
    async def add_metric_entry(websocket: WebSocket) -> None:
        await websocket.accept()
        try:
            while True:
                request = KeyMetricEntryAddRequest(**await websocket.receive_json())
                mdb.add_metric_entry(
                    key     = MetricKey(request.key),
                    entry   = request.entry.tocore(),
                    test    = request.test and TestId(request.test),
                    dut     = request.dut and {DutId(d) for d in request.dut},
                )
        except WebSocketDisconnect:
            pass


    return router


