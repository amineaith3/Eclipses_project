import customtkinter as ctk

class QuizSetupFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=15)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(self, text="Quiz Setup", font=ctk.CTkFont(size=36, weight="bold"))
        title.grid(row=0, column=0, pady=(60, 20))
        
        sub = ctk.CTkLabel(self, text="Customize your learning experience.", font=ctk.CTkFont(size=18), text_color="gray")
        sub.grid(row=1, column=0, pady=(0, 40))

        # Category
        cat_lbl = ctk.CTkLabel(self, text="Select Category:", font=ctk.CTkFont(size=18))
        cat_lbl.grid(row=2, column=0, pady=(10, 5))
        
        self.cat_var = ctk.StringVar(value="All / Random")
        self.cat_menu = ctk.CTkOptionMenu(self, variable=self.cat_var, values=["All / Random"], font=ctk.CTkFont(size=16), height=40, width=300)
        self.cat_menu.grid(row=3, column=0, pady=(0, 20))

        # Number of Questions
        count_lbl = ctk.CTkLabel(self, text="Number of Questions:", font=ctk.CTkFont(size=18))
        count_lbl.grid(row=4, column=0, pady=(10, 5))
        
        self.count_var = ctk.StringVar(value="10")
        self.count_menu = ctk.CTkOptionMenu(self, variable=self.count_var, values=["5", "10", "20", "50", "All"], font=ctk.CTkFont(size=16), height=40, width=300)
        self.count_menu.grid(row=5, column=0, pady=(0, 40))
        
        badge_hint = ctk.CTkLabel(self, text="💡 Tip: Play quizzes with 20+ questions to earn high-tier badges!", text_color="#ffb74d")
        badge_hint.grid(row=6, column=0, pady=(0, 20))

        # Start
        btn_start = ctk.CTkButton(self, text="Start Quiz", font=ctk.CTkFont(size=20, weight="bold"), height=60, fg_color="#4a148c", hover_color="#6a1b9a", command=self.start)
        btn_start.grid(row=7, column=0, pady=(20, 10))

    def update_view(self):
        cats = self.controller.quiz_manager.get_categories()
        self.cat_menu.configure(values=cats)

    def start(self):
        cat = self.cat_var.get()
        count = self.count_var.get()
        self.controller.start_quiz(cat, count)
