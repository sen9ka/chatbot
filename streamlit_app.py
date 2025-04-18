import streamlit as st
import uuid

st.set_page_config(layout="wide")

# === Инициализация состояния ===
if "topics" not in st.session_state:
    st.session_state.topics = {}
if "active_topic" not in st.session_state:
    # Создаём первую тему
    new_topic_id = str(uuid.uuid4())[:8]
    st.session_state.active_topic = f"Новая тема {new_topic_id}"
    st.session_state.topics[st.session_state.active_topic] = []

# === Функция отображения боковой панели ===
def sidebar(role):
    with st.sidebar:
        st.markdown(f"### {'👤 Пользователь' if role == 'user' else '🛠️ Поддержка'}")
        st.markdown("#### История тем")

        # Кнопка создания новой темы
        if st.button("➕ Новая тема"):
            new_topic_id = str(uuid.uuid4())[:8]
            topic_name = f"Новая тема {new_topic_id}"
            st.session_state.topics[topic_name] = []
            st.session_state.active_topic = topic_name

        # Список всех тем
        for topic in list(st.session_state.topics.keys()):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                if st.button(topic, key=f"select_{role}_{topic}"):
                    st.session_state.active_topic = topic
            with col2:
                if st.button("🗑️", key=f"delete_{role}_{topic}"):
                    st.session_state.topics.pop(topic)
                    if topic == st.session_state.active_topic:
                        if st.session_state.topics:
                            st.session_state.active_topic = list(st.session_state.topics.keys())[0]
                        else:
                            new_topic_id = str(uuid.uuid4())[:8]
                            st.session_state.active_topic = f"Новая тема {new_topic_id}"
                            st.session_state.topics[st.session_state.active_topic] = []
                    st.experimental_rerun()

# === Вызов боковых панелей ===
sidebar("user")  # Покажется в левой панели

# === Две колонки: пользователь и поддержка ===
col_user, col_support = st.columns(2)

# === Интерфейс Пользователя ===
with col_user:
    st.subheader("👤 Интерфейс Пользователя")
    st.caption(f"💬 Тема: {st.session_state.active_topic}")

    for msg in st.session_state.topics[st.session_state.active_topic]:
        with st.chat_message(msg["role"]):
            align = "right" if msg["role"] == "user" else "left"
            st.markdown(f"<div style='text-align: {align};'>{msg['content']}</div>", unsafe_allow_html=True)

    user_input = st.text_input("Пользователь вводит сообщение:", key="user_input")
    if st.button("Отправить как Пользователь"):
        if user_input:
            st.session_state.topics[st.session_state.active_topic].append({"role": "user", "content": user_input})

# === Интерфейс Поддержки ===
with col_support:
    st.subheader("🛠️ Интерфейс Поддержки")
    st.caption(f"💬 Тема: {st.session_state.active_topic}")

    for msg in st.session_state.topics[st.session_state.active_topic]:
        with st.chat_message(msg["role"]):
            align = "right" if msg["role"] == "assistant" else "left"
            st.markdown(f"<div style='text-align: {align};'>{msg['content']}</div>", unsafe_allow_html=True)

    support_input = st.text_input("Поддержка отвечает:", key="support_input")
    if st.button("Ответить как Поддержка"):
        if support_input:
            st.session_state.topics[st.session_state.active_topic].append({"role": "assistant", "content": support_input})