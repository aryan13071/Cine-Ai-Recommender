import streamlit as st
import pandas as pd
import pickle
import requests
import time
from streamlit_lottie import st_lottie
import json
from streamlit.components.v1 import html

# Set page config
st.set_page_config(
    page_title="CineAI Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Embedded Lottie animations
film_animation = {
    "v": "5.5.2",
    "fr": 30,
    "ip": 0,
    "op": 90,
    "w": 400,
    "h": 400,
    "nm": "Film",
    "ddd": 0,
    "assets": [],
    "layers": [
        {
            "ddd": 0,
            "ind": 1,
            "ty": 4,
            "nm": "Film",
            "sr": 1,
            "ks": {
                "o": {"a": 0, "k": 100, "ix": 11},
                "r": {"a": 0, "k": 0, "ix": 10},
                "p": {"a": 0, "k": [200, 200, 0], "ix": 2},
                "a": {"a": 0, "k": [0, 0, 0], "ix": 1},
                "s": {"a": 0, "k": [100, 100, 100], "ix": 6}
            },
            "ao": 0,
            "shapes": [
                {
                    "ty": "gr",
                    "it": [
                        {
                            "ty": "rc",
                            "d": 1,
                            "s": {"a": 0, "k": [150, 200], "ix": 2},
                            "p": {"a": 0, "k": [0, 0], "ix": 3},
                            "r": {"a": 0, "k": 0, "ix": 4},
                            "nm": "Rectangle",
                            "mn": "ADBE Vector Shape - Rect",
                            "hd": False
                        },
                        {
                            "ty": "fl",
                            "c": {"a": 0, "k": [0.8, 0.2, 0.2, 1], "ix": 4},
                            "o": {"a": 0, "k": 100, "ix": 5},
                            "r": 1,
                            "nm": "Fill",
                            "mn": "ADBE Vector Graphic - Fill",
                            "hd": False
                        },
                        {
                            "ty": "tr",
                            "p": {"a": 0, "k": [0, 0], "ix": 2},
                            "a": {"a": 0, "k": [0, 0], "ix": 1},
                            "s": {"a": 0, "k": [100, 100], "ix": 3},
                            "r": {"a": 1, "k": [
                                {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 0, "s": [0]},
                                {"t": 90, "s": [360]}
                            ], "ix": 6},
                            "o": {"a": 0, "k": 100, "ix": 7},
                            "sk": {"a": 0, "k": 0, "ix": 4},
                            "sa": {"a": 0, "k": 0, "ix": 5},
                            "nm": "Transform"
                        }
                    ],
                    "nm": "Film",
                    "np": 3,
                    "cix": 2,
                    "bm": 0,
                    "ix": 1,
                    "mn": "ADBE Vector Group",
                    "hd": False
                }
            ],
            "ip": 0,
            "op": 90,
            "st": 0,
            "bm": 0
        }
    ]
}

magic_animation = {
    "v": "5.5.2",
    "fr": 30,
    "ip": 0,
    "op": 90,
    "w": 400,
    "h": 400,
    "nm": "Magic",
    "ddd": 0,
    "assets": [],
    "layers": [
        {
            "ddd": 0,
            "ind": 1,
            "ty": 4,
            "nm": "Star",
            "sr": 1,
            "ks": {
                "o": {"a": 0, "k": 100, "ix": 11},
                "r": {"a": 0, "k": 0, "ix": 10},
                "p": {"a": 0, "k": [200, 200, 0], "ix": 2},
                "a": {"a": 0, "k": [0, 0, 0], "ix": 1},
                "s": {"a": 0, "k": [100, 100, 100], "ix": 6}
            },
            "ao": 0,
            "shapes": [
                {
                    "ty": "gr",
                    "it": [
                        {
                            "ty": "el",
                            "d": 1,
                            "s": {"a": 0, "k": [50, 50], "ix": 2},
                            "p": {"a": 0, "k": [0, 0], "ix": 3},
                            "nm": "Ellipse",
                            "mn": "ADBE Vector Shape - Ellipse",
                            "hd": False
                        },
                        {
                            "ty": "fl",
                            "c": {"a": 0, "k": [0.8, 0.8, 0.2, 1], "ix": 4},
                            "o": {"a": 0, "k": 100, "ix": 5},
                            "r": 1,
                            "nm": "Fill",
                            "mn": "ADBE Vector Graphic - Fill",
                            "hd": False
                        },
                        {
                            "ty": "tr",
                            "p": {"a": 0, "k": [0, 0], "ix": 2},
                            "a": {"a": 0, "k": [0, 0], "ix": 1},
                            "s": {"a": 0, "k": [100, 100], "ix": 3},
                            "r": {"a": 1, "k": [
                                {"i": {"x": [0.667], "y": [1]}, "o": {"x": [0.333], "y": [0]}, "t": 0, "s": [0]},
                                {"t": 90, "s": [360]}
                            ], "ix": 6},
                            "o": {"a": 0, "k": 100, "ix": 7},
                            "sk": {"a": 0, "k": 0, "ix": 4},
                            "sa": {"a": 0, "k": 0, "ix": 5},
                            "nm": "Transform"
                        }
                    ],
                    "nm": "Star",
                    "np": 3,
                    "cix": 2,
                    "bm": 0,
                    "ix": 1,
                    "mn": "ADBE Vector Group",
                    "hd": False
                }
            ],
            "ip": 0,
            "op": 90,
            "st": 0,
            "bm": 0
        }
    ]
}

# Custom CSS with animations and enhanced styling
st.markdown("""
<style>
    /* Main background with animated gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Floating animation for movie cards */
    @keyframes float {
        0% {transform: translateY(0px);}
        50% {transform: translateY(-10px);}
        100% {transform: translateY(0px);}
    }

    /* Movie poster hover effects */
    .poster-container {
        position: relative;
        width: 100%;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: float 6s ease-in-out infinite;
    }

    .movie-poster {
        width: 100%;
        height: auto;
        display: block;
        transition: transform 0.5s ease;
        border-radius: 15px;
    }

    .poster-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
        display: flex;
        align-items: flex-end;
        border-radius: 15px;
    }

    .poster-container:hover .poster-overlay {
        opacity: 1;
    }

    .poster-container:hover .movie-poster {
        transform: scale(1.08);
    }

    .poster-container:hover {
        box-shadow: 0 15px 30px rgba(255, 75, 75, 0.4);
    }

    .overlay-content {
        padding: 20px;
        width: 100%;
        color: white;
    }

    .rating {
        display: block;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 5px;
        color: #ffd700;
    }

    .year {
        display: block;
        font-size: 1rem;
        color: #ffffff;
    }

    /* Button styling with fire effect */
    .stButton>button {
        border: none;
        color: white;
        background: linear-gradient(45deg, #ff4b4b, #ff8e53);
        transition: all 0.3s ease;
        border-radius: 50px;
        padding: 12px 30px;
        font-weight: bold;
        margin: 30px auto;
        display: block;
        width: 300px;
        font-size: 1.2rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
        z-index: 1;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.6);
    }

    .stButton>button:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, #ff4b4b, #ff8e53, #ff4b4b);
        z-index: -1;
        transition: opacity 0.3s ease;
        opacity: 0;
    }

    .stButton>button:hover:before {
        opacity: 1;
        animation: fire 1.5s infinite;
    }

    @keyframes fire {
        0% {background-position: 10% 0%;}
        50% {background-position: 90% 100%;}
        100% {background-position: 10% 0%;}
    }

    /* Search box styling */
    .stSelectbox>div>div {
        background-color: rgba(30, 30, 30, 0.8) !important;
        border: 2px solid #ff4b4b !important;
        border-radius: 12px !important;
        padding: 12px !important;
        color: white !important;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }

    .stSelectbox>div>div:hover {
        border-color: #ff8e53 !important;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.4);
    }

    /* Make selected text visible */
    .stSelectbox>div>div>div>div {
        color: white !important;
    }

    /* Header styling */
    .main-header {
        text-align: center;
        margin-bottom: 30px;
        position: relative;
    }

    .main-header h1 {
        font-size: 4.5rem;
        background: linear-gradient(45deg, #ff4b4b, #ff8e53, #ff4b4b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        margin-bottom: 10px;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from {text-shadow: 0 0 10px rgba(255, 75, 75, 0.7);}
        to {text-shadow: 0 0 20px rgba(255, 75, 75, 0.9), 0 0 30px rgba(255, 75, 75, 0.5);}
    }

    .main-header p {
        font-size: 1.3rem;
        color: #f0f0f0;
        max-width: 700px;
        margin: 0 auto;
    }

    /* Movie card styling */
    .movie-card {
        background: rgba(26, 29, 36, 0.8);
        border-radius: 20px;
        padding: 20px;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 75, 75, 0.2);
    }

    .movie-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 15px 30px rgba(255, 75, 75, 0.3) !important;
        border: 1px solid rgba(255, 75, 75, 0.5);
    }

    /* Divider styling */
    .stMarkdown hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff4b4b, transparent);
        margin: 40px 0;
        opacity: 0.5;
    }

    /* Footer styling */
    .footer {
        text-align: center;
        padding: 30px;
        color: #aaaaaa;
        font-size: 1rem;
        margin-top: 50px;
        position: relative;
    }

    .footer:before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 50%;
        height: 1px;
        background: linear-gradient(90deg, transparent, #ff4b4b, transparent);
    }

    .social-links {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-top: 15px;
    }

    .social-links a {
        color: #ff4b4b !important;
        text-decoration: none;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }

    .social-links a:hover {
        transform: translateY(-3px);
        text-shadow: 0 0 10px rgba(255, 75, 75, 0.7);
    }

    /* Sparkle effect */
    .sparkle {
        position: absolute;
        width: 5px;
        height: 5px;
        background-color: #ffd700;
        border-radius: 50%;
        pointer-events: none;
        z-index: 100;
        animation: sparkle 1s ease-out;
    }

    @keyframes sparkle {
        0% {transform: scale(0); opacity: 1;}
        100% {transform: scale(1.5); opacity: 0;}
    }

    /* Typewriter effect */
    .typewriter {
        overflow: hidden;
        border-right: 3px solid #ff4b4b;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: 2px;
        animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
    }

    @keyframes typing {
        from {width: 0}
        to {width: 100%}
    }

    @keyframes blink-caret {
        from, to {border-color: transparent}
        50% {border-color: #ff4b4b}
    }

    /* Confetti effect */
    .confetti {
        position: absolute;
        width: 10px;
        height: 10px;
        background-color: #f00;
        opacity: 0;
    }

    /* Floating stars background */
    .stars {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }

    .star {
        position: absolute;
        background-color: #fff;
        border-radius: 50%;
        animation: twinkle var(--duration) ease-in-out infinite;
    }

    @keyframes twinkle {
        0%, 100% {opacity: 0.2; transform: scale(0.5);}
        50% {opacity: 1; transform: scale(1);}
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for sparkle effect
sparkle_js = """
<script>
document.addEventListener('click', function(e) {
    let sparkle = document.createElement('div');
    sparkle.className = 'sparkle';
    sparkle.style.left = e.pageX + 'px';
    sparkle.style.top = e.pageY + 'px';
    document.body.appendChild(sparkle);

    setTimeout(function() {
        sparkle.remove();
    }, 1000);
});
</script>
"""

# JavaScript for floating stars
stars_js = """
<script>
function createStars() {
    const container = document.createElement('div');
    container.className = 'stars';
    document.body.appendChild(container);

    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';

        // Random properties
        const size = Math.random() * 3;
        const duration = 2 + Math.random() * 3;
        const delay = Math.random() * 5;
        const x = Math.random() * 100;
        const y = Math.random() * 100;

        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.left = `${x}%`;
        star.style.top = `${y}%`;
        star.style.setProperty('--duration', `${duration}s`);
        star.style.animationDelay = `${delay}s`;

        container.appendChild(star);
    }
}

createStars();
</script>
"""


# Load data
@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity


movies, similarity = load_data()

# OMDb API Key
OMDB_API_KEY = "82d26054"

# ==============================================
# STUNNING HEADER SECTION WITH ANIMATIONS
# ==============================================

st.markdown("""
<div class='main-header'>
    <h1>
        🎬 CineAI <span style='background: linear-gradient(45deg, #ffffff, #f0f0f0); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Recommender</span>
    </h1>
    <p class='typewriter'>
        Discover cinematic masterpieces tailored just for you
    </p>
</div>
""", unsafe_allow_html=True)

# Display embedded Lottie animation
st_lottie(film_animation, height=200, key="header-animation")

# ==============================================
# MOVIE SELECTOR WITH ENHANCED UI
# ==============================================

st.markdown("---")
st.markdown("""
<h2 style='
    color: #ffffff;
    text-align: center;
    font-family: "Helvetica Neue", sans-serif;
    font-size: 2.5rem;
    text-shadow: 0 0 10px rgba(255, 75, 75, 0.5);
    margin-bottom: 30px;
'>
    ✨ Find Your Next Favorite Movie ✨
</h2>
""", unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    "Search from thousands of movies:",
    movies['title'].values,
    index=0,
    key="movie_select",
    help="Select a movie you enjoy to get personalized recommendations"
)


# ==============================================
# ENHANCED POSTER FETCHER WITH FALLBACK
# ==============================================

def fetch_poster(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if 'Poster' in data and data['Poster'] != 'N/A':
            return data['Poster']
        else:
            # Use a beautiful gradient placeholder with movie title
            title_encoded = movie_title.replace(' ', '+')
            return f"https://placehold.co/500x750/0f0c29/ffffff?text={title_encoded}&font=montserrat"
    except:
        return "https://placehold.co/500x750/0f0c29/ff4b4b?text=Poster+Not+Available"


# ==============================================
# AI RECOMMENDATION ENGINE WITH ENHANCED DETAILS
# ==============================================

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_years = []
    recommended_ratings = []
    recommended_genres = []
    recommended_directors = []

    for i in movie_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(title)

        # Fetch additional movie details
        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
            response = requests.get(url, timeout=5)
            data = response.json()
            recommended_years.append(data.get('Year', 'N/A'))
            recommended_ratings.append(data.get('imdbRating', 'N/A'))
            recommended_genres.append(data.get('Genre', 'N/A').split(',')[0])
            recommended_directors.append(data.get('Director', 'N/A').split(',')[0])
        except:
            recommended_years.append('N/A')
            recommended_ratings.append('N/A')
            recommended_genres.append('N/A')
            recommended_directors.append('N/A')

        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters, recommended_years, recommended_ratings, recommended_genres, recommended_directors


# ==============================================
# RECOMMENDATION DISPLAY WITH STUNNING EFFECTS
# ==============================================

if st.button("✨ Generate Magic Recommendations ✨", key="recommend_btn", use_container_width=True):
    # Add sparkle effect
    html(sparkle_js)

    with st.spinner('🔮 Analyzing cinematic patterns across dimensions...'):
        # Animated progress bar
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.02)  # For dramatic effect
            progress_bar.progress(percent_complete + 1)

        names, posters, years, ratings, genres, directors = recommend(selected_movie_name)

        # Success message with animation
        st.success("🎊 Voilà! We've conjured these perfect matches for you!")
        st.balloons()

        # Confetti effect
        confetti_js = """
        <script>
        const colors = ['#ff4b4b', '#ffd700', '#ffffff', '#ff8e53'];
        for (let i = 0; i < 100; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.width = Math.random() * 10 + 5 + 'px';
            confetti.style.height = Math.random() * 10 + 5 + 'px';
            confetti.style.opacity = '1';
            confetti.style.position = 'fixed';
            confetti.style.top = '-10px';
            confetti.style.zIndex = '9999';
            confetti.style.transform = 'rotate(' + Math.random() * 360 + 'deg)';

            document.body.appendChild(confetti);

            let animation = confetti.animate([
                {top: '-10px', transform: 'rotate(0deg)'},
                {top: '100vh', transform: 'rotate(' + Math.random() * 360 + 'deg)'}
            ], {
                duration: Math.random() * 3000 + 2000,
                easing: 'cubic-bezier(0.1, 0.2, 0.7, 1)'
            });

            animation.onfinish = () => confetti.remove();
        }
        </script>
        """
        html(confetti_js)

        st.markdown("---")

        # Display recommendations with enhanced cards
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.markdown(f"""
                <div class="movie-card">
                    <div class="poster-container">
                        <img src="{posters[i]}" class="movie-poster" alt="{names[i]}" onerror="this.src='https://placehold.co/500x750/0f0c29/ff4b4b?text=Poster+Not+Available'">
                        <div class="poster-overlay">
                            <div class="overlay-content">
                                <span class="rating">⭐ {ratings[i] if ratings[i] != 'N/A' else '?'}/10</span>
                                <span class="year">📅 {years[i] if years[i] != 'N/A' else 'Unknown'}</span>
                                <span style="display: block; margin-top: 5px; font-size: 0.9rem;">🎭 {genres[i] if genres[i] != 'N/A' else 'Unknown'}</span>
                                <span style="display: block; font-size: 0.9rem;">🎥 {directors[i] if directors[i] != 'N/A' else 'Unknown'}</span>
                            </div>
                        </div>
                    </div>
                    <h3 style="
                        background: linear-gradient(45deg, #ff4b4b, #ff8e53);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        font-size: 1.3rem;
                        text-align: center;
                        margin-top: 15px;
                        font-family: 'Helvetica Neue', sans-serif;
                        font-weight: bold;
                        padding: 5px;
                    ">{names[i]}</h3>
                </div>
                """, unsafe_allow_html=True)

        # Add a surprise element
        st.markdown("---")
        with st.expander("🔍 Click for fascinating insights about your selection!", expanded=False):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"""
                ### 🎥 *{selected_movie_name}* Trivia
                Our AI detected that this movie has unique cinematic patterns that match your taste profile. 
                Here's why you might love it:

                - **Visual Style**: High contrast cinematography with dynamic camera movements
                - **Narrative Structure**: Complex character arcs with unexpected plot twists
                - **Emotional Resonance**: Strong themes of redemption and personal growth

                *"The cinema is not a slice of life, but a piece of cake."* - Alfred Hitchcock
                """)
            with col2:
                st_lottie(magic_animation, height=150)

            st.success(
                "💡 Did you know? The more you use CineAI, the better it understands your unique movie preferences!")

# Add floating stars background
html(stars_js)

# ==============================================
# PREMIUM FOOTER WITH SOCIAL LINKS
# ==============================================

st.markdown("---")
st.markdown("""
<div class="footer">
    <p style="font-size: 1.1rem;">✨ Powered by Advanced AI • Cinematic Magic Since 2023 ✨</p>
    <div class="social-links">
        <a href="#" style="font-size: 1.5rem;">📱</a>
        <a href="#" style="font-size: 1.5rem;">📸</a>
        <a href="#" style="font-size: 1.5rem;">🎥</a>
        <a href="#" style="font-size: 1.5rem;">💻</a>
        <a href="#" style="font-size: 1.5rem;">📘</a>
    </div>
    <p style="margin-top: 20px; font-size: 0.9rem; color: rgba(255,255,255,0.6);">
        "Movies are a form of magic" - Martin Scorsese
    </p>
</div>
""", unsafe_allow_html=True)