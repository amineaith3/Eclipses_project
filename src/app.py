import customtkinter as ctk
from src.core.gamification import GamificationManager
from src.core.quiz_manager import QuizManager
from src.ui.simulator_frame import SimulatorFrame
from src.ui.quiz_setup_frame import QuizSetupFrame
from src.ui.quiz_frame import QuizFrame
from src.ui.result_frame import ResultFrame
from src.ui.profile_frame import ProfileFrame
from src.ui.glossary_frame import GlossaryFrame
import os
import tkinter as tk
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EclipseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Eclipse Explorer Q&A Pro")
        self.geometry("1100x750")
        self.resizable(False, False)
        
        # Window Icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', 'Astronest.png')
        if os.path.exists(icon_path):
            try:
                img = tk.PhotoImage(file=icon_path)
                self.iconphoto(False, img)
            except Exception as e:
                print("Could not set icon:", e)
        
        self.gamification = GamificationManager(self)
        self.quiz_manager = QuizManager()
        
        self.current_quiz_questions = []
        self.current_score = 0
        self.current_category = "All Categories"
        
        # Grid layout (Sidebar + Main)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#1a1a2e")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        
        if os.path.exists(icon_path):
            logo_img = ctk.CTkImage(Image.open(icon_path), size=(120, 120))
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="", image=logo_img)
            self.logo_label.grid(row=0, column=0, padx=20, pady=(40, 10))
            
        self.logo_text = ctk.CTkLabel(self.sidebar_frame, text="Eclipse Explorer", font=ctk.CTkFont(size=20, weight="bold"), text_color="#ffb74d")
        self.logo_text.grid(row=1, column=0, padx=20, pady=(0, 40))
        
        # Navigation Buttons
        self.nav_buttons = []
        
        self.btn_nav_sim = ctk.CTkButton(self.sidebar_frame, text="☀ Simulator", font=ctk.CTkFont(size=16, weight="bold"), height=50, fg_color="transparent", text_color="gray90", hover_color="#2a2a4e", anchor="w", command=lambda: self.show_frame("simulator"))
        self.btn_nav_sim.grid(row=2, column=0, pady=5, padx=20, sticky="ew")
        self.nav_buttons.append(self.btn_nav_sim)

        self.btn_nav_quiz = ctk.CTkButton(self.sidebar_frame, text="❓ Quizzes", font=ctk.CTkFont(size=16, weight="bold"), height=50, fg_color="transparent", text_color="gray90", hover_color="#2a2a4e", anchor="w", command=lambda: self.show_frame("quiz_setup"))
        self.btn_nav_quiz.grid(row=3, column=0, pady=5, padx=20, sticky="ew")
        self.nav_buttons.append(self.btn_nav_quiz)

        self.btn_nav_glossary = ctk.CTkButton(self.sidebar_frame, text="📖 Glossary", font=ctk.CTkFont(size=16, weight="bold"), height=50, fg_color="transparent", text_color="gray90", hover_color="#2a2a4e", anchor="w", command=lambda: self.show_frame("glossary"))
        self.btn_nav_glossary.grid(row=4, column=0, pady=5, padx=20, sticky="ew")
        self.nav_buttons.append(self.btn_nav_glossary)

        self.btn_nav_profile = ctk.CTkButton(self.sidebar_frame, text="🏆 Profile", font=ctk.CTkFont(size=16, weight="bold"), height=50, fg_color="transparent", text_color="gray90", hover_color="#2a2a4e", anchor="w", command=lambda: self.show_frame("profile"))
        self.btn_nav_profile.grid(row=5, column=0, pady=5, padx=20, sticky="ew")
        self.nav_buttons.append(self.btn_nav_profile)
        
        # Contact button at the bottom
        self.btn_nav_contact = ctk.CTkButton(self.sidebar_frame, text="✉ Support", font=ctk.CTkFont(size=14), height=40, fg_color="transparent", hover_color="#f44336", text_color="#f44336", command=self.contact_creators)
        self.btn_nav_contact.grid(row=7, column=0, pady=20, padx=20, sticky="ew")
        
        # --- Main Area ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        self.frames["simulator"] = SimulatorFrame(self.main_frame, self)
        self.frames["quiz_setup"] = QuizSetupFrame(self.main_frame, self)
        self.frames["quiz"] = QuizFrame(self.main_frame, self)
        self.frames["result"] = ResultFrame(self.main_frame, self)
        self.frames["profile"] = ProfileFrame(self.main_frame, self)
        self.frames["glossary"] = GlossaryFrame(self.main_frame, self)
        
        self.show_frame("simulator")
        
    def select_nav_button(self, name):
        for btn in self.nav_buttons:
            btn.configure(fg_color="transparent")
        if name == "simulator":
            self.btn_nav_sim.configure(fg_color="#4a148c")
        elif name == "quiz_setup":
            self.btn_nav_quiz.configure(fg_color="#4a148c")
        elif name == "glossary":
            self.btn_nav_glossary.configure(fg_color="#4a148c")
        elif name == "profile":
            self.btn_nav_profile.configure(fg_color="#4a148c")

    def show_frame(self, name):
        # Update styling
        if name in ["simulator", "quiz_setup", "glossary", "profile"]:
            self.select_nav_button(name)
            
        for frame in self.frames.values():
            frame.grid_forget()
            
        if name == "profile":
            self.frames["profile"].update_view()
        elif name == "quiz_setup":
            self.frames["quiz_setup"].update_view()
        elif name == "glossary":
            self.gamification.award_badge("Encyclopedia Worm")
            
        self.frames[name].grid(row=0, column=0, sticky="nsew")
        
    def start_quiz(self, category, count):
        self.current_category = category
        self.current_quiz_questions = self.quiz_manager.setup_quiz(category, count)
        if not self.current_quiz_questions:
            return
        self.frames["quiz"].start(self.current_quiz_questions)
        self.show_frame("quiz")
        
    def contact_creators(self):
        import webbrowser
        email = "amineaithamma2004@gmail.com"
        subject = "Raise a technical request"
        webbrowser.open(f"mailto:{email}?subject={subject}")
