
import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os # Import os

# Get credentials from environment variables/secrets
CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID") 
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")

# Fallback for local testing (optional, but helpful)
# CLIENT_ID = st.secrets.get("SPOTIPY_CLIENT_ID")
# CLIENT_SECRET = st.secrets.get("SPOTIPY_CLIENT_SECRET")

# Check if keys are loaded
if not CLIENT_ID or not CLIENT_SECRET:
    st.error("Spotify credentials (SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET) not found in environment variables.")
else:
    # Initialize the Spotify client
    client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

   

def get_song_album_cover_url(song_name, artist_name):
    # Search for the track
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track", limit=1)

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        
        # Get album cover
        album_cover_url = "https://i.postimg.cc/0QNxYz4V/social.png" # Default
        if track["album"]["images"]:
            album_cover_url = track["album"]["images"][0]["url"]
            
        # Get Spotify track URL
        spotify_url = track["external_urls"]["spotify"]
        
        # Return both
        return album_cover_url, spotify_url
    else:
        # Return defaults if not found
        return "https://i.postimg.cc/0QNxYz4V/social.png", None

def recommend(song):
    try:
        index = music[music['song'] == song].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        recommended_music_names = []
        recommended_music_posters = []
        recommended_music_urls = []  # New list for Spotify URLs
        
        for i in distances[1:6]:
            artist = music.iloc[i[0]].artist
            song_title = music.iloc[i[0]].song
            
            # Get both poster and track URL
            poster, url = get_song_album_cover_url(song_title, artist)
            
            recommended_music_names.append(song_title)
            recommended_music_posters.append(poster)
            recommended_music_urls.append(url) # Add URL to the list
            
        # Return all three lists
        return recommended_music_names, recommended_music_posters, recommended_music_urls
    
    except IndexError:
        st.error(f"The song '{song}' is not in our dataset. Please try another song.")
        return [], [], []

st.header('Music Recommender System')
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

music_list = music['song'].values
selected_song = st.selectbox(  # Changed variable name for clarity
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    # Unpack all three lists
    recommended_music_names, recommended_music_posters, recommended_music_urls = recommend(selected_song)
    
    if recommended_music_names: # Check if recommendations were found
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Helper function to display
        def display_recommendation(col, name, poster, url):
            with col:
                if url:
                    # Display song name as a clickable link
                    st.markdown(f"[{name}]({url})")
                    # Display image as a clickable link (using HTML in markdown)
                    st.markdown(f"<a href='{url}' target='_blank'><img src='{poster}' style='width:100%'></a>", unsafe_allow_html=True)
                else:
                    # Fallback if no URL was found
                    st.text(name)
                    st.image(poster)

        # Display all 5 recommendations
        display_recommendation(col1, recommended_music_names[0], recommended_music_posters[0], recommended_music_urls[0])
        display_recommendation(col2, recommended_music_names[1], recommended_music_posters[1], recommended_music_urls[1])
        display_recommendation(col3, recommended_music_names[2], recommended_music_posters[2], recommended_music_urls[2])
        display_recommendation(col4, recommended_music_names[3], recommended_music_posters[3], recommended_music_urls[3])
        display_recommendation(col5, recommended_music_names[4], recommended_music_posters[4], recommended_music_urls[4])