import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY") # from .env file get API key
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("My First Gemini Chatbot")

# Stop app if API key missing
if not api_key:
    st.error("GEMINI_API_KEY not found. Check your .env file.")
    st.stop()

# Create Gemini client 
client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-2.5-flash-lite"

# Session memory  rerun the page
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_input
        )
        reply = response.text
    except Exception as e:
        reply = f"Error from Gemini: {e}"

    # Show assistant message immediately 
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
