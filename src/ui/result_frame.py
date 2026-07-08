import customtkinter as ctk

class ResultFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=15)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="Quiz Completed!", font=ctk.CTkFont(size=36, weight="bold"))
        title.grid(row=0, column=0, pady=(80, 20))

        self.lbl_score = ctk.CTkLabel(self, text="Score: 0/15", font=ctk.CTkFont(size=48, weight="bold"), text_color="#ffb74d")
        self.lbl_score.grid(row=1, column=0, pady=20)

        self.lbl_msg = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=20))
        self.lbl_msg.grid(row=2, column=0, pady=20)
        
        self.lbl_badges = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16, weight="bold"), text_color="#4caf50")
        self.lbl_badges.grid(row=3, column=0, pady=10)

        btn_restart = ctk.CTkButton(self, text="Play Again", font=ctk.CTkFont(size=18), height=50, command=lambda: self.controller.show_frame("quiz_setup"))
        btn_restart.grid(row=4, column=0, pady=20)

        btn_home = ctk.CTkButton(self, text="Back to Menu", font=ctk.CTkFont(size=18), height=50, fg_color="transparent", border_width=2, command=lambda: self.controller.show_frame("menu"))
        btn_home.grid(row=5, column=0, pady=10)
        
    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.update_results()

    def update_results(self):
        score = self.controller.current_score
        total = len(self.controller.current_quiz_questions)
        self.lbl_score.configure(text=f"Score: {score}/{total}")
        
        pct = score / total if total > 0 else 0
        if pct == 1.0:
            msg = "Flawless! You are a true master."
        elif pct >= 0.8:
            msg = "Excellent work!"
        elif pct >= 0.5:
            msg = "Good job! Keep exploring."
        else:
            msg = "Keep exploring to learn more about eclipses!"
        self.lbl_msg.configure(text=msg)
        
        self.controller.gamification.evaluate_quiz_badges(score, total)
