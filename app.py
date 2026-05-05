import streamlit as st
import pandas as pd
import requests

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #C71585;
    color: white;
}

/* Title */
h1 {
    color: #8B0000;
    text-align: center;
    font-size: 42px;
    font-weight: 800;
}

/* Text */
p, label {
    color: white;
    font-size: 16px;
}

/* Selectbox */
div[data-baseweb="select"] {
    background-color: white;
    border-radius: 10px;
}

/* Button */
.stButton > button {
    background-color: #8B0000;
    color: white;
    border-radius: 12px;
    height: 45px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    background-color: #a30000;
}

/* Subheaders */
h2, h3 {
    color: white;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
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

# ---------------- GENRES ----------------
all_genres = set()
for g in movies['genres']:
    for genre in g.split('|'):
        all_genres.add(genre)

genre_list = sorted(list(all_genres))

# ---------------- UI ----------------
st.title("🎬 Movie Recommendation System")

# Create two columns
left, right = st.columns([1, 2])

with left:
    st.write("Select a genre, choose a movie, and get recommendations.")

    selected_genre = st.selectbox("Choose a genre:", genre_list)

    recommendable_ids = movie_similarity.columns

    filtered_movies = movies[
        (movies['genres'].str.contains(selected_genre, na=False)) &
        (movies['movieId'].isin(recommendable_ids))
    ]

    movie_list = filtered_movies['title'].sort_values().values
    movie_name = st.selectbox("Choose a movie:", movie_list)

    recommend_clicked = st.button("Recommend")

# ---------------- RECOMMEND FUNCTION ----------------
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

# ---------------- DISPLAY ----------------
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
                        st.image(poster)
                    else:
                        st.write("🎬")

                    st.markdown(f"**{row['title']}**")
                    st.caption(row['genres'])