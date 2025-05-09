# Movie Recommendation System

## Overview
This is a **Movie Recommendation System** built using **collaborative filtering** and **cosine similarity**. The system suggests personalized movie recommendations to users based on their movie ratings and the ratings of similar users.

The project makes use of the **Movies Dataset**, **Ratings Dataset**, and **User Dataset** to predict which movies a user might enjoy based on the preferences of similar users.

## Features
- **Collaborative Filtering**: Recommends movies based on user similarity.
- **Cosine Similarity**: Measures the similarity between users.
- **RMSE Evaluation**: Evaluates the performance of the model using Root Mean Square Error (RMSE).

## Datasets
The following datasets are used in this project:
- `movies.dat`: Contains movie details (movieId, title, genres).
- `ratings.dat`: Contains user ratings for movies (userId, movieId, rating, timestamp).
- `users.dat`: Contains demographic information about users (userId, gender, age, occupation, zip).

The datasets are in `.dat` format and separated by `::` (double colons).

## Installation

### Prerequisites
Make sure you have **Python** and **Jupyter Notebook** installed.

### Clone the repository:
```bash
git clone https://github.com/your-username/Movie-Recommendation-System.git

