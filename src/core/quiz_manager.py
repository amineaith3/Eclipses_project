import json
import random

class QuizManager:
    def __init__(self):
        self.all_questions = []
        self.categories = set()
        self.load_data()
        
    def load_data(self):
        try:
            with open("eclipse_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.all_questions = data.get("questions", [])
                for q in self.all_questions:
                    cat = q.get("category", "General Trivia")
                    self.categories.add(cat)
        except Exception as e:
            print("Error loading eclipse_data.json:", e)
            
    def get_categories(self):
        cats = list(self.categories)
        cats.sort()
        return ["All / Random"] + cats
        
    def setup_quiz(self, category, count):
        pool = self.all_questions
        if category != "All / Random":
            pool = [q for q in pool if q.get("category", "General Trivia") == category]
            
        if count == "All":
            count = len(pool)
        else:
            try:
                count = int(count)
            except ValueError:
                count = 10
            
        count = min(count, len(pool))
        return random.sample(pool, count)
