import streamlit as st
import pickle
import pandas as pd
import requests

# API key
api_key = 'af55e1236e2f97678bc5089d2054b3b1'

# Function to fetch poster using movie_id
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    return 'https://image.tmdb.org/t/p/original' + data['poster_path']

# Load the movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movies_poster

# Streamlit App UI
st.title('🎥 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    st.subheader("Top 5 Recommendations for you:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
