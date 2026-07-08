import customtkinter as ctk
import webbrowser

class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=15)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        
        title_lbl = ctk.CTkLabel(self, text="Eclipse Explorer", font=ctk.CTkFont(size=42, weight="bold"))
        title_lbl.grid(row=0, column=0, pady=(60, 10))

        sub_lbl = ctk.CTkLabel(self, text="Discover the mysteries of the sun and moon.", font=ctk.CTkFont(size=18), text_color="gray")
        sub_lbl.grid(row=1, column=0, pady=(0, 40))

        self.btn_sim = ctk.CTkButton(self, text="☀ Interactive Simulator", font=ctk.CTkFont(size=18), height=50, command=lambda: self.controller.show_frame("simulator"))
        self.btn_sim.grid(row=2, column=0, pady=10)

        self.btn_quiz = ctk.CTkButton(self, text="❓ Take the Quiz", font=ctk.CTkFont(size=18), height=50, command=lambda: self.controller.show_frame("quiz_setup"), state="disabled")
        self.btn_quiz.grid(row=3, column=0, pady=10)

        self.btn_profile = ctk.CTkButton(self, text="🏆 My Profile & Badges", font=ctk.CTkFont(size=18), height=50, fg_color="#4a148c", hover_color="#6a1b9a", command=lambda: self.controller.show_frame("profile"))
        self.btn_profile.grid(row=4, column=0, pady=10)

        self.btn_contact = ctk.CTkButton(self, text="✉ Contact Creators", font=ctk.CTkFont(size=18), height=50, fg_color="transparent", border_width=2, command=self.contact_creators)
        self.btn_contact.grid(row=5, column=0, pady=10)
        
        self.sim_status_lbl = ctk.CTkLabel(self, text="Complete the simulation to unlock the quiz!", text_color="#ffb74d")
        self.sim_status_lbl.grid(row=6, column=0, pady=20)
        
    def update_view(self):
        user_data = self.controller.gamification.user_data
        if user_data.get("simulations_watched", 0) > 0:
            self.btn_quiz.configure(state="normal")
            self.sim_status_lbl.configure(text="Quiz Unlocked!", text_color="#4caf50")
        else:
            self.btn_quiz.configure(state="disabled")
            self.sim_status_lbl.configure(text="Complete the simulation to unlock the quiz!", text_color="#ffb74d")

    def contact_creators(self):
        email = "amineaithamma2004@gmail.com"
        subject = "Raise a technical request"
        webbrowser.open(f"mailto:{email}?subject={subject}")
