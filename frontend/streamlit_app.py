

# frontend/streamlit_app.py
import streamlit as st
from backend.chatbot_engine import ChatbotEngine

# Initialiser le chatbot
engine = ChatbotEngine("chatbot_data/chatbot_anomalies_roulements_20000.xlsx")

st.title("🤖 Chatbot de Maintenance Prédictive")
user_input = st.text_input("Posez une question sur une anomalie mécanique :")

if user_input:
    result = engine.get_response(user_input)
    st.subheader("Réponse détectée :")
    st.write(f"**Question reconnue :** {result['question_trouvée']}")
    st.write(f"**Réponse :** {result['réponse']}")
    st.write(f"**Solution recommandée :** {result['solution']}")
    st.write(f"**Type d'anomalie :** {result['type_anomalie']}")

