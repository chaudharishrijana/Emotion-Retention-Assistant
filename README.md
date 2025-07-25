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
text

Key fixes made:
1. Removed the HTML comment `<!-- Triple backticks close the Mermaid block -->` from inside the Mermaid code block
2. Removed the text "Installation Requirements Python 3.8+..." that was accidentally inside the code block
3. Maintained proper Markdown formatting with:
   - Triple backticks to open/close code blocks
   - Clear section headers
   - Consistent indentation

The Mermaid diagram should now render properly on GitHub/GitLab. Remember:
- Mermaid diagrams must contain ONLY diagram syntax
- No additional text/comments inside the code block
- Use exactly three backticks to open/close code blocks
- Place all non-diagram content outside the Mermaid block
New chat

