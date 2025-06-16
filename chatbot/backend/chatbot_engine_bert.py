# backend/chatbot_engine_bert.py
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# 🔹 Dictionnaire de réponses simples
SALUTATIONS = {
    "bonjour": "Bonjour 😊 ! Je suis ChatMI. Pose-moi une question sur une anomalie ou une panne.",
    "salut": "Salut 👋 ! En quoi puis-je vous aider ?",
    "hello": "Hello ! Je suis à votre service.",
    "ça va": "Je vais bien merci, prêt à vous aider !",
    "bonsoir": "Bonsoir 🌙 ! Prêt à analyser vos problèmes techniques ?"
}

class SmartChatbot:
    def __init__(self, path_to_file):
        self.df = pd.read_excel(path_to_file)
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.embeddings = self.model.encode(self.df['Question'].tolist(), convert_to_tensor=True)

    def get_response(self, user_input):
        user_input_lower = user_input.lower()

        # 🎯 Vérifie s’il s’agit d’une salutation
        for mot in SALUTATIONS:
            if mot in user_input_lower:
                return {
                    "question_trouvée": mot,
                    "réponse": SALUTATIONS[mot],
                    "solution": "N'hésitez pas à poser une question technique.",
                    "type_anomalie": "Général",
                    "similarité": 1.0
                }

        # 🧠 Sinon, logique BERT classique
        query_embedding = self.model.encode(user_input, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        best_idx = scores.argmax().item()
        best_match = self.df.iloc[best_idx]
        return {
            "question_trouvée": best_match["Question"],
            "réponse": best_match["Réponse"],
            "solution": best_match["Solution"],
            "type_anomalie": best_match["Type d'anomalie"],
            "similarité": scores[best_idx].item()
        }
