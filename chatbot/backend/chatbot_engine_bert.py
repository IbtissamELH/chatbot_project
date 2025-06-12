# backend/chatbot_engine_bert.py
import pandas as pd
from sentence_transformers import SentenceTransformer,util

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["Ceci est un exemple."])
print(embeddings)
class SmartChatbot:
    def __init__(self, path_to_file):
        self.df = pd.read_excel(path_to_file)
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.embeddings = self.model.encode(self.df['Question'].tolist(), convert_to_tensor=True)

    def get_response(self, user_input):
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
