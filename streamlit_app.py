import streamlit as st

# Заголовок и описание
st.title("💬 Поддержка с помощью нейронной сети")
st.write(
    "Это чат между пользователем и оператором поддержки, где ответы оператору помогает генерировать нейросеть, подключённая к Qdrant."
)

# Инициализируем историю сообщений
if "messages" not in st.session_state:
    st.session_state.messages = []

# Показываем чат в виде двух колонок
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 Пользователь")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])

with col2:
    st.subheader("🛠️ Поддержка")
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

# Ввод нового сообщения от пользователя
prompt = st.chat_input("Напишите сообщение от пользователя...")
if prompt:
    # Сохраняем сообщение пользователя
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Здесь будет заглушка для ответа нейросети, заменим позже на запрос к Qdrant + модель
    response = f"Ответ от поддержки на: \"{prompt}\""

    # Сохраняем сообщение от поддержки
    st.session_state.messages.append({"role": "assistant", "content": response})