import streamlit as st
import requests
import streamlit.components.v1 as components

# GitHub raw file URLs
HTML_URL = "https://raw.githubusercontent.com/KKishore0106/Disease-Prediction/refs/heads/main/index.html"

def get_github_file(url):
    """Fetch file content from GitHub."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "<p style='color: red;'>Error loading the chat interface. Check the GitHub URL.</p>"

# Load HTML from GitHub
chat_html = get_github_file(HTML_URL)

# Streamlit Page Config
st.set_page_config(page_title="ChatGPT Health Assistant", page_icon="💬")
st.title("🩺 AI Health Chatbot")
st.write("Interact with the chatbot and get health insights.")

# Embed the GitHub-hosted chat UI inside Streamlit
components.html(chat_html, height=600, scrolling=True)
