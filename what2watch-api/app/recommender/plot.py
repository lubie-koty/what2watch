import numpy as np
import pandas as pd

from fastapi import HTTPException, status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from app.recommender import DATA_PATH
from app.schemas.recommendations import ChatResponse
from app.utils.input import parse_input_title


class PlotRecommender:
    def __init__(self):
        self.__load_plot_recommender()

    def __load_plot_recommender(self) -> None:
        tfidf = TfidfVectorizer(stop_words='english')
        metadata = pd.read_csv(f'{DATA_PATH}/movies_metadata.csv', low_memory=False)
        metadata = metadata.drop([19730, 29503, 35587])
        metadata['overview'] = metadata['overview'].fillna('')

        tfidf_matrix = tfidf.fit_transform(metadata['overview'])
        self.__cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)
        self.__indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates().drop(labels=np.nan)
        self.__dataset = metadata

    def get_recommendations(self, title: str) -> ChatResponse:
        parsed_title = parse_input_title(title, self.__indices)
        try:
            movie_index = self.indices[parsed_title]
        except KeyError:
            return ChatResponse(
                is_successful=False,
                error_message=f'Could not find recommendation for "{title}"'
            )
        similar_scores = list(enumerate(self.__cosine_similarity[movie_index]))
        similar_scores = sorted(similar_scores, key=lambda x: np.any(x[1]), reverse=True)
        return ChatResponse(
            is_successful=True,
            data=list(self.__dataset['title'].iloc[[i[0] for i in similar_scores[1:10]]])
        )
