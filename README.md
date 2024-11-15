# Halal Movies 🎬

A content analysis tool that helps users make informed decisions about movie content from an Islamic perspective.

  ⚠️ **IMPORTANT PARENTAL DISCLAIMER**
    
    Please be aware that:
    - This app is still in development and may contain inaccuracies
    - AI analysis may sometimes "hallucinate" or generate incorrect information
    - The content analysis should not be considered as a definitive guide
    - Parents should independently verify movie content before making viewing decisions
    - Always use trusted parental guidance resources alongside this tool
    
    Your discretion and additional research are strongly recommended.

## Description
Halal Movies is a Streamlit-based web application that provides detailed scene-by-scene analysis of movies, focusing on content that may be concerning from an Islamic viewpoint. The app combines data from TMDB (The Movie Database) with AI-powered content analysis to provide comprehensive insights about movie content.

## Features
- 🔍 Movie search functionality
- 📝 Detailed scene-by-scene content analysis
- 🏷️ US movie ratings and descriptions
- 🎯 Content keywords identification
- ⚠️ Specific content warnings for:
  - Intimate scenes
  - Inappropriate content
  - Suggestive behavior
  - Family-friendly assessment

## Technology Stack
- Python
- Streamlit
- OpenAI GPT-4
- TMDB API

## Requirements
- Python 3.6+
- OpenAI API key
- TMDB API key
- Required Python packages:
  - streamlit
  - requests
  - python-dotenv
  - openai

## Setup
1. Clone the repository
2. Create a `.env` file with your API keys:
   ```
   TMDB_API_KEY=your_tmdb_key
   OPENAI_API_KEY=your_openai_key
   ```
3. Install requirements:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   streamlit run app.py
   ```

## Usage
1. Enter a movie title in the search box
2. Click "Analyze" to get detailed content analysis
3. Review the comprehensive scene-by-scene breakdown
4. Check the final recommendation for viewing suitability

## Note
This tool is meant to be used as a guide only. Always verify content with trusted sources and use personal judgment when making viewing decisions.
