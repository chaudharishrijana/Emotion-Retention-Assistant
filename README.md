# Emotion-Based Engagement Assistant

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
