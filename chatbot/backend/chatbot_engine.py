import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SALUTATIONS = {
    "bonjour": "Bonjour 😊 ! Je suis ChatMI. Pose-moi une question sur une anomalie ou une panne.",
    "salut": "Salut 👋 ! En quoi puis-je vous aider ?",
    "hello": "Hello ! Je suis à votre service.",
    "ça va": "Je vais bien merci, prêt à vous aider !",
    "bonsoir": "Bonsoir 🌙 ! Prêt à analyser vos problèmes techniques ?"
}

class ChatbotEngine:
    def __init__(self, path_to_file):
        self.df = pd.read_excel(path_to_file)
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.df['Question'])

    def get_response(self, user_input):
        user_input_lower = user_input.lower()
        
        # 🎯 Détection des salutations
        for mot in SALUTATIONS:
            if mot in user_input_lower:
                return {
                    "question_trouvée": mot,
                    "réponse": SALUTATIONS[mot],
                    "solution": "N'hésitez pas à poser une question technique.",
                    "type_anomalie": "Général"
                }

        # 🔍 Sinon, répondre avec logique TF-IDF
        input_vec = self.vectorizer.transform([user_input])
        similarities = cosine_similarity(input_vec, self.question_vectors)
        idx = similarities.argmax()
        best_match = self.df.iloc[idx]
        return {
            "question_trouvée": best_match["Question"],
            "réponse": best_match["Réponse"],
            "solution": best_match["Solution"],
            "type_anomalie": best_match["Type d'anomalie"]
        }
