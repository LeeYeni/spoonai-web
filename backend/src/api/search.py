from fastapi import APIRouter, Depends, Request
from typing import List

from src.service.search_pipeline import SearchPipeline
from src.api.dependency import get_search_pipeline, get_client_ip
from src.schema.search import SearchRequest, SearchResponse

router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)

@router.post("/", response_model=List[SearchResponse])
async def recommend(
    ip_request: Request,
    request: SearchRequest,
    service: SearchPipeline = Depends(get_search_pipeline)
):
    ip_address = get_client_ip(ip_request)
    return await service.recommend(ip_address, request.x, request.y, request.query)