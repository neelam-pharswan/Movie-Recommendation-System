import streamlit as st
import pandas as pd
import requests
import base64

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("bg image.webp")

st.markdown(f"""
<style>
.stApp {{
    background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.75)),
                      url("data:image/webp;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}}

h1 {{
    color: #ffffff;
    text-align: center;
    font-size: 55px;
    font-weight: 900;
}}

p {{
    font-size: 22px;
    color: #f5f5f5;
}}

label {{
    font-size: 21px !important;
    font-weight: 700;
    color: #ffffff !important;
}}

div[data-baseweb="select"] {{
    background-color: #ffffff;
    border-radius: 14px;
    padding: 7px;
    font-size: 18px;
}}

.stButton > button {{
    background: linear-gradient(to right, #8B0000, #C71585);
    color: white;
    border-radius: 16px;
    height: 60px;
    width: 100%;
    font-size: 23px;
    font-weight: bold;
    border: none;
}}

.stButton > button:hover {{
    background: linear-gradient(to right, #a30000, #ff1493);
    color: white;
    transform: scale(1.04);
}}

[data-testid="column"]:first-child {{
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(14px);
    border-radius: 22px;
    padding: 25px;
    border: 1px solid rgba(255,255,255,0.25);
}}

h2, h3 {{
    font-size: 34px;
    color: #ffffff;
    text-align: center;
}}

img {{
    border-radius: 16px;
    margin-bottom: 10px;
    transition: transform 0.3s ease;
}}

img:hover {{
    transform: scale(1.08);
}}

strong {{
    font-size: 19px;
    color: white;
}}

.rating {{
    font-size: 17px;
    font-weight: 700;
    color: #ffd700;
    margin-top: -5px;
    margin-bottom: 5px;
}}

[data-testid="stCaptionContainer"] {{
    font-size: 16px;
    color: #eeeeee;
}}

.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}}
</style>
""", unsafe_allow_html=True)

movies = pd.read_pickle("movies.pkl")
movie_similarity = pd.read_pickle("movie_similarity.pkl")

api_key = st.secrets["TMDB_API_KEY"]

def clean_title(title):
    return title.rsplit("(", 1)[0].strip()

@st.cache_data
def fetch_movie_details(movie_title):
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": api_key,
        "query": clean_title(movie_title)
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["results"]:
        movie_data = data["results"][0]
        poster_path = movie_data.get("poster_path")
        rating = movie_data.get("vote_average")

        poster_url = None

        if poster_path:
            poster_url = "https://image.tmdb.org/t/p/w500" + poster_path

        return poster_url, rating

    return None, None

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
                poster, rating = fetch_movie_details(row['title'])

                with cols[i % 5]:
                    if poster:
                        st.image(poster, use_container_width=True)
                    else:
                        st.write("🎬")

                    st.markdown(f"**{row['title']}**")

                    if rating:
                        st.markdown(f"<div class='rating'>⭐ {rating:.1f}/10</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='rating'>⭐ N/A</div>", unsafe_allow_html=True)

                    st.caption(row['genres'])