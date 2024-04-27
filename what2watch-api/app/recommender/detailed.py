from ast import literal_eval

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.recommender import DATA_PATH


def _get_director(data) -> str | float:
    return next((i for i in data if i['job'] == 'Director'), np.nan)


def _get_list(data) -> list[str]:
    if isinstance(data, list):
        return [i['name'] for i in data][:3]
    return []


def _clean_data(data) -> list | str:
    if isinstance(data, list):
        return [i.replace(' ', '').lower() for i in data]
    elif isinstance(data, str):
        return data.replace(' ', '').lower()
    return ''


def _create_soup(data) -> str:
    return f'{" ".join(data["keywords"])} {" ".join(data["cast"])} {data["director"]} {" ".join(data["genres"])}'


class DetailedRecommender:
    def __init__(self):
        self.__load_detailed_recommender()

    def __load_detailed_recommender(self) -> None:
        count_vectorizer = CountVectorizer(stop_words='english')
        metadata = pd.read_csv(f'{DATA_PATH}/movies_metadata.csv', low_memory=False)
        # metadata = metadata.drop([19730, 29503, 35587])
        movie_credits = pd.read_csv(f'{DATA_PATH}/credits.csv')
        keywords = pd.read_csv(f'{DATA_PATH}/keywords.csv')

        metadata['id'] = metadata['id'].astype('int')
        movie_credits['id'] = movie_credits['id'].astype('int')
        keywords['id'] = keywords['id'].astype('int')

        metadata = metadata.merge(movie_credits, on='id').merge(keywords, on='id')
        for feature in ['cast', 'crew', 'keywords', 'genres']:
            metadata[feature] = metadata[feature].apply(literal_eval)
        metadata['director'] = metadata['crew'].apply(_get_director)
        for feature in ['cast', 'keywords', 'genres']:
            metadata[feature] = metadata[feature].apply(_get_list)
        for feature in ['cast', 'keywords', 'director', 'genres']:
            metadata[feature] = metadata[feature].apply(_clean_data)
        metadata['soup'] = metadata.apply(_create_soup, axis=1)

        count_matrix = count_vectorizer.fit_transform(metadata['soup'])
        metadata = metadata.reset_index()
        self.cosine_similarity = cosine_similarity(count_matrix, count_matrix)
        self.indices = pd.Series(metadata.index, index=metadata['title'])
        self.dataset = metadata


    def get_recommendations(self, title: str) -> pd.DataFrame:
        movie_index = self.indices[title]
        similar_scores = list(enumerate(self.cosine_similarity[movie_index]))
        similar_scores = sorted(similar_scores, key=lambda x: np.any(x[1]), reverse=True)
        return self.dataset['title'].iloc[[i[0] for i in similar_scores[1:10]]]

