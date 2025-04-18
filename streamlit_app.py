import streamlit as st

st.set_page_config(layout="wide")

st.title("💬 Чат: Пользователь ↔ Поддержка")
st.write("Каждая сторона видит свою сторону чата как в привычных мессенджерах.")

# Инициализируем историю сообщений
if "messages" not in st.session_state:
    st.session_state.messages = []

# Создаём две колонки: пользователь и поддержка
col_user, col_support = st.columns(2)

# === Интерфейс Пользователя ===
with col_user:
    st.subheader("👤 Интерфейс Пользователя")

    for msg in st.session_state.messages:
        with st.chat_message("user" if msg["role"] == "user" else "assistant", avatar="💬"):
            align = "right" if msg["role"] == "user" else "left"
            st.markdown(f"<div style='text-align: {align};'>{msg['content']}</div>", unsafe_allow_html=True)

    user_input = st.text_input("Пользователь вводит сообщение:", key="user_input")
    if st.button("Отправить как Пользователь"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

# === Интерфейс Поддержки ===
with col_support:
    st.subheader("🛠️ Интерфейс Поддержки")

    for msg in st.session_state.messages:
        with st.chat_message("assistant" if msg["role"] == "assistant" else "user", avatar="💬"):
            align = "right" if msg["role"] == "assistant" else "left"
            st.markdown(f"<div style='text-align: {align};'>{msg['content']}</div>", unsafe_allow_html=True)

    support_input = st.text_input("Поддержка отвечает:", key="support_input")
    if st.button("Ответить как Поддержка"):
        if support_input:
            st.session_state.messages.append({"role": "assistant", "content": support_input})