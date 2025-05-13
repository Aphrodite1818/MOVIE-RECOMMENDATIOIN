import streamlit as st 
import pandas as pd
import requests
import pickle as pkl

# importing files
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pkl.load(file)

# function to get top 10 similar movies
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices][['title', 'movie_id', 'overview']]

# function to fetch poster using TMDb API
def fetch_poster(movie_id):
    api_key = "f4f2a8053cd54d38429a968a3b49ecfe"
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/150?text=No+Image"

# Streamlit UI
st.title('🎬 Movie Recommendation System')

with st.form('movie_form'):
    st.write("This tool is not a streaming platform it is a recommendation system for movies 🍿")
    selected_movie = st.selectbox('Search movies 🔍', movies['title'].values)
    submit = st.form_submit_button('Recommend')

# Show recommendations if form was submitted
if submit:
    recommendation = get_recommendations(selected_movie)
    st.write("Top Recommended Movies For You:")

    for i in range(0, 10, 5):
        cols = st.columns(5)
        for col, j in zip(cols, range(i, i + 5)):
            if j < len(recommendation):
                movie_title = recommendation.iloc[j]['title']
                movie_id = recommendation.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    st.image(poster_url, width=130)
                    st.write(movie_title)

# 💼 Developer Credit (Footer)
st.markdown("""
<hr style="border:1px solid #ccc; margin-top:30px; margin-bottom:10px;">
<div style='text-align: center;'>
    <small>Designed & Developed by <b>Taiwo A</b>  | ⚙️ Powered by Streamlit</small>
</div>
""", unsafe_allow_html=True)
