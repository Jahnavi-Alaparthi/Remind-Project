import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta

# Load .env file and API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found. Check your .env file.")
    st.stop()

# Initialize Gemini client
client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-2.5-flash-lite"
DATA_FILE = "chat_history.json"

# --- Utility functions ---

def load_data():
    """Load chat history from JSON file. Returns a list."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(data):
    """Save chat history to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_interaction(query, response):
    """Save a single interaction with timestamp."""
    data = load_data()
    data.append({
        "query": query,
        "response": response,
        "time": datetime.now().isoformat(),
        "quized": False  # track if quiz was generated
    })
    save_data(data)

def get_due_quiz():
    """Return the first interaction older than 10 minutes that hasn't been quized."""
    now = datetime.now()
    data = load_data()
    for item in data:
        q_time = datetime.fromisoformat(item["time"])
        if now - q_time >= timedelta(minutes=10) and not item.get("quized", False):
            item["quized"] = True  # mark as quized
            save_data(data)
            return item
    return None

# --- Streamlit UI ---
st.title("Time-Based Quiz Bot")
st.caption("Your chat will be saved, and you'll get a quiz 10 minutes after each question!")

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display previous messages
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Display user message immediately
    st.session_state.chat.append({"role": "user", "content": user_input})
    
    # Send to Gemini and get reply
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[types.Content(role="user", parts=[types.Part(text=user_input)])]
        )
        reply = response.text
    except Exception as e:
        reply = f"Error from Gemini: {e}"

    # Display assistant reply immediately
    st.session_state.chat.append({"role": "assistant", "content": reply})

    # Save interaction
    save_interaction(user_input, reply)

# --- Check for quizzes ---
quiz_item = get_due_quiz()
if quiz_item:
    st.sidebar.header(" Quiz Time!")
    st.sidebar.markdown(f"**Based on:** {quiz_item['query']}")
    st.sidebar.markdown("Try to answer the question below!")

    user_answer = st.sidebar.text_area("Your answer:", key=f"quiz_{quiz_item['time']}")

    if st.sidebar.button("Submit answer", key=f"submit_{quiz_item['time']}"):
        evaluation_prompt = (
            f"You are an examiner.\n\n"
            f"Topic: {quiz_item['query']}\n\n"
            f"Student Answer: {user_answer}\n\n"
            "Decide whether the answer is correct or incorrect. "
            "Start your response with either 'Correct:' or 'Incorrect:' "
            "and then give a brief explanation."
        )

        try:
            eval_response = client.models.generate_content(
                model=MODEL_NAME,
                contents=[types.Content(role="user", parts=[types.Part(text=evaluation_prompt)])]
            )
            st.sidebar.markdown("### Evaluation")
            st.sidebar.markdown(eval_response.text)
        except Exception as e:
            st.sidebar.error(f"Error during evaluation: {e}")
