# 🎬 Movie Recommendation System

A professional **Movie Recommendation System** built using **Collaborative Filtering** on the MovieLens dataset. The project recommends movies based on user rating similarity and enhances the user experience with a Streamlit web interface and TMDB API integration for real-time movie posters and ratings.

---

## 🚀 Live Demo

Add your deployed Streamlit link here:

```text
https://movie-recommendation-system-hza5xncdxnpyleyfgiqsnv.streamlit.app/
```

---

## 📌 Project Overview

This project recommends similar movies based on user's historical rating patterns. It uses a **movie-to-movie collaborative filtering approach**, where movies are compared based on how users rated them.

The system also integrates the **TMDB API** to fetch real-time movie posters and ratings, making the application more interactive and visually appealing.

---

## ✨ Features

- Movie recommendation based on user rating similarity
- Genre-based movie filtering
- Movie selection through dropdown menus
- Real-time movie posters using TMDB API
- TMDB movie ratings displayed with recommendations
- Streamlit-based interactive web interface
- Cached API calls for better performance
- Deployed as a live web application

---

## 🧠 Recommendation Approach

The system uses **Collaborative Filtering**, which recommends movies by analyzing user rating behavior.

### Workflow

1. Load MovieLens datasets: `movies.dat`, `ratings.dat`, and `users.dat`.
2. Create a user-movie rating matrix.
3. Convert it into a movie-user matrix.
4. Filter movies with sufficient ratings to improve recommendation quality.
5. Calculate movie similarity using correlation.
6. Recommend movies similar to the selected movie.
7. Fetch posters and ratings from TMDB API.

---

## 🛠️ Tech Stack

**Programming Language:** Python

**Libraries:** Pandas, NumPy, Requests

**Recommendation Technique:** Collaborative Filtering, Correlation-based Similarity

**Web Framework:** Streamlit

**API Integration:** TMDB API

**Tools & Platforms:** Google Colab, Git & GitHub, Streamlit Cloud

---

## 📂 Project Structure

```text
Movie-Recommender/
│
├── app.py
├── movies.pkl
├── movie_similarity.pkl
├── requirements.txt
├── README.md
│
└── .streamlit/
    └── secrets.toml
```

---

## 📊 Dataset

The project uses the **MovieLens dataset**, which contains movie details, user ratings, and user information.

Main files used:

```text
movies.dat
ratings.dat
users.dat
```

The ratings data is used to build the recommendation engine, while the movie data is used to display movie titles and genres.

---

## 🔐 TMDB API Setup

This project uses TMDB API to fetch movie posters and ratings.

Create a `.streamlit/secrets.toml` file:

```toml
TMDB_API_KEY = "your_tmdb_api_key_here"
```

In Streamlit Cloud, add the same key under:

```text
App Settings → Secrets
```

---

## ▶️ How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/movie-recommendation-system.git
```

### 2. Move into the project folder

```bash
cd movie-recommendation-system
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit app

```bash
streamlit run app.py
```

If Streamlit command is not recognized, use:

```bash
python -m streamlit run app.py
```

---

## 📦 Requirements

Add these to `requirements.txt`:

```text
streamlit
pandas
numpy
requests
```

---

## 🖥️ Web App Interface

The app allows users to:

1. Select a movie genre.
2. Choose a movie from that genre.
3. Click the recommend button.
4. View similar movie recommendations with posters, ratings, and genres.

---

## 📈 Results

The recommendation system successfully generates movie recommendations based on similarity in user rating patterns. TMDB API integration improves the visual quality of the app by adding posters and real-time ratings.

---

## 💡 Key Learning Outcomes

Through this project, I learned:

- How collaborative filtering works
- How to create a user-movie matrix
- How to calculate movie similarity
- How to optimize recommendations by filtering popular movies
- How to integrate external APIs into ML projects
- How to build and deploy an interactive Streamlit web app

---

## 🚀 Future Improvements

- Add trending movies using TMDB API
- Add movie overview 
- Build a hybrid recommendation system
- Add user-based recommendation
- Add search functionality for all TMDB movies
- Improve UI with advanced movie cards

---

## 👩‍💻 Author

**Neelam Pharswan**  
Data Science Student  

GitHub: https://github.com/neelam-pharswan
---

## ⭐ Project Summary

This project combines **machine learning, data processing, API integration, and web deployment** to create a complete end-to-end movie recommendation system.
