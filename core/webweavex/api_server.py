from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .async_engine import AsyncWebWeaveX
from .models import PageResult


class UrlRequest(BaseModel):
  url: str


app = FastAPI(title="WebWeaveX API", version="0.1.0")
_engine = AsyncWebWeaveX()


@app.on_event("shutdown")
async def _shutdown_engine() -> None:
  await _engine.aclose()


@app.post("/crawl", response_model=PageResult)
async def crawl(request: UrlRequest) -> PageResult:
  return await _engine.crawl(request.url)


@app.post("/crawl_site", response_model=list[PageResult])
async def crawl_site(request: UrlRequest) -> list[PageResult]:
  return await _engine.crawl_site(request.url)


@app.post("/rag_dataset")
async def rag_dataset(request: UrlRequest) -> list[dict[str, object]]:
  return await _engine.build_rag_dataset(request.url)


@app.post("/knowledge_graph")
async def knowledge_graph(request: UrlRequest) -> dict[str, list[dict[str, str]]]:
  return await _engine.build_knowledge_graph(request.url)
