# backend/chatbot_engine.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ChatbotEngine:
    def __init__(self, path_to_file):
        self.df = pd.read_excel(path_to_file)
        self.vectorizer = TfidfVectorizer()
        self.question_vectors = self.vectorizer.fit_transform(self.df['Question'])

    def get_response(self, user_input):
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
