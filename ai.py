import streamlit as st
import requests

# Replace with your TMDb API key
API_KEY = "your_tmdb_api_key"

def search_movie(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(url)
    data = response.json()
    return data['results']

def get_movie_link(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=external_ids"
    response = requests.get(url)
    data = response.json()
    homepage = data.get('homepage')
    return homepage or "No official link available"

# Streamlit UI
st.title("🎥 Movie Link Finder")
movie_title = st.text_input("Enter a movie name:")

if movie_title:
    results = search_movie(movie_title)
    if results:
        for movie in results[:3]:  # Show top 3 results
            st.subheader(movie['title'])
            st.write("Release Date:", movie.get('release_date', 'Unknown'))
            st.write("Overview:", movie.get('overview', 'No description available'))
            link = get_movie_link(movie['id'])
            st.markdown(f"[Official Link]({link})")
    else:
        st.warning("No movies found.")
