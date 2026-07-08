import customtkinter as ctk
from src.core.gamification import GamificationManager
from src.core.quiz_manager import QuizManager
# pyrefly: ignore [missing-import]
from src.ui.menu_frame import MenuFrame
from src.ui.simulator_frame import SimulatorFrame
from src.ui.quiz_setup_frame import QuizSetupFrame
from src.ui.quiz_frame import QuizFrame
from src.ui.result_frame import ResultFrame
from src.ui.profile_frame import ProfileFrame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EclipseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Eclipse Explorer Q&A Pro")
        self.geometry("1000x750")
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        import tkinter as tk
        import os
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'Astronest.png')
        if os.path.exists(icon_path):
            try:
                img = tk.PhotoImage(file=icon_path)
                self.iconphoto(False, img)
            except Exception as e:
                print("Could not set icon:", e)
        
        self.gamification = GamificationManager(self)
        self.quiz_manager = QuizManager()
        
        # App State
        self.current_quiz_questions = []
        self.current_score = 0
        
        self.frames = {}
        self.frames["menu"] = MenuFrame(self, self)
        self.frames["simulator"] = SimulatorFrame(self, self)
        self.frames["quiz_setup"] = QuizSetupFrame(self, self)
        self.frames["quiz"] = QuizFrame(self, self)
        self.frames["result"] = ResultFrame(self, self)
        self.frames["profile"] = ProfileFrame(self, self)
        
        self.show_frame("menu")
        
    def show_frame(self, name):
        for frame in self.frames.values():
            frame.grid_forget()
            
        if name == "menu":
            self.frames["menu"].update_view()
        elif name == "profile":
            self.frames["profile"].update_view()
        elif name == "quiz_setup":
            self.frames["quiz_setup"].update_view()
            
        self.frames[name].grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
    def start_quiz(self, category, count):
        self.current_quiz_questions = self.quiz_manager.setup_quiz(category, count)
        if not self.current_quiz_questions:
            return
        self.frames["quiz"].start(self.current_quiz_questions)
        self.show_frame("quiz")
