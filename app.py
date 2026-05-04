import streamlit as st
import pandas as pd

st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
    color: white;
}

h1 {
    color: #ff4b4b;
    text-align: center;
    font-size: 42px;
    font-weight: 800;
}

p, label, .stMarkdown {
    color: white;
    font-size: 16px;
}

div[data-baseweb="select"] {
    background-color: white;
    border-radius: 10px;
}

.stButton > button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 12px;
    height: 45px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #ff6b6b;
    color: white;
    border: none;
}

[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 12px;
    padding: 10px;
}

h2, h3 {
    color: #ffd166;
    text-align: center;
}

.stAlert {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

movies = pd.read_pickle("movies.pkl")
movie_similarity = pd.read_pickle("movie_similarity.pkl")

all_genres = set()

for g in movies['genres']:
    for genre in g.split('|'):
        all_genres.add(genre)

genre_list = sorted(list(all_genres))

st.title("🎬 Movie Recommendation System")
st.write("Select a genre, choose a movie, and get similar recommendations.")

selected_genre = st.selectbox("Choose a genre:", genre_list)

recommendable_ids = movie_similarity.columns

filtered_movies = movies[
    (movies['genres'].str.contains(selected_genre, na=False)) &
    (movies['movieId'].isin(recommendable_ids))
]

movie_list = filtered_movies['title'].sort_values().values
movie_name = st.selectbox("Choose a movie:", movie_list)

def recommend(movie_name):
    movie = movies[movies['title'] == movie_name]

    if movie.empty:
        return "Movie not found"

    movie_id = movie.iloc[0]['movieId']

    if movie_id not in movie_similarity.columns:
        return "Movie not in filtered dataset"

    similar = movie_similarity[movie_id].sort_values(ascending=False)[1:11]

    result = similar.reset_index()
    result.columns = ['movieId', 'similarity']

    result = result.merge(movies, on='movieId')

    return result[['title', 'genres', 'similarity']]

if st.button("Recommend"):
    result = recommend(movie_name)

    if isinstance(result, str):
        st.warning(result)
    else:
        st.subheader("Recommended Movies")
        st.dataframe(result)