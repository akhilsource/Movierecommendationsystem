import numpy as np
import pandas as pd
import difflib
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar(name='Iron Man'):
    data = pd.read_csv("D:/project_recommedation_system/movies.csv")
    # data = data.iloc[100, :]
    selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director', 'crew']
    for feature in selected_features:
        data[feature] = data[feature].fillna('')
    combined_features = data[selected_features].apply(lambda x: ' '.join(x), axis=1)
    
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(combined_features)
    similarity = cosine_similarity(feature_vectors)

    titles = data['title'].to_list()
    close_matches = difflib.get_close_matches(name, titles)
    close_match = close_matches[0]
    index_movie = data[data.title == close_match]['index'].values[0]
    similarity_Score = list(enumerate(similarity[index_movie]))
    sorted_similar_movies = sorted(similarity_Score, key=lambda x: x[1], reverse=True)

    print('Movies suggested for you:\n')
    for i, movie in enumerate(sorted_similar_movies, 1):
        index = movie[0]
        title_from_index = data[data.index == index]['title'].values[0]
        if i < 12 and i != 1:
            print(i - 1, '.', title_from_index)
    
    # Saving data and similarity matrix to pickle files
    pickle.dump(data, open('data.pk1', 'wb'))
    pickle.dump(similarity, open('similarity.pk1', 'wb'))
    # Loading similarity matrix from pickle file
    loaded_similarity = pickle.load(open('similarity.pk1', 'rb'), encoding='latin1')
    print('Loaded Similarity Matrix:', loaded_similarity)

find_similar("Avengers age of ultron")
