# streamlit_app.py
import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Charger le dataset
df = pd.read_excel("chatbot_data/chatbot_anomalies_roulements_20000.xlsx")

# Charger le modèle BERT
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(df['Question'].tolist(), convert_to_tensor=True)

# Interface Streamlit
st.title("🤖 Chatbot IA sur les anomalies mécaniques")

user_input = st.text_input("Pose ta question :")

if user_input:
    query_embedding = model.encode(user_input, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    best_idx = scores.argmax().item()
    best_match = df.iloc[best_idx]

    st.markdown(f"**Question correspondante :** {best_match['Question']}")
    st.markdown(f"**Réponse :** {best_match['Réponse']}")
    st.markdown(f"**Solution :** {best_match['Solution']}")
    st.markdown(f"**Type d'anomalie :** {best_match['Type d\'anomalie']}")
