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

        btn_restart = ctk.CTkButton(self, text="Play Again", font=ctk.CTkFont(size=18), height=50, fg_color="#4a148c", hover_color="#6a1b9a", command=lambda: self.controller.show_frame("quiz_setup"))
        btn_restart.grid(row=4, column=0, pady=20)
        
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
        self.controller.gamification.evaluate_quiz_badges(score, total, self.controller.current_category)
        
        if pct == 1.0 and total >= 20:
            # Short delay to allow the frame to render before popping the dialog
            self.after(500, self.trigger_certificate)

    def trigger_certificate(self):
        dialog = ctk.CTkInputDialog(text="Congratulations on Diamond Ring Master!\nEnter your name for your official Certificate:", title="Certificate Generation")
        name = dialog.get_input()
        if name:
            from src.core.certificate import CertificateGenerator
            path = CertificateGenerator.generate(name)
            if path:
                self.lbl_badges.configure(text=f"✅ Certificate saved to your Desktop!", text_color="#4caf50")
