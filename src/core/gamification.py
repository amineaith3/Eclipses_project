import json
import os
import customtkinter as ctk

class GamificationManager:
    def __init__(self, root):
        self.root = root
        
        # Save to AppData so it doesn't clutter the project folder
        appdata = os.getenv('APPDATA')
        if appdata:
            self.save_dir = os.path.join(appdata, 'EclipseExplorer')
        else:
            self.save_dir = os.path.join(os.path.expanduser('~'), '.eclipse_explorer')
            
        os.makedirs(self.save_dir, exist_ok=True)
        self.progress_file = os.path.join(self.save_dir, "user_progress.json")
        
        self.user_data = self.default_data()
        self.load()

    def default_data(self):
        return {
            "badges": [],
            "quizzes_taken": 0,
            "simulations_watched": 0
        }

    def load(self):
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, "r") as f:
                    self.user_data = json.load(f)
            except Exception:
                pass

    def save(self):
        try:
            with open(self.progress_file, "w") as f:
                json.dump(self.user_data, f, indent=4)
        except Exception as e:
            print("Error saving progress:", e)

    def reset_account(self):
        self.user_data = self.default_data()
        self.save()
        if os.path.exists("user_progress.json"):
            try: os.remove("user_progress.json") # Cleanup legacy
            except: pass

    def award_badge(self, badge_name):
        if badge_name not in self.user_data["badges"]:
            self.user_data["badges"].append(badge_name)
            self.save()
            self.show_badge_unlocked(badge_name)
            return True
        return False
        
    def evaluate_quiz_badges(self, score, total_questions):
        self.user_data["quizzes_taken"] += 1
        self.award_badge("Scholar")
            
        if total_questions >= 20:
            self.award_badge("Novice Eclipse Chaser")
            
            pct = score / total_questions
            if pct >= 0.8:
                self.award_badge("Silver Corona")
            if pct >= 0.9:
                self.award_badge("Golden Umbra")
            if pct == 1.0:
                self.award_badge("Diamond Ring Master")
                
        self.save()

    def show_badge_unlocked(self, badge_name):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Badge Unlocked!")
        popup.geometry("350x150")
        popup.attributes("-topmost", True)
        
        lbl = ctk.CTkLabel(popup, text="🏆 Badge Unlocked! 🏆", font=ctk.CTkFont(size=20, weight="bold"), text_color="#ffb74d")
        lbl.pack(pady=(20, 10))
        
        name_lbl = ctk.CTkLabel(popup, text=badge_name, font=ctk.CTkFont(size=18, weight="bold"))
        name_lbl.pack(pady=5)
        
        # Auto-close
        self.root.after(4000, popup.destroy)
