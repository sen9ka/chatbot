import streamlit as st

st.set_page_config(layout="wide")

# === Инициализация состояния ===
def init_state():
    for prefix in ["user", "support"]:
        if f"{prefix}_topics" not in st.session_state:
            st.session_state[f"{prefix}_topics"] = {}
        if f"{prefix}_active_topic" not in st.session_state:
            topic_name = f"Новая тема"
            st.session_state[f"{prefix}_active_topic"] = topic_name
            st.session_state[f"{prefix}_topics"][topic_name] = []

init_state()

# === Генерация названия темы по сообщению ===
def generate_topic_name(message):
    short = message.strip().split("\n")[0][:30]
    return short if short else "Без названия"

# === Боковая панель для каждой роли ===
def sidebar(role):
    prefix = f"{role}_"
    topics = st.session_state[f"{prefix}topics"]
    active_topic = st.session_state[f"{prefix}active_topic"]

    with st.sidebar:
        st.markdown(f"### {'👤 Пользователь' if role == 'user' else '🛠️ Поддержка'}")
        st.markdown("#### Темы")

        # Кнопка создания новой темы
        if st.button("➕ Новая тема", key=f"new_topic_{role}"):
            topic_name = "Новая тема"
            counter = 1
            while topic_name in topics:
                topic_name = f"Новая тема {counter}"
                counter += 1
            topics[topic_name] = []
            st.session_state[f"{prefix}active_topic"] = topic_name

        # Список тем
        for topic in list(topics.keys()):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                if st.button(topic, key=f"select_{role}_{topic}"):
                    st.session_state[f"{prefix}active_topic"] = topic
            with col2:
                if st.button("🗑️", key=f"delete_{role}_{topic}"):
                    topics.pop(topic)
                    if topic == active_topic:
                        st.session_state[f"{prefix}active_topic"] = next(iter(topics), "Новая тема")
                        if st.session_state[f"{prefix}active_topic"] not in topics:
                            st.session_state[f"{prefix}topics"][st.session_state[f'{prefix}active_topic']] = []
                    st.experimental_rerun()

# === Отображение боковых панелей ===
sidebar("user")

# === Интерфейс ===
col_user, col_support = st.columns(2)

# === Интерфейс Пользователя ===
with col_user:
    st.subheader("👤 Интерфейс Пользователя")
    user_topics = st.session_state.user_topics
    active_user_topic = st.session_state.user_active_topic

    st.caption(f"💬 Тема: {active_user_topic}")
    for msg in user_topics[active_user_topic]:
        with st.chat_message(msg["role"]):
            align = "right" if msg["role"] == "user" else "left"
            st.markdown(f"<div style='text-align: {align};'>{msg['content']}</div>", unsafe_allow_html=True)

    user_input = st.text_input("Пользователь вводит сообщение:", key="user_input")
    if st.button("Отправить как Пользователь"):
        if user_input:
            # Если первое сообщение — переименовать тему
            if len(user_topics[active_user_topic]) == 0:
                new_name = generate_topic_name(user_input)
                user_topics[new_name] = user_topics.pop(active_user_topic)
                st.session_state.user_active_topic = new_name
                active_user_topic = new_name

            user_topics[active_user_topic].append({"role": "user", "content": user_input})

# === Интерфейс Поддержки ===
with col_support:
    st.subheader("🛠️ Интерфейс Поддержки")
    support_topics = st.session_state.support_topics
    active_support_topic = st.session_state.support_active_topic

    st.caption(f"💬 Тема: {active_support_topic}")
    for msg in support_topics[active_support_topic]:
        with st.chat_message(msg["role"]):
            align = "right" if msg["role"] == "assistant" else "left"
            st.markdown(f"<div style='text-align: {align};'>{msg['content']}</div>", unsafe_allow_html=True)

    support_input = st.text_input("Поддержка отвечает:", key="support_input")
    if st.button("Ответить как Поддержка"):
        if support_input:
            # Если первое сообщение — переименовать тему
            if len(support_topics[active_support_topic]) == 0:
                new_name = generate_topic_name(support_input)
                support_topics[new_name] = support_topics.pop(active_support_topic)
                st.session_state.support_active_topic = new_name
                active_support_topic = new_name

            support_topics[active_support_topic].append({"role": "assistant", "content": support_input})