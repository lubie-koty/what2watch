from pydantic import BaseModel

class Recommendation(BaseModel):
    title: str
    vote_count: int
    vote_average: float
    score: float


class RecommendationList(BaseModel):
    recommendations: list[Recommendation]


class ChatResponse(BaseModel):
    is_successful: bool
    error_message: str | None
    data: list[str] | None
