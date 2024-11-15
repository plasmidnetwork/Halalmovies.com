import streamlit as st
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"

# Initialize the client
client = OpenAI(api_key=OPENAI_API_KEY)

def search_movie(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    return response.json()

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "append_to_response": "release_dates,keywords"
    }
    response = requests.get(url, params=params)
    details = response.json()
    
    ratings_url = f"{BASE_URL}/movie/{movie_id}/release_dates"
    ratings_response = requests.get(ratings_url, params={"api_key": TMDB_API_KEY})
    ratings_data = ratings_response.json()
    
    keywords_url = f"{BASE_URL}/movie/{movie_id}/keywords"
    keywords_response = requests.get(keywords_url, params={"api_key": TMDB_API_KEY})
    keywords_data = keywords_response.json()
    
    return details, ratings_data, keywords_data

def analyze_content(keywords_data, ratings_data):
    keywords = [keyword['name'].lower() for keyword in keywords_data.get('keywords', [])]
    
    content_indicators = {
        "Sexual Content": ["nudity", "sex scene", "sexual content", "erotic", "romance", "kissing"],
        "Violence": ["graphic violence", "gore", "bloody", "fighting", "combat"],
        "Language": ["profanity", "strong language", "explicit language"],
        "Substance Use": ["drug use", "substance abuse", "alcoholism", "smoking"]
    }
    
    warnings = {category: "No" for category in content_indicators}
    for category, indicators in content_indicators.items():
        if any(word in keywords for word in indicators):
            warnings[category] = "Yes"
    
    rating = "Not rated"
    rating_description = ""
    for country in ratings_data.get('results', []):
        if country.get('iso_3166_1') == 'US':
            for release in country.get('release_dates', []):
                if release.get('certification'):
                    rating = release.get('certification')
                    rating_descriptions = {
                        'G': 'General Audience - Suitable for all ages',
                        'PG': 'Parental Guidance Suggested',
                        'PG-13': 'Parents Strongly Cautioned',
                        'R': 'Restricted - Under 17 requires accompanying adult',
                        'NC-17': 'Adults Only - No one 17 and under admitted'
                    }
                    rating_description = rating_descriptions.get(rating, '')
                    break
    
    return warnings, rating, rating_description, keywords

def get_ai_content_analysis(movie_title, overview):
    if not OPENAI_API_KEY:
        st.error("OpenAI API key not found in environment variables")
        return None
    
    prompt = f"""
For the movie "{movie_title}", please analyze the following content:
Movie overview: {overview}

Please analyze the file for scenes containing any sexual content including kissing, nudity, and sexual acts or effection.

If you find a scene containing at least one of the above elements, provide a complete detail of the scene:

Scene [number]:
- 📝 **Description**: [Provide a description of the scene]
- 👥 **Characters**: [Names of characters involved]
- ℹ️ **Implies Intimacy or Sexual Act**: [If the scene includes sexual effection then simply answer Yes / Otherwise just answer Unknown]
- 🔞 **Nudity**: Male / Female / Both
- 💋 **Kissing**: Yes / No
- 👁 **Buttocks**: Yes / No
- 👁 **Breasts or Nipples**: Yes / No
- 👁 **Vagina**: Yes / No
- 👁 **Penis**: Yes / No
- 🔊 **Moaning**: Yes / if No, then Unknown
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a movie scenes analyzer providing thorough and insightful scene analysis. Be specific and detailed, no opinions, just observations where relevant to enhance understanding. Highlight any content that make parents watching with children uncomfortable."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        if response.choices:
            return response.choices[0].message.content
        else:
            st.error("No response generated")
            return None
            
    except Exception as e:
        st.error(f"Error calling OpenAI API: {str(e)}")
        return None

# Page configuration
st.set_page_config(
    page_title="HalalMovies.com",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="auto"
)

st.markdown("""
    <h1 style='text-align: center; color: #2E7D32;'>Halal Movies 🎬</h1>
    """, unsafe_allow_html=True)

st.markdown("""
    <p style='text-align: center;'>Detailed movie content analysis for informed viewing decisions</p>
    """, unsafe_allow_html=True)

# Add disclaimer box
st.warning("""
    ⚠️ **IMPORTANT PARENTAL DISCLAIMER**
    
    Please be aware that:
    - This app is still in development and may contain inaccuracies
    - AI analysis may sometimes "hallucinate" or generate incorrect information
    - The content analysis should not be considered as a definitive guide
    - Parents should independently verify movie content before making viewing decisions
    - Always use trusted parental guidance resources alongside this tool
    
    Your discretion and additional research are strongly recommended.
""")

# Add this function before your text_input
def handle_enter():
    if st.session_state.movie_input:
        st.session_state.analyze = True

# Replace your current text_input and button with this:
movie_name = st.text_input(
    "Enter movie title",
    placeholder="Example: The Lion King",
    key="movie_input",
    on_change=handle_enter
)

if st.button("Analyze 🔍", type="primary", use_container_width=True) or st.session_state.get('analyze', False):
    # Reset the analyze flag
    st.session_state.analyze = False
    
    if movie_name:
        with st.spinner("Analyzing..."):
            results = search_movie(movie_name)
            
            if results.get("results"):
                movie = results["results"][0]
                details, ratings_data, keywords_data = get_movie_details(movie["id"])
                warnings, rating, rating_description, keywords = analyze_content(keywords_data, ratings_data)
                
                # Display movie info
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if movie.get("poster_path"):
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                        st.image(poster_url, width=200)
                
                with col2:
                    st.subheader(movie["title"])
                    st.write(f"Release Date: {movie.get('release_date', 'N/A')}")
                    st.write(f"Overview: {movie.get('overview', 'No overview available')}")
                
                # Display US Rating
                st.write(f"🏷️ US Rating: {rating}")
                if rating_description:
                    st.caption(rating_description)
                
                # Display keywords
                st.subheader("🏷️ Content Keywords")
                st.write(", ".join(keywords[:10]) if keywords else "No keywords available")
                
                # Display AI Analysis
                st.subheader("🔍 Detailed Scene Analysis")
                with st.spinner("Generating detailed scene analysis..."):
                    ai_analysis = get_ai_content_analysis(
                        movie["title"],
                        movie.get("overview", "")
                    )
                    
                    if ai_analysis:
                        with st.expander("📝 Scene-by-Scene Content Analysis", expanded=True):
                            st.markdown(ai_analysis)
                    else:
                        st.error("Unable to generate detailed analysis. Please try again.")
                
                # Remove the Final Recommendation section and go straight to the footer
                st.caption("Note: This analysis is automated and should be used as a guide only. Always verify with trusted sources.")
                
                # Add some spacing
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown("---")  # Horizontal line

                # Create footer columns with better proportions
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown("""
                        <div style='font-size: 0.8em; color: #666666; padding-top: 20px;'>
                        This product uses the TMDB API but is not endorsed or certified by TMDB.
                        </div>
                        """, unsafe_allow_html=True)

                with col2:
                    try:
                        st.image("assets/tmdb_logo.svg", width=80)
                    except Exception as e:
                        st.error(f"Could not load TMDB logo: {str(e)}")
                
            else:
                st.error("Movie not found. Please check the spelling and try again.")
    else:
        st.warning("Please enter a movie or show name")
