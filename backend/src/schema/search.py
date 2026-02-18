from pydantic import BaseModel, HttpUrl

class SearchRequest(BaseModel):
    x: float
    y: float
    query: str

class SearchResponse(BaseModel):
    restaurant: str
    place_url: HttpUrl