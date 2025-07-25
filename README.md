# Emotion Retention System

![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0-blue)

An AI-powered emotion analysis tool using LangChain for conversation management, detecting user emotions in real-time, predicting disengagement risk, and generating personalized interaction strategies.

##  Overview
This Streamlit application combines NLP models with LangChain's memory management to:
1. Detect emotions in user messages using Hugging Face Transformers
2. Manage conversation history with LangChain's memory buffers
3. Predict disengagement risk based on emotional patterns
4. Generate AI-powered interaction recommendations
5. Visualize emotional patterns and risk factors

##  Key Features
- **LangChain Memory Management**: Persistent conversation history with `ConversationBufferMemory`
- **Real-time Emotion Detection**: DistilRoBERTa model classifies text into 7 emotions
- **Disengagement Prediction**: Risk calculation based on negative emotions
- **AI Recommendations**: GPT-2 generates personalized engagement strategies
- **Interactive Visualizations**: Emotion distribution charts and risk indicators
- **Data Persistence**: Automatic saving/loading of chat history to JSON

##  LangChain Implementation
```mermaid
graph LR
    A[User Input] --> B[LangChain Memory]
    B --> C[Emotion Detection]
    C --> D[Risk Analysis]
    D --> E[Response Generation]
    E --> F[Update Memory]
    F --> G[Persistent Storage]



Overview
The Emotion Retention Assistant is an AI-powered analytics tool that helps customer support teams identify at-risk customers by analyzing emotional sentiment in text communications. The application combines natural language processing with visualization tools to provide actionable insights for customer retention.

Key Features
Real-time Emotion Analysis: Classifies text into 7 emotional categories

Churn Risk Prediction: Calculates customer departure probability

AI-Powered Recommendations: Generates retention strategies using GPT-2

Conversation Management: Archives and restores chat histories

Data Visualization: Interactive emotion and risk charts

Technical Architecture
Diagram
Code
graph TD
    A[User Input] --> B(Emotion Classifier)
    A --> C(GPT-2 Generator)
    B --> D[Emotion Scores]
    D --> E[Churn Calculator]
    E --> F[Risk Visualization]
    C --> G[Retention Recommendation]
    D --> G
    E --> G
    F --> H[Dashboard]
    G --> H
Installation
Requirements
Python 3.8+

pip package manager

Setup Process
Create a requirements.txt file with:

txt
streamlit>=1.22
transformers>=4.30
torch>=2.0
langchain>=0.0.346
matplotlib>=3.7
Install dependencies:

bash
pip install -r requirements.txt
Launch application:

bash
streamlit run app.py
Usage Guide
Interface Overview
Component	Functionality
Main Chat Area	Displays conversation history with analysis
Input Box	Message entry at bottom of screen
Sidebar	Conversation management controls
Expandable Panels	Detailed emotion and risk visualizations
Workflow
Enter customer message in chat input

Application returns:

Primary detected emotion

Churn risk percentage

AI-generated retention recommendation

Expand panels to view detailed emotion distribution and risk assessment

Conversation Management
Action	Method	Data Persistence
New Conversation	Sidebar: "New Chat"	Creates new chat_history.json
Archive Chat	Automatic on new chat start	Saves to archived_chats.json
Restore Conversation	Sidebar: "Load Selected"	Retrieves from archived_chats.json
Delete History	Sidebar: "Delete All"	Clears all JSON files
Technical Specifications
AI Models
Model	Purpose	Specifications
j-hartmann/emotion-english-distilroberta-base	Emotion classification	7 emotional categories, DistilRoBERTa architecture
gpt2	Recommendation engine	117M parameters, fine-tuned for retention strategies
Core Algorithms
python
# Emotion Detection
def detect_emotion(text):
    results = classifier(text)[0]
    return sorted(results, key=lambda x: x['score'], reverse=True)

# Churn Risk Calculation
def calculate_churn_percent(scores):
    risk_emotions = ['anger', 'disgust', 'fear', 'sadness']
    return sum(score['score'] for score in scores 
               if score['label'].lower() in risk_emotions) * 100

# Recommendation Engine
def recommend_action(emotion, user_message):
    prompt = f"Generate retention response for: {user_message} with emotion {emotion}"
    return generator(prompt, max_length=100)[0]['generated_text']
Data Persistence
File	Structure	Purpose
chat_history.json	List of message objects	Current conversation
archived_chats.json	List of {name, chat} objects	Historical conversations
Visualization System
Visualization	Type	Color Coding
Emotion Distribution	Horizontal Bar Chart	Emotion-specific palette
Churn Risk	Single Bar Meter	Gradient (green → red)


