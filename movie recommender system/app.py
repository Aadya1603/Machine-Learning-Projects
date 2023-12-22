import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
import io


def recommend(movie):
    movie_index = movies[movies['title']== movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]
    recommended_movies = [(movies.iloc[i[0]].title, movies.iloc[i[0]]) for i in movies_list]
    return recommended_movies

def get_poster(movie_title):
    # Replace "YOUR_API_KEY" with your actual API key
    api_key = "c3245c0facb43baa08be0934a0e8b336"
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(url)
    data = response.json()
    if data["results"]:
        poster_path = data["results"][0]["poster_path"]
        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            response = requests.get(image_url)
            image = Image.open(io.BytesIO(response.content))
            return image
    return None

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System ')

selected_movie_name = st.selectbox(
    'How would you like to be connected ?',
    movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for title, genre in recommendations:
        poster = get_poster(title)
        if poster:
            st.image(poster)
        st.write(f"{title} ({genre})")


