
# -*- coding: UTF-8 -*-


from pathlib import Path

from fastapi import FastAPI

from ..core import MetricDB

from .info.http import MetricInfoHttpRouter
from .info.ws import MetricInfoWsRouter
from .entry.http import MetricEntryHttpRouter
from .entry.ws import MetricEntryWsRouter



class MdbAPI(FastAPI):

    def __init__(self, filename: Path):
        super().__init__()
        self.mdb = MetricDB(filename)
        self.include_router(MetricInfoHttpRouter(self.mdb), prefix="/api/v1")
        self.include_router(MetricInfoWsRouter(self.mdb), prefix="/wsapi/v1")
        self.include_router(MetricEntryHttpRouter(self.mdb), prefix="/api/v1")
        self.include_router(MetricEntryWsRouter(self.mdb), prefix="/wsapi/v1")

