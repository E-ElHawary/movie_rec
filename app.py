import pandas as pd
import numpy as np
import streamlit as st
import pickle
import requests


with open('movie_rec.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)


def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices][['title', 'movie_id']]




def fetch_poster(movie_id):
    api_key = '45a64c70d089f22fb9af691fcbae2068'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    reponse = requests.get(url)
    data = reponse.json()
    poster_path = data['poster_path']
    full_path = f'https://image.tmdb.org/t/p/w500{poster_path}'
    return full_path

st.title("movie reccomendation system")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 recommended movies:")

    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    st.image(poster_url, width=130)
                    st.write(movie_title)
