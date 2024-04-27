from numbers import Number
from functools import partial

import pandas as pd

from app.recommender import DATA_PATH
from app.schemas.recommendations import Recommendation, RecommendationList


def _weighted_rating(df: pd.DataFrame, mean: Number, minimum: Number) -> Number:
    vote_count = df['vote_count']
    vote_average = df['vote_average']
    return (vote_count / (vote_count + mean) * vote_average) + (mean / (mean + vote_count) * minimum)


class SimpleRecommender:
    def __init__(self):
        self.__load_simple_recommender()

    def __load_simple_recommender(self) -> None:
        metadata = pd.read_csv(f'{DATA_PATH}/movies_metadata.csv', low_memory=False)

        mean_of_votes = metadata['vote_average'].mean()
        minimum_n_of_votes = metadata['vote_count'].quantile(0.9)

        metadata = metadata.loc[metadata['vote_count'] >= minimum_n_of_votes]
        rating_function = partial(_weighted_rating, mean=mean_of_votes, minimum=minimum_n_of_votes)
        metadata['score'] = metadata.apply(rating_function, axis=1)
        self.__dataset = metadata.sort_values('score', ascending=False)

    def get_recommendations(self, number_of_movies: int) -> RecommendationList:
        recommendations = self.__dataset[['title', 'vote_count', 'vote_average', 'score']].head(number_of_movies)
        return RecommendationList(
            recommendations=[
                Recommendation(
                    title=r['title'],
                    vote_count=r['vote_count'],
                    vote_average=r['vote_average'],
                    score=r['score']
                )
                for r in recommendations
            ]
        )
