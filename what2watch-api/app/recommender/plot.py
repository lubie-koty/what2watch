import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from app.recommender import DATA_PATH


class PlotRecommender:
    def __init__(self):
        self.__load_plot_recommender()

    def __load_plot_recommender(self) -> None:
        tfidf = TfidfVectorizer(stop_words='english')
        metadata = pd.read_csv(f'{DATA_PATH}/movies_metadata.csv', low_memory=False)
        metadata['overview'] = metadata['overview'].fillna('')

        tfidf_matrix = tfidf.fit_transform(metadata['overview'])
        self.cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix)
        self.indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()
        self.dataset = metadata

    def get_recommendations(self, title: str) -> pd.DataFrame:
        movie_index = self.indices[title]
        similar_scores = list(enumerate(self.cosine_similarity[movie_index]))
        similar_scores = sorted(similar_scores, key=lambda x: np.any(x[1]), reverse=True)
        return self.dataset['title'].iloc[[i[0] for i in similar_scores[1:10]]]

