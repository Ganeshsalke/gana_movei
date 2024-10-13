import pickle
import streamlit as st
import requests
import os

# Fetch poster from movie ID
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else None
        return full_path
    except Exception as e:
        st.error(f"Failed to fetch movie poster: {e}")
        return None

# Recommendation function
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return [], []

# Streamlit app styling and header
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.familynow.club/wp-content/uploads/2022/04/login-background.jpeg");
        background-size: cover;
        background-position: center;
        height: 100vh;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='color:#ff3333;'>MovieMate</h1>", unsafe_allow_html=True)

# File paths for the pickle files
movie_list_path = r'C:\Users\91721\Downloads\movie-recommender-system\movie-recommender-system-tmdb-dataset-main\movie_list.pkl'
similarity_path = r'C:\Users\91721\Downloads\movie-recommender-system\movie-recommender-system-tmdb-dataset-main\similarity.pkl'

# Check if the files exist before loading them
movies = None
similarity = None

if os.path.exists(movie_list_path) and os.path.exists(similarity_path):
    try:
        movies = pickle.load(open(movie_list_path, 'rb'))
        similarity = pickle.load(open(similarity_path, 'rb'))
    except Exception as e:
        st.error(f"Error loading data: {e}")
else:
    st.error("Required files not found. Please check the file paths.")

# Only proceed if data is loaded successfully
if movies is not None and similarity is not None:
    # Initialize watchlist if it doesn't exist
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []

    # Movie search bar
    search_term = st.text_input("Search for a movie:")
    if search_term:
        filtered_movies = movies[movies['title'].str.contains(search_term, case=False)]
        if not filtered_movies.empty:
            movie_list = filtered_movies['title'].values
        else:
            st.warning("No movies found. Please try another search.")
            movie_list = []
    else:
        movie_list = movies['title'].values

    # Dropdown for selecting a movie
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

    # Watchlist feature
    if st.button('Add to Watchlist'):
        if selected_movie not in st.session_state.watchlist:
            st.session_state.watchlist.append(selected_movie)
            st.success(f"{selected_movie} added to your watchlist!")
        else:
            st.warning(f"{selected_movie} is already in your watchlist.")

    # Display Watchlist
    st.subheader("Your Watchlist:")
    for movie in st.session_state.watchlist:
        st.text(movie)

    # Show recommended movies and posters when button is clicked
    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        if recommended_movie_names:
            cols = st.columns(5)
            for i, col in enumerate(cols):
                if i < len(recommended_movie_names):
                    with col:
                        st.text(recommended_movie_names[i])
                        st.image(recommended_movie_posters[i])
        else:
            st.warning("No recommendations available.")

    # User Ratings
    rating = st.slider("Rate this movie:", 1, 5, value=3)
    if st.button('Submit Rating'):
        st.success(f"You rated {selected_movie} a {rating}!")

# Footer
st.markdown("<footer style='text-align: center;'><p style='color: white;'>© 2024 Ganesh Salke | <a href='https://66a8f7716252b82abe966920--golden-gecko-48b2cf.netlify.app'>PortFolio</a></p></footer>", unsafe_allow_html=True)