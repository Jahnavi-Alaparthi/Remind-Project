import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import json
import random
from datetime import datetime
QUIZ_AFTER = 5
MODEL_NAME = "gemini-2.5-flash-lite"
DATA_FILE = "chat_history.json"

st.set_page_config(
    page_title="Gemini Quiz Bot",
    layout="centered"
)

st.title(" Gemini Chatbot with Automatic Quiz")
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env file")
    st.stop()

client = genai.Client(api_key=api_key)
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_interaction(query, response):
    data = load_data()
    data.append({
        "query": query,
        "response": response,
        "time": datetime.now().isoformat()
    })
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_interaction(query, response):
    data = load_data()
    data.append({
        "query": query,
        "response": response,
        "time": datetime.now().isoformat()
    })
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "counter" not in st.session_state:
    st.session_state.counter = 0

if "recent_queries" not in st.session_state:
    st.session_state.recent_queries = []

if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None

if "show_quiz" not in st.session_state:
    st.session_state.show_quiz = False
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
user_input = st.chat_input("Ask anything...")

if user_input:
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Update counter
    st.session_state.counter += 1
    st.session_state.recent_queries.append(user_input)

    # Call Gemini
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_input
    )
    reply = response.text

    # Show assistant reply immediately
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    save_interaction(user_input, reply)
    if st.session_state.counter == QUIZ_AFTER:
        quiz_topic = random.choice(st.session_state.recent_queries)

        quiz_prompt = (
            "Create a short conceptual quiz question.\n"
            "Do NOT give the answer.\n\n"
            f"Topic: {quiz_topic}"
        )

        quiz_response = client.models.generate_content(
            model=MODEL_NAME,
            contents=quiz_prompt
        )

        st.session_state.quiz_question = quiz_response.text
        st.session_state.show_quiz = True

        st.session_state.counter = 0
        st.session_state.recent_queries = []
if st.session_state.show_quiz:
    st.divider()
    st.subheader(" Quiz Time!")

    st.markdown(st.session_state.quiz_question)

    user_answer = st.text_area("Your answer:")

    if st.button("Submit Answer"):
        evaluation_prompt = (
            "You are an examiner.\n\n"
            f"Question: {st.session_state.quiz_question}\n\n"
            f"Student Answer: {user_answer}\n\n"
            "Start with Correct: or Incorrect: and explain briefly."
        )

        evaluation = client.models.generate_content(
            model=MODEL_NAME,
            contents=evaluation_prompt
        )

        st.success("Evaluation")
        st.markdown(evaluation.text)

        st.session_state.show_quiz = False
        st.session_state.quiz_question = None
