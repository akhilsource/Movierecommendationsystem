import time
import streamlit as st
import pickle
import difflib
import os
import requests
st.header("Movie recommendation system")
movies = pickle.load(open('data.pk1', 'rb'))
similarity = pickle.load(open('similarity.pk1', 'rb'), encoding='latin1')
titles=movies['title'].values
def get_id(movie_name):
    id=movies[movies.title==movie_name]['id'].values[0]
    return id
def movie_poster(movie_name):
    key=os.environ.get("api_key")
    id=get_id(movie_name)
    url=("https://api.themoviedb.org/3/movie/{}?api_key="+key+'&language=en-US').format(id)
    data=requests.get(url)
    data=data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path
imageUrls = [
    movie_poster("Jurassic World"),
    movie_poster("Captain America: Civil War"),
    movie_poster("X-Men: The Last Stand"),
    movie_poster("Avengers: Age of Ultron"),
    movie_poster("Avatar"),
    movie_poster("Batman v Superman: Dawn of Justice"),
    movie_poster("Man of Steel"),
    movie_poster("Scooby-Doo"),
    movie_poster("Aliens"),
    movie_poster("The Conjuring 2"),
    movie_poster("The Devil's Own"),
    movie_poster("Nutty Professor II: The Klumps"),
    movie_poster("Iron Man 2")
    ]
#imageCarouselComponent=components.declare_component("image-carousel-component")
#imageCarouselComponent(imageUrls=imageUrls, height=200)
def recommend(movie):
    close_matches = difflib.get_close_matches(movie, titles)
    close_match = close_matches[0]
    index_movie = movies[movies.title == close_match]['index'].values[0]
    similarity_Score = list(enumerate(similarity[index_movie]))
    similarity_Score=sorted(similarity_Score, key=lambda x: x[1], reverse=True)
    f = []
    for i, movie in enumerate(similarity_Score[1:6],1):
        index = movie[0]
        d=[]
        title_from_index = movies[movies.index == index]['title'].values[0]
        path=movie_poster(title_from_index)
        d.append(title_from_index)
        d.append(path)
        f.append(d)       
    return f
name = st.selectbox("Select the movie to recommend", movies['title'].values)
if st.button("Show recommendations"):
    query = recommend(name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(query[0][0])
        st.image(query[0][1])
    with col2:
        st.text(query[1][0])
        st.image(query[1][1])
    with col3:
        st.text(query[2][0])
        st.image(query[2][1])
    with col4:
        st.text(query[3][0])
        st.image(query[3][1])
    with col5:
        st.text(query[4][0])
        st.image(query[4][1])
