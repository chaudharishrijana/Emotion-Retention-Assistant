import streamlit as st
from transformers import pipeline
from langchain.memory import ConversationBufferMemory
import matplotlib.pyplot as plt
import json
import os

# Load Emotion Detection Model
@st.cache_resource
def load_emotion_classifier():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=True
    )

emotion_classifier = load_emotion_classifier()

# Load Text Generation Model
@st.cache_resource
def load_text_generator():
    return pipeline("text-generation", model="gpt2")

text_generator = load_text_generator()

# Memory
memory = ConversationBufferMemory(return_messages=True)

# Save chat log to JSON file
def save_chat_history_to_file(chat_log, filename="chat_history.json"):
    try:
        with open(filename, "w") as f:
            json.dump(chat_log, f, indent=4)
    except Exception as e:
        st.error(f"Error saving chat history: {e}")

# Load chat log from JSON file
def load_chat_history_from_file(filename="chat_history.json"):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading chat history: {e}")
    return []

# Restore memory from loaded chat history
def restore_memory_from_chat_log(chat_log, memory):
    memory.chat_memory.messages.clear()
    for chat in chat_log:
        memory.chat_memory.add_user_message(chat.get("user", ""))
        memory.chat_memory.add_ai_message(f"Detected Emotion: {chat.get('emotion', 'N/A')}")

# Detect Emotion
def detect_emotion(text):
    result = emotion_classifier(text)[0]
    sorted_result = sorted(result, key=lambda x: x['score'], reverse=True)
    return sorted_result[0]['label'], result

# Update Memory
def update_memory(user_input, emotion):
    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(f"Detected Emotion: {emotion}")

# Churn Risk Logic
def predict_churn(text, emotion):
    negative_emotions = ['anger', 'disgust', 'fear', 'sadness']
    return emotion.lower() in negative_emotions

# Churn Risk Percentage Calculation
def calculate_churn_percent(emotion_scores):
    risk_emotions = ['anger', 'disgust', 'fear', 'sadness']
    risk_score = sum(score['score'] for score in emotion_scores if score['label'].lower() in risk_emotions)
    return risk_score * 100

# Personalized Recommendation
def recommend_action(churn_risk, emotion, user_message):
    prompt = f"""
    You are an AI support assistant. A user sent this message: \"{user_message}\"
    The detected emotion is: {emotion}.
    Based on the tone and context, give a personalized recommendation on how to respond to this user to retain them, if there's a risk.
    Keep it short, empathetic, and helpful.
    """
    output = text_generator(prompt, max_length=100, do_sample=True, top_k=50)[0]['generated_text']
    recommendation = output.replace(prompt, "").strip().split("\n")[0]
    return recommendation

# Emotion Score Graph
def show_emotion_graph(scores):
    labels = [item['label'] for item in scores]
    values = [item['score'] for item in scores]
    color_map = {
        "anger": "#FF6B6B",
        "disgust": "#8D6E63",
        "fear": "#FFD54F",
        "joy": "#4CAF50",
        "neutral": "#90A4AE",
        "sadness": "#42A5F5",
        "surprise": "#BA68C8"
    }
    colors = [color_map.get(label.lower(), "#B0BEC5") for label in labels]
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=colors)
    ax.set_xlabel('Emotions')
    ax.set_ylabel('Confidence Score')
    ax.set_ylim(0, 1)
    ax.set_title("Emotion Confidence Scores")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    return fig

# Churn Risk Graph
def show_churn_graph(churn_percent):
    fig, ax = plt.subplots()
    if churn_percent >= 70:
        color = "#FF5252"
    elif churn_percent >= 40:
        color = "#FFA726"
    else:
        color = "#66BB6A"
    ax.bar(["Churn Risk"], [churn_percent], color=color)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Churn Risk (%)")
    ax.set_title("Churn Risk Percentage")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    return fig

# Streamlit Layout
st.set_page_config(page_title="Emotion Chat", layout="wide")

# Load chat history on startup
if "chat_log" not in st.session_state:
    st.session_state.chat_log = load_chat_history_from_file()
    restore_memory_from_chat_log(st.session_state.chat_log, memory)

# Sidebar - Conversation History
with st.sidebar:
    st.title("\U0001F4DA Conversation History")
    if memory.chat_memory.messages:
        for msg in memory.chat_memory.messages:
            if msg.type == "human":
                st.markdown(f"\U0001F464 {msg.content}")
            else:
                st.markdown(f"\U0001F916 {msg.content}")
    else:
        st.info("No conversation yet.")

# Main UI
st.title(" Emotion Retention Assistant")

# Chat Input
user_input = st.chat_input("Type your message here...")

if user_input:
    emotion, full_scores = detect_emotion(user_input)
    churn = predict_churn(user_input, emotion)
    churn_percent = calculate_churn_percent(full_scores)
    action = recommend_action(churn, emotion, user_input)
    update_memory(user_input, emotion)
    st.session_state.chat_log.append({
        "user": user_input,
        "emotion": emotion,
        "churn": churn,
        "churn_percent": churn_percent,
        "action": action,
        "scores": full_scores
    })
    save_chat_history_to_file(st.session_state.chat_log)

# Display Chat
for chat in st.session_state.chat_log:
    churn_percent = chat.get("churn_percent", 0.0)
    churn_text = "Yes" if chat.get("churn", False) else "No"
    st.chat_message("user").write(chat.get("user", ""))
    st.chat_message("assistant").markdown(
        f"""
        **Detected Emotion:** `{chat.get("emotion", "N/A")}`  
        **Churn Risk:** {churn_text} ({churn_percent:.2f}%)  
        **Recommended Action:** _{chat.get("action", "N/A")}_
        """
    )
    with st.expander("\U0001F4CA Emotion & Churn Graphs"):
        col1, col2 = st.columns(2)
        with col1:
            fig1 = show_emotion_graph(chat.get("scores", []))
            st.pyplot(fig1)
        with col2:
            fig2 = show_churn_graph(churn_percent)
            st.pyplot(fig2)
