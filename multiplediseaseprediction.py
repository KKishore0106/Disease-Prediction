import streamlit as st
import requests
import streamlit.components.v1 as components

# 🔹 GitHub Pages or jsDelivr Raw File URLs
HTML_URL = "https://KKishore0106.github.io/Disease-Prediction/index.html"  # Update if using GitHub Pages
# HTML_URL = "https://cdn.jsdelivr.net/gh/KKishore0106/Disease-Prediction/index.html"  # Alternative jsDelivr link

def fetch_github_file(url):
    """Fetch file content from GitHub-hosted HTML"""
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "<p style='color: red;'>Error loading the chat interface. Check the GitHub URL.</p>"

# 🔹 Load the ChatGPT-style UI from GitHub
chat_ui = fetch_github_file(HTML_URL)

# 🔹 Set Streamlit Page Configuration
st.set_page_config(page_title="ChatGPT Health Assistant", page_icon="💬")

st.title("🩺 AI Health Chatbot")
st.write("Interact with the chatbot and get health insights.")

# 🔹 Embed the ChatGPT UI inside Streamlit
components.html(chat_ui, height=700, scrolling=True)
