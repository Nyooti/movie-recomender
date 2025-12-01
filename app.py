import streamlit as st
import requests
from typing import Dict

# TMDB API Configuration
TMDB_API_KEY = "d067a8687675d4ae5dd12c44661a3c41"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

# Genre mapping
GENRE_MAP = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Family": 10751,
    "Fantasy": 14,
    "History": 36,
    "Horror": 27,
    "Music": 10402,
    "Mystery": 9648,
    "Romance": 10749,
    "Sci-Fi": 878,
    "Thriller": 53,
    "War": 10752,
    "Western": 37
}

def fetch_movies(genre_id: int, page: int = 1) -> Dict:
    """Fetch movies from TMDB API by genre"""
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "vote_count.gte": 100,
        "page": page
    }
    response = requests.get(url, params=params)
    return response.json()

def search_movies(query: str, page: int = 1) -> Dict:
    """Search movies from TMDB API"""
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "page": page
    }
    response = requests.get(url, params=params)
    return response.json()

# Page config
st.set_page_config(
    page_title="NYTMovies - Discover Your Next Favorite Movie",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional look
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header styling */
    .hero-section {
        text-align: center;
        padding: 2rem 0 2rem 0;
        background: linear-gradient(180deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
    }
    

    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff 0%, #a8b3ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #a8b3ff;
        margin-bottom: 2rem;
    }
    
    /* Search section */
    .stSelectbox, .stTextInput {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        color: #fff;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        color: #fff;
        font-size: 1.1rem;
        padding: 0.75rem 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(255, 255, 255, 0.03);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stRadio > div > label {
        color: #a8b3ff;
        font-weight: 500;
    }
    
    /* Movie cards */
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 0;
        overflow: hidden;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        color: #a8b3ff;
        font-weight: 500;
    }
    
    /* Stats section */
    .stats-container {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 1rem;
        color: #a8b3ff;
        margin-top: 0.5rem;
    }
    
    /* Genre chips */
    .genre-chip {
        display: inline-block;
        background: rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        color: #a8b3ff;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        color: #a8b3ff;
    }
    
    .custom-footer a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
    }
    
    .custom-footer a:hover {
        text-decoration: underline;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #fff !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #a8b3ff;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🎬 NYTMovies</div>
    <div class="hero-subtitle">Discover Your Next Favorite Movie</div>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'movies' not in st.session_state:
    st.session_state.movies = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'total_results' not in st.session_state:
    st.session_state.total_results = 0

# Search Section
st.markdown("### 🔍 Find Movies")

col1, col2 = st.columns([2, 1])

with col1:
    search_type = st.radio("Search by:", ["Genre", "Keyword"], horizontal=True, label_visibility="collapsed")

with col2:
    st.write("")

# Search interface
if search_type == "Genre":
    col_select, col_button = st.columns([3, 1])
    
    with col_select:
        selected_genre = st.selectbox("Select a genre:", list(GENRE_MAP.keys()), label_visibility="collapsed")
    
    with col_button:
        search_clicked = st.button("🎬 Search", use_container_width=True)
    
    if search_clicked:
        with st.spinner("Finding amazing movies..."):
            st.session_state.current_page = 1
            genre_id = GENRE_MAP[selected_genre]
            data = fetch_movies(genre_id, st.session_state.current_page)
            st.session_state.movies = data.get('results', [])
            st.session_state.total_pages = data.get('total_pages', 0)
            st.session_state.total_results = data.get('total_results', 0)
            st.session_state.search_type = 'genre'
            st.session_state.genre_id = genre_id
            st.session_state.selected_genre = selected_genre

else:
    col_input, col_button = st.columns([3, 1])
    
    with col_input:
        search_query = st.text_input("Search for movies:", placeholder="e.g., Inception, Avatar, Matrix", label_visibility="collapsed")
    
    with col_button:
        search_clicked = st.button("🔍 Search", use_container_width=True)
    
    if search_clicked and search_query:
        with st.spinner("Searching movies..."):
            st.session_state.current_page = 1
            data = search_movies(search_query, st.session_state.current_page)
            st.session_state.movies = data.get('results', [])
            st.session_state.total_pages = data.get('total_pages', 0)
            st.session_state.total_results = data.get('total_results', 0)
            st.session_state.search_type = 'search'
            st.session_state.search_query = search_query

# Display movies
if st.session_state.movies:
    # Stats
    st.markdown("---")
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    
    with col_stat1:
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-number">{len(st.session_state.movies)}</div>
            <div class="stat-label">Movies Loaded</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-number">{st.session_state.total_results:,}</div>
            <div class="stat-label">Total Results</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stat3:
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-number">{st.session_state.current_page}</div>
            <div class="stat-label">Current Page</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎥 Results")
    
    # Display in grid
    cols = st.columns(4)
    
    for idx, movie in enumerate(st.session_state.movies):
        with cols[idx % 4]:
            # Movie poster
            poster_path = movie.get('poster_path')
            if poster_path:
                st.image(f"{TMDB_IMAGE_BASE}{poster_path}", use_container_width=True)
            else:
                st.markdown('<div style="background: rgba(102, 126, 234, 0.1); padding: 5rem; text-align: center; border-radius: 12px; font-size: 3rem;">🎬</div>', unsafe_allow_html=True)
            
            # Movie title
            st.markdown(f"**{movie.get('title', 'N/A')}**")
            
            # Movie metadata
            year = movie.get('release_date', '')[:4] if movie.get('release_date') else 'N/A'
            rating = movie.get('vote_average', 0)
            
            st.markdown(f"📅 {year} | ⭐ {rating:.1f}/10")
            
            # Overview expander
            with st.expander("📖 Read more"):
                overview = movie.get('overview', 'No description available.')
                st.write(overview)
    
    # Load more button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.current_page < min(st.session_state.total_pages, 3):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("⬇️ Load More Movies", use_container_width=True):
                with st.spinner("Loading more movies..."):
                    st.session_state.current_page += 1
                    
                    if st.session_state.search_type == 'genre':
                        data = fetch_movies(st.session_state.genre_id, st.session_state.current_page)
                    else:
                        data = search_movies(st.session_state.search_query, st.session_state.current_page)
                    
                    st.session_state.movies.extend(data.get('results', []))
                    st.rerun()
    else:
        st.info("🎬 You've reached the maximum number of results (60 movies)")

else:
    # Welcome message with features
    st.markdown("---")
    
    # Features section
    st.markdown("### ✨ Why Choose NYTMovies?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 2rem; border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.3); text-align: center; height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎬</div>
            <h3 style="color: #fff; margin-bottom: 1rem;">Vast Collection</h3>
            <p style="color: #a8b3ff;">Access thousands of movies from TMDB's extensive database with detailed information and ratings.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 2rem; border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.3); text-align: center; height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: #fff; margin-bottom: 1rem;">Smart Search</h3>
            <p style="color: #a8b3ff;">Find movies by genre, title, or keyword with our powerful search engine.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 2rem; border-radius: 16px; border: 1px solid rgba(102, 126, 234, 0.3); text-align: center; height: 100%;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⭐</div>
            <h3 style="color: #fff; margin-bottom: 1rem;">Ratings & Reviews</h3>
            <p style="color: #a8b3ff;">See ratings, release dates, and detailed descriptions for every movie.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Popular genres section
    st.markdown("### 🌟 Explore Popular Genres")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.02); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.05);">
        <span class="genre-chip">🎬 Action</span>
        <span class="genre-chip">😂 Comedy</span>
        <span class="genre-chip">🎭 Drama</span>
        <span class="genre-chip">👻 Horror</span>
        <span class="genre-chip">💕 Romance</span>
        <span class="genre-chip">🚀 Sci-Fi</span>
        <span class="genre-chip">🔪 Thriller</span>
        <span class="genre-chip">🎨 Animation</span>
        <span class="genre-chip">🗡️ Adventure</span>
        <span class="genre-chip">🕵️ Mystery</span>
        <span class="genre-chip">👨‍👩‍👧 Family</span>
        <span class="genre-chip">🎵 Music</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%); border-radius: 20px; border: 1px solid rgba(102, 126, 234, 0.3); margin: 2rem 0;">
        <h2 style="color: #fff; margin-bottom: 1rem; font-size: 2rem;">Ready to Find Your Next Favorite Movie?</h2>
        <p style="color: #a8b3ff; font-size: 1.2rem; margin-bottom: 0;">Select a genre above or search for a specific movie to get started!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats showcase
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.03); border-radius: 12px;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #667eea;">1M+</div>
            <div style="color: #a8b3ff; margin-top: 0.5rem;">Movies</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.03); border-radius: 12px;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #667eea;">17</div>
            <div style="color: #a8b3ff; margin-top: 0.5rem;">Genres</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.03); border-radius: 12px;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #667eea;">100%</div>
            <div style="color: #a8b3ff; margin-top: 0.5rem;">Free</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(255, 255, 255, 0.03); border-radius: 12px;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #667eea;">24/7</div>
            <div style="color: #a8b3ff; margin-top: 0.5rem;">Available</div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="custom-footer">
    <p>Movie data provided by <a href='https://www.themoviedb.org/' target='_blank'>The Movie Database (TMDB)</a></p>
    <p style="margin-top: 0.5rem; font-size: 0.9rem;">Designed and Developed by NYOOTI</p>
</div>
""", unsafe_allow_html=True)
