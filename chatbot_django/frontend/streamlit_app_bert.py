# frontend/streamlit_app_bert.py
import streamlit as st
from backend.chatbot_engine_bert import SmartChatbot

bot = SmartChatbot("chatbot_data/chatbot_anomalies_roulements_20000.xlsx")

st.title("🧠 Chatbot Intelligent (BERT)")
user_input = st.text_input("Posez une question technique :")

if user_input:
    result = bot.get_response(user_input)
    st.write(f"**Question la plus proche :** {result['question_trouvée']}")
    st.write(f"**Réponse :** {result['réponse']}")
    st.write(f"**Solution :** {result['solution']}")
    st.write(f"**Type d'anomalie :** {result['type_anomalie']}")
    st.write(f"**Similarité :** {result['similarité']:.2f}")
