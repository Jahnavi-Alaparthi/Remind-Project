# Re-Mind Project
# Overview

Re-Mind is an agentic AI–based chatbot system designed to improve memory retention through interaction, stored context, and automated quizzing.
The project consists of multiple chatbots that demonstrate persistence, time-based logic, and autonomous quiz generation using a generative AI model.

# Tools Used (Overall)

Python

Streamlit

Google Gemini (Generative AI)

JSON

datetime

random

# .env file 

Stores the Gemini API key securely as an environment variable.
This prevents exposing sensitive credentials in the source code.

# app.py — Basic Chatbot
Tools Used

Python

Streamlit

Google Gemini

Description:

A basic chatbot that answers user questions using the Gemini model.

Important Code Block: Calling the Gemini Model
response = client.models.generate_content(
    model=MODEL_NAME,
    contents=[
        types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )
    ]
)
reply = response.text


Explanation:
This block sends the user’s input to the Gemini model using a structured prompt format.
The model processes the input and returns a generated response, which is then displayed in the Streamlit chat interface.

# counterbot.py — Query-Based Quiz Bot
Tools Used

Python

Streamlit

Google Gemini

JSON

random

Description

This chatbot stores user queries and automatically quizzes the user after every 5 questions.
One of the previously asked questions is selected randomly as the quiz topic.

Important Code Block: JSON Storage
def save_interaction(query, response):
    data = load_data()
    data["interactions"].append({
        "query": query,
        "response": response
    })
    save_data(data)


Explanation:
This function enables persistent memory.
Each user interaction is saved to a JSON file, allowing the chatbot to remember previous queries even after the program restarts.
The stored data is later used to generate quiz questions.

# timebot.py — Time-Based Quiz Bot
Tools Used

Python

Streamlit

Google Gemini

JSON

datetime

Description

This chatbot stores the time at which each query is asked and quizzes the user on that query 10 minutes later, demonstrating time-based decision-making.

Important Code Block: Timestamp Storage
from datetime import datetime

data["interactions"].append({
    "query": query,
    "response": response,
    "time": datetime.now().isoformat()
})


Explanation:
The datetime module is used to record the exact time of each interaction.
The timestamp is stored in ISO format so it can be safely saved in JSON.
This allows the chatbot to compare current time with past interactions and decide when to trigger a quiz.

# Key Concept Demonstrated: Agentic AI

This project demonstrates agentic AI principles by enabling the chatbot to:

Store information (memory)

Make decisions (when to quiz)

Use tools (JSON, time, random selection)

Act autonomously without explicit user instruction

# Purpose

This project was developed as part of the Winter in Data Science (WiDS) 2025 program to gain hands-on experience with:

Generative AI APIs

Stateful chatbot design

Persistent storage

Autonomous AI behavior
