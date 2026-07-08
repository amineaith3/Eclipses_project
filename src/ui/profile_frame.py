import customtkinter as ctk

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=15)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(self, text="My Profile & Badges", font=ctk.CTkFont(size=32, weight="bold"))
        title.grid(row=0, column=0, pady=(40, 20))
        
        self.stats_lbl = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=18))
        self.stats_lbl.grid(row=1, column=0, pady=10)
        
        self.badges_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.badges_frame.grid(row=2, column=0, pady=20, padx=50, sticky="ew")
        
        btn_reset = ctk.CTkButton(self, text="Reset Account", font=ctk.CTkFont(size=14), fg_color="#f44336", hover_color="#d32f2f", command=self.reset_account)
        btn_reset.grid(row=3, column=0, pady=(40, 10))
        
        btn_back = ctk.CTkButton(self, text="Back to Menu", font=ctk.CTkFont(size=18), height=50, fg_color="transparent", border_width=2, command=lambda: self.controller.show_frame("menu"))
        btn_back.grid(row=4, column=0, pady=10)

    def reset_account(self):
        self.controller.gamification.reset_account()
        self.controller.current_quiz_questions = []
        self.controller.current_score = 0
        self.update_view()

    def update_view(self):
        udata = self.controller.gamification.user_data
        self.stats_lbl.configure(text=f"Quizzes Taken: {udata['quizzes_taken']}  |  Simulations Watched: {udata['simulations_watched']}")
        
        for widget in self.badges_frame.winfo_children():
            widget.destroy()
            
        all_badges = {
            "Astronomer": "Complete the Eclipse Simulation.",
            "Scholar": "Complete your first quiz.",
            "Speed Demon": "Answer a question correctly in under 5 seconds.",
            "Novice Eclipse Chaser": "Complete a 20+ question quiz.",
            "Silver Corona": "Score 80%+ on a 20+ question quiz.",
            "Golden Umbra": "Score 90%+ on a 20+ question quiz.",
            "Diamond Ring Master": "Score 100% on a 20+ question quiz."
        }
        
        row = 0
        col = 0
        for b_name, b_desc in all_badges.items():
            unlocked = b_name in udata["badges"]
            color = "#ffb74d" if unlocked else "#555555"
            icon = "🏆" if unlocked else "🔒"
            
            b_frame = ctk.CTkFrame(self.badges_frame, border_color=color, border_width=2, corner_radius=10)
            b_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            ctk.CTkLabel(b_frame, text=f"{icon} {b_name}", font=ctk.CTkFont(size=16, weight="bold"), text_color=color).pack(pady=(10, 5), padx=20)
            ctk.CTkLabel(b_frame, text=b_desc, wraplength=180, text_color="gray").pack(pady=(0, 10), padx=20)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
