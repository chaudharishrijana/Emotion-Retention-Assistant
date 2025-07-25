# Emotion Retention Assistant

## Overview
The Emotion Retention Assistant is an AI-powered analytics tool that helps customer support teams identify at-risk customers by analyzing emotional sentiment in text communications. The application combines natural language processing with visualization tools to provide actionable insights for customer retention.

## Key Features
- **Real-time Emotion Analysis**: Classifies text into 7 emotional categories
- **Churn Risk Prediction**: Calculates customer departure probability
- **AI-Powered Recommendations**: Generates retention strategies using GPT-2
- **Conversation Management**: Archives and restores chat histories
- **Data Visualization**: Interactive emotion and risk charts

## Technical Architecture
```mermaid
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
