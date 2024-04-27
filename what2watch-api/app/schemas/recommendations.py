from pydantic import BaseModel

class Recommendation(BaseModel):
    title: str
    vote_count: int
    vote_average: float
    score: float


class RecommendationList(BaseModel):
    recommendations: list[Recommendation]


class TitleList(BaseModel):
    titles: list[str]
