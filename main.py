import streamlit as st
from transformers import pipeline
from langchain.memory import ConversationBufferMemory
import matplotlib.pyplot as plt
import json
import os

# ----- Model loading -----
@st.cache_resource
def load_emotion_classifier():
    return pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=True
    )
emotion_classifier = load_emotion_classifier()

@st.cache_resource
def load_text_generator():
    return pipeline("text-generation", model="gpt2")

text_generator = load_text_generator()

# ----- Files & Memory -----
CHAT_HISTORY_FILE = "chat_history.json"
ARCHIVE_FILE = "archived_chats.json"

memory = ConversationBufferMemory(return_messages=True)

# Utility: Save JSON
def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Utility: Load JSON
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

# Restore LangChain memory from past chat
def restore_memory(chat_log):
    memory.chat_memory.messages.clear()
    for chat in chat_log:
        memory.chat_memory.add_user_message(chat.get("user", ""))
        memory.chat_memory.add_ai_message(f"Detected Emotion: {chat.get('emotion', 'N/A')}")

# ----- Emotion and churn logic -----
def detect_emotion(text):
    result = emotion_classifier(text)[0]
    sorted_result = sorted(result, key=lambda x: x['score'], reverse=True)
    return sorted_result[0]['label'], result

def update_memory(user_input, emotion):
    memory.chat_memory.add_user_message(user_input)
    memory.chat_memory.add_ai_message(f"Detected Emotion: {emotion}")

def predict_churn(text, emotion):
    negative_emotions = ['anger', 'disgust', 'fear', 'sadness']
    return emotion.lower() in negative_emotions

def calculate_churn_percent(emotion_scores):
    risk_emotions = ['anger', 'disgust', 'fear', 'sadness']
    risk_score = sum(score['score'] for score in emotion_scores if score['label'].lower() in risk_emotions)
    return risk_score * 100

def recommend_action(churn_risk, emotion, user_message):
    prompt = f"""
You are an AI support assistant. A user sent this message: "{user_message}"
The detected emotion is: {emotion}.
Based on the tone and context, give a personalized recommendation on how to respond to this user to retain them, if there's a risk.
Keep it short, empathetic, and helpful.
"""
    output = text_generator(prompt, max_length=100, do_sample=True, top_k=50)[0]['generated_text']
    recommendation = output.replace(prompt, "").strip().split("\n")[0]
    return recommendation

# ----- Visualization -----
def show_emotion_graph(scores):
    labels = [item['label'] for item in scores]
    values = [item['score'] for item in scores]
    color_map = {
        "anger": "#FF6B6B", "disgust": "#8D6E63", "fear": "#FFD54F", "joy": "#4CAF50",
        "neutral": "#90A4AE", "sadness": "#42A5F5", "surprise": "#BA68C8"
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

def show_churn_graph(churn_percent):
    fig, ax = plt.subplots()
    color = "#FF5252" if churn_percent >= 70 else "#FFA726" if churn_percent >= 40 else "#66BB6A"
    ax.bar(["Churn Risk"], [churn_percent], color=color)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Churn Risk (%)")
    ax.set_title("Churn Risk Percentage")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    return fig

# ----- Session State Initialization -----
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

if "archived_chats" not in st.session_state:
    st.session_state.archived_chats = load_json(ARCHIVE_FILE)

if "selected_chat_index" not in st.session_state:
    st.session_state.selected_chat_index = None

# Restore memory on load
restore_memory(st.session_state.chat_log)

# ----- Chat control functions -----
def new_chat(chat_name):
    if st.session_state.chat_log:
        st.session_state.archived_chats.append({
            "name": chat_name,
            "chat": st.session_state.chat_log.copy()
        })
        save_json(st.session_state.archived_chats, ARCHIVE_FILE)
    st.session_state.chat_log = []
    save_json(st.session_state.chat_log, CHAT_HISTORY_FILE)
    restore_memory(st.session_state.chat_log)
    st.session_state.selected_chat_index = None

def delete_all_history():
    st.session_state.archived_chats = []
    st.session_state.chat_log = []
    save_json(st.session_state.archived_chats, ARCHIVE_FILE)
    save_json(st.session_state.chat_log, CHAT_HISTORY_FILE)
    restore_memory(st.session_state.chat_log)
    st.session_state.selected_chat_index = None

def load_archived_chat(index):
    if 0 <= index < len(st.session_state.archived_chats):
        st.session_state.chat_log = st.session_state.archived_chats[index]["chat"]
        save_json(st.session_state.chat_log, CHAT_HISTORY_FILE)
        restore_memory(st.session_state.chat_log)

def delete_archived_chat(index):
    if 0 <= index < len(st.session_state.archived_chats):
        del st.session_state.archived_chats[index]
        save_json(st.session_state.archived_chats, ARCHIVE_FILE)
        st.session_state.selected_chat_index = None

# ----- Sidebar UI -----
with st.sidebar:
    st.title("\U0001F4DA Conversation History")

    chat_name = st.text_input("New Chat Name", value="Untitled Chat")
    col_new, col_del_all = st.columns([1, 1])
    with col_new:
        if st.button("📝 New Chat"):
            new_chat(chat_name)
    with col_del_all:
        if st.button("🗑️ Delete All History"):
            delete_all_history()

    st.markdown("---")

    if st.session_state.archived_chats:
        options = [chat["name"] for chat in st.session_state.archived_chats]
        selected_index = st.session_state.selected_chat_index or 0
        selected_index = min(selected_index, len(options) - 1)
        selected_name = st.selectbox("Select Chat", options=options, index=selected_index)
        st.session_state.selected_chat_index = options.index(selected_name)

        col_load, col_del = st.columns([1, 1])
        with col_load:
            if st.button("Load Selected Chat"):
                load_archived_chat(st.session_state.selected_chat_index)
        with col_del:
            if st.button("Delete Selected Chat"):
                delete_archived_chat(st.session_state.selected_chat_index)
    else:
        st.info("No archived chats yet.")

# ----- Main Chat UI -----
st.title("Emotion Retention Assistant")
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
    save_json(st.session_state.chat_log, CHAT_HISTORY_FILE)

# ----- Chat Display -----
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
