import streamlit as st
import pandas as pd
import requests

st.markdown("""
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #1a001a, #C71585, #2b2b2b);
    color: white;
}

/* Main container spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}

/* Title */
h1 {
    text-align: center;
    font-size: 52px;
    font-weight: 900;
    color: white;
}

/* Left panel glass effect */
[data-testid="column"]:first-child {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
}

/* Labels */
label {
    font-size: 18px !important;
    font-weight: 600;
}

/* Selectbox */
div[data-baseweb="select"] {
    background: white;
    border-radius: 12px;
}

/* Button */
.stButton > button {
    background: linear-gradient(to right, #8B0000, #C71585);
    color: white;
    border-radius: 14px;
    height: 55px;
    font-size: 20px;
    font-weight: bold;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.08);
    background: linear-gradient(to right, #ff004f, #ff1493);
}

/* Subheader */
h3 {
    text-align: center;
    font-size: 30px;
}

/* Poster images */
img {
    border-radius: 14px;
    transition: transform 0.3s ease;
}

/* Hover zoom effect */
img:hover {
    transform: scale(1.12);
}

/* Movie title */
strong {
    font-size: 17px;
}

/* Caption */
.stCaption {
    font-size: 14px;
    color: #e0e0e0;
}

</style>
""", unsafe_allow_html=True)
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