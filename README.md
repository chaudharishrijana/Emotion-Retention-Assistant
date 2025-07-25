# 🧠 Emotion Retention Assistant

The **Emotion Retention Assistant** is an AI-powered Streamlit web app that detects user emotions from chat messages, calculates churn risk, and recommends empathetic responses using GPT-2. It visualizes emotional states and helps support teams better retain customers based on sentiment.

---

## 🚀 Features

- 🔍 Emotion detection using a fine-tuned RoBERTa model
- 📉 Churn risk prediction based on emotional tone
- 🤖 GPT-2 powered personalized recommendations
- 📊 Emotion and churn risk visualizations
- 💬 LangChain-based memory for chat history
- 🗂️ Save, load, and manage previous chat sessions

---

## 🖼️ Demo Preview

<p align="center">
  <img src="https://user-images.githubusercontent.com/your-screenshot-path/demo.png" alt="App Preview" width="80%">
</p>

---

## 🧰 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **NLP Models**: [Hugging Face Transformers](https://huggingface.co/)
  - Emotion model: `j-hartmann/emotion-english-distilroberta-base`
  - Text generation: `gpt2`
- **Memory**: [LangChain](https://www.langchain.com/)
- **Visualization**: `matplotlib`
- **Storage**: JSON files for local chat history and archives

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/emotion-retention-assistant.git
cd emotion-retention-assistant

2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
