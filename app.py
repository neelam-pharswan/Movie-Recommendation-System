import streamlit as st
import pandas as pd
import requests

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #C71585, #8B0000, #2b2b2b);
    color: white;
}

h1 {
    color: #ffffff;
    text-align: center;
    font-size: 50px;
    font-weight: 900;
}

p {
    font-size: 20px;
    color: #f5f5f5;
}

label {
    font-size: 20px !important;
    font-weight: 700;
    color: #ffffff !important;
}

div[data-baseweb="select"] {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 6px;
    font-size: 18px;
}

.stButton > button {
    background: linear-gradient(to right, #8B0000, #C71585);
    color: white;
    border-radius: 14px;
    height: 58px;
    width: 100%;
    font-size: 22px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background: linear-gradient(to right, #a30000, #ff1493);
    color: white;
}

h2, h3 {
    font-size: 30px;
    color: #ffffff;
    text-align: center;
}

img {
    border-radius: 14px;
    margin-bottom: 10px;
}

strong {
    font-size: 18px;
}

[data-testid="stCaptionContainer"] {
    font-size: 15px;
    color: #eeeeee;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}
</style>
""", unsafe_allow_html=True)

movies = pd.read_pickle("movies.pkl")
movie_similarity = pd.read_pickle("movie_similarity.pkl")

api_key = st.secrets["TMDB_API_KEY"]

def clean_title(title):
    return title.rsplit("(", 1)[0].strip()

@st.cache_data
def fetch_poster(movie_title):
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": api_key,
        "query": clean_title(movie_title)
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["results"]:
        poster_path = data["results"][0].get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    return None

all_genres = set()

for g in movies['genres']:
    for genre in g.split('|'):
        all_genres.add(genre)

genre_list = sorted(list(all_genres))

st.title("🎬 Movie Recommendation System")

left, right = st.columns([1, 2])

with left:
    st.write("Select a genre, choose a movie, and get similar recommendations.")

    selected_genre = st.selectbox("Choose a genre:", genre_list)

    recommendable_ids = movie_similarity.columns

    filtered_movies = movies[
        (movies['genres'].str.contains(selected_genre, na=False)) &
        (movies['movieId'].isin(recommendable_ids))
    ]

    movie_list = filtered_movies['title'].sort_values().values

    movie_name = st.selectbox("Choose a movie:", movie_list)

    recommend_clicked = st.button("Recommend")

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

with right:
    if recommend_clicked:
        result = recommend(movie_name)

        if isinstance(result, str):
            st.warning(result)
        else:
            st.subheader("Recommended Movies")

            cols = st.columns(5)

            for i, row in result.head(10).iterrows():
                poster = fetch_poster(row['title'])

                with cols[i % 5]:
                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.write("🎬")

                    st.markdown(f"**{row['title']}**")
                    st.caption(row['genres'])