import streamlit as st
import modal
import json
import os
import re

def main():
    #st.set_page_config(layout="wide")
    
    st.title("🎙️ Newsletter Dashboard")
    available_podcast_info = create_dict_from_json_files('.')

    # Left section - Input fields
    st.sidebar.header("Podcast RSS Feeds")

    # Dropdown box
    st.sidebar.subheader("Available Podcasts Feeds")
    selected_podcast = st.sidebar.selectbox("Select Podcast", options=available_podcast_info.keys())
    if selected_podcast:
        podcast_info = available_podcast_info[selected_podcast]
        display_podcast_info(podcast_info)
    
    # User Input box
    st.sidebar.subheader("Add and Process New Podcast Feed")
    url = st.sidebar.text_input("Link to RSS Feed")
    process_button = st.sidebar.button("Process Podcast Feed")
    st.sidebar.markdown("**Note**: Podcast processing can take upto 5 mins, please be patient.")
    
    if process_button:
        podcast_info = process_podcast_info(url)
        display_podcast_info(podcast_info)

def display_podcast_info(podcast_info):
    #st.header("Newsletter Content")
    st.divider()
    #st.subheader("Episode Title")
    #st.write("Episode Title")
    st.subheader("Podcast: "+podcast_info['podcast_details']['podcast_title'])
    st.subheader("Episode: "+podcast_info['podcast_details']['episode_title'])
    st.image(podcast_info['podcast_details']['episode_image'], caption="Podcast Cover", width=300, use_column_width=True)

    # Use regex to remove the guest details from the podcast_summary
    match = re.search(r'GUEST TITLE: .*?\n\n(.*)', podcast_info['podcast_summary'], flags=re.DOTALL)
    cleaned_summary = match.group(1) if match else podcast_info['podcast_summary']

    tab1, tab2, tab3 = st.tabs(["Summary", "Guest Details", "Key Moments"])

    with tab1:
        st.subheader("Podcast Episode Summary")
        st.write(cleaned_summary)  

    with tab2:
        # Display the podcast guest and their details in a side-by-side layout
        header_text = "Podcast Guest" if podcast_info['podcast_details']['episode_title'] != 'Host' else "Podcast Host"
        details_header_text = header_text + " Details"
        col3, col4 = st.columns([3, 7])
        with col3:
            st.subheader(header_text)
            st.write(podcast_info['podcast_guest']['name'])
        with col4:
            st.subheader(details_header_text)
            st.write(podcast_info["podcast_guest"]['summary'])
        # Check if "profile_picture" exists and seems like a URL
        profile_picture = podcast_info['podcast_guest'].get('profile_picture')
        if profile_picture and (profile_picture.startswith('http://') or profile_picture.startswith('https://')):
            st.image(profile_picture, caption=podcast_info['podcast_guest']['name'], width=300, use_column_width=True)

    with tab3:
        # Display the five key moments
        st.subheader("Key Moments, Insights, and Perspectives")
        key_moments = podcast_info['podcast_highlights']
        for moment in key_moments.split('\n'):
            st.markdown(f"<p style='margin-bottom: 5px;'>{moment}</p>", unsafe_allow_html=True)

def create_dict_from_json_files(folder_path):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]
    data_dict = {}
    for file_name in json_files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            podcast_info = json.load(file)
            podcast_name = podcast_info['podcast_details']['podcast_title']
            data_dict[podcast_name] = podcast_info
    return data_dict

def process_podcast_info(url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(url, '/content/podcast/')
    return output

if __name__ == '__main__':
    main()
