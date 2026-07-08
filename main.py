import customtkinter as ctk
import tkinter as tk
import json
import random
import webbrowser

# Setup CustomTkinter Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EclipseApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Eclipse Explorer Q&A")
        self.geometry("900x700")
        self.resizable(False, False)

        # App State
        self.quiz_data = []
        self.selected_questions = []
        self.current_q_index = 0
        self.score = 0
        self.simulation_completed = False

        self.load_data()

        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Initialize Frames
        self.frames = {}
        
        self.setup_menu_frame()
        self.setup_quiz_frame()
        self.setup_result_frame()
        self.setup_simulator_frame()

        self.show_frame("menu")

    def load_data(self):
        try:
            with open("eclipse_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quiz_data = data.get("questions", [])
        except Exception as e:
            print("Error loading eclipse_data.json:", e)

    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[frame_name].grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    # --- MENU FRAME ---
    def setup_menu_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        self.frames["menu"] = frame
        
        frame.grid_columnconfigure(0, weight=1)
        
        # Logo/Title
        title_lbl = ctk.CTkLabel(frame, text="Eclipse Explorer", font=ctk.CTkFont(size=42, weight="bold"))
        title_lbl.grid(row=0, column=0, pady=(60, 10))

        sub_lbl = ctk.CTkLabel(frame, text="Discover the mysteries of the sun and moon.", font=ctk.CTkFont(size=18), text_color="gray")
        sub_lbl.grid(row=1, column=0, pady=(0, 50))

        # Buttons
        self.btn_sim = ctk.CTkButton(frame, text="☀ Interactive Simulator", font=ctk.CTkFont(size=18), height=50, command=lambda: self.show_frame("simulator"))
        self.btn_sim.grid(row=2, column=0, pady=10)

        self.btn_quiz = ctk.CTkButton(frame, text="❓ Take the Quiz", font=ctk.CTkFont(size=18), height=50, command=self.start_quiz, state="disabled")
        self.btn_quiz.grid(row=3, column=0, pady=10)

        self.btn_contact = ctk.CTkButton(frame, text="✉ Contact Creators", font=ctk.CTkFont(size=18), height=50, fg_color="transparent", border_width=2, command=self.contact_creators)
        self.btn_contact.grid(row=4, column=0, pady=10)
        
        self.sim_status_lbl = ctk.CTkLabel(frame, text="Complete the simulation to unlock the quiz!", text_color="#ffb74d")
        self.sim_status_lbl.grid(row=5, column=0, pady=20)

    def unlock_quiz(self):
        self.simulation_completed = True
        self.sim_status_lbl.configure(text="Simulation completed! Quiz unlocked.", text_color="#4caf50")
        self.btn_quiz.configure(state="normal")

    def contact_creators(self):
        email = "amineaithamma2004@gmail.com"
        subject = "Raise a technical request"
        webbrowser.open(f"mailto:{email}?subject={subject}")

    # --- SIMULATOR FRAME ---
    def setup_simulator_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        self.frames["simulator"] = frame
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(frame, text="Solar Eclipse Simulator", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, pady=20)

        # Canvas for drawing
        self.canvas_width = 800
        self.canvas_height = 300
        self.canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg="#000000", highlightthickness=0)
        self.canvas.grid(row=1, column=0, pady=10)

        # Draw Sun (stationary in center)
        self.sun_radius = 80
        sun_x = self.canvas_width // 2
        sun_y = self.canvas_height // 2
        
        # Add a glow effect
        self.canvas.create_oval(sun_x - 100, sun_y - 100, sun_x + 100, sun_y + 100, fill="#331a00", outline="")
        self.canvas.create_oval(sun_x - 90, sun_y - 90, sun_x + 90, sun_y + 90, fill="#663300", outline="")
        
        self.sun = self.canvas.create_oval(sun_x - self.sun_radius, sun_y - self.sun_radius, 
                                           sun_x + self.sun_radius, sun_y + self.sun_radius, 
                                           fill="#ffcc00", outline="#ff9900", width=2)
                                           
        # Draw Moon (moves)
        self.moon_radius = 78 # slightly smaller to allow corona/baily's beads effect visualization
        self.moon_start_x = 100
        self.moon = self.canvas.create_oval(self.moon_start_x - self.moon_radius, sun_y - self.moon_radius, 
                                            self.moon_start_x + self.moon_radius, sun_y + self.moon_radius, 
                                            fill="#1a1a1a", outline="#0a0a0a", width=2)

        # Info Box
        self.info_lbl = ctk.CTkLabel(frame, text="Drag the slider to move the Moon.", font=ctk.CTkFont(size=18), wraplength=700)
        self.info_lbl.grid(row=2, column=0, pady=10)

        # Controls
        controls_frame = ctk.CTkFrame(frame, fg_color="transparent")
        controls_frame.grid(row=3, column=0, pady=20, sticky="ew", padx=50)
        controls_frame.grid_columnconfigure(1, weight=1)

        self.slider = ctk.CTkSlider(controls_frame, from_=100, to=700, command=self.update_simulation)
        self.slider.set(100)
        self.slider.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))

        btn_auto = ctk.CTkButton(controls_frame, text="Auto-Play", command=self.auto_play_sim)
        btn_auto.grid(row=1, column=0, sticky="w")

        btn_back = ctk.CTkButton(controls_frame, text="Back to Menu", fg_color="transparent", border_width=2, command=self.exit_simulator)
        btn_back.grid(row=1, column=2, sticky="e")
        
        self.auto_playing = False

    def update_simulation(self, value):
        moon_x = float(value)
        sun_y = self.canvas_height // 2
        
        # Move the moon
        self.canvas.coords(self.moon, moon_x - self.moon_radius, sun_y - self.moon_radius,
                                      moon_x + self.moon_radius, sun_y + self.moon_radius)
                                      
        # Update Info Text based on position
        center_x = self.canvas_width // 2
        distance = abs(moon_x - center_x)
        
        if distance < 10:
            info = ("TOTAL ECLIPSE (Totality):\n"
                    "The Moon completely covers the Sun. The Sun's delicate outer atmosphere, "
                    "the corona, becomes visible as a pearly white halo.")
        elif distance < self.sun_radius + 15 and distance >= 10:
            info = ("BAILY'S BEADS / DIAMOND RING:\n"
                    "Just before or after totality, sunlight shines through the rugged lunar valleys "
                    "creating bright spots (Baily's Beads) and a brilliant 'Diamond Ring' effect.")
        elif distance < self.sun_radius * 2:
            info = ("PARTIAL ECLIPSE:\n"
                    "The Moon is partially obscuring the Sun. It looks like a bite has been taken "
                    "out of the Sun. Always use protective eyewear!")
        else:
            info = ("NO ECLIPSE:\n"
                    "The Moon and Sun are not aligned. Drag the slider to begin the transit.")
                    
        self.info_lbl.configure(text=info)

    def auto_play_sim(self):
        if self.auto_playing:
            return
            
        self.auto_playing = True
        self.slider.set(100)
        self.animate_sim()

    def animate_sim(self):
        if not self.auto_playing:
            return
            
        current = self.slider.get()
        if current < 700:
            next_val = current + 2
            self.slider.set(next_val)
            self.update_simulation(next_val)
            self.after(20, self.animate_sim)
        else:
            self.auto_playing = False

    def exit_simulator(self):
        self.auto_playing = False
        self.unlock_quiz()
        self.show_frame("menu")

    # --- QUIZ FRAME ---
    def setup_quiz_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        self.frames["quiz"] = frame
        frame.grid_columnconfigure(0, weight=1)

        # Header: Progress
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(header_frame, height=10)
        self.progress_bar.grid(row=0, column=0, sticky="ew", padx=(0, 20))
        self.progress_bar.set(0)

        self.lbl_progress = ctk.CTkLabel(header_frame, text="1/15", font=ctk.CTkFont(weight="bold"))
        self.lbl_progress.grid(row=0, column=1)

        # Question
        self.lbl_question = ctk.CTkLabel(frame, text="Question text goes here", font=ctk.CTkFont(size=22, weight="bold"), wraplength=700)
        self.lbl_question.grid(row=1, column=0, pady=(40, 40), padx=20)

        # Choices
        self.choice_buttons = []
        for i in range(3):
            btn = ctk.CTkButton(frame, text=f"Choice {i+1}", font=ctk.CTkFont(size=16), height=60, 
                                anchor="w", fg_color="#2b2b2b", hover_color="#3b3b3b",
                                command=lambda idx=i: self.select_answer(idx))
            btn.grid(row=2+i, column=0, sticky="ew", padx=50, pady=10)
            self.choice_buttons.append(btn)

        # Feedback & Next
        footer_frame = ctk.CTkFrame(frame, fg_color="transparent")
        footer_frame.grid(row=6, column=0, sticky="ew", padx=50, pady=40)
        footer_frame.grid_columnconfigure(0, weight=1)

        self.lbl_feedback = ctk.CTkLabel(footer_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_feedback.grid(row=0, column=0, sticky="w")

        self.btn_next = ctk.CTkButton(footer_frame, text="Next Question →", font=ctk.CTkFont(weight="bold"), 
                                      command=self.next_question)
        self.btn_next.grid(row=0, column=1, sticky="e")
        self.btn_next.grid_remove()

    def start_quiz(self):
        if not self.quiz_data:
            return

        self.score = 0
        self.current_q_index = 0
        
        # Shuffle and select 15
        shuffled = random.sample(self.quiz_data, min(15, len(self.quiz_data)))
        self.selected_questions = shuffled
        
        self.show_frame("quiz")
        self.load_question()

    def load_question(self):
        self.lbl_feedback.configure(text="")
        self.btn_next.grid_remove()

        q_data = self.selected_questions[self.current_q_index]
        self.lbl_question.configure(text=f"{self.current_q_index + 1}. {q_data['question']}")
        self.lbl_progress.configure(text=f"{self.current_q_index + 1}/{len(self.selected_questions)}")
        
        progress_val = (self.current_q_index) / len(self.selected_questions)
        self.progress_bar.set(progress_val)

        choices = q_data["choices"].copy()
        random.shuffle(choices)
        self.current_correct_answer = q_data["correct_answer"]
        self.current_choices = choices

        for i, btn in enumerate(self.choice_buttons):
            if i < len(choices):
                btn.configure(text=choices[i], state="normal", fg_color="#2b2b2b")
                btn.grid()
            else:
                btn.grid_remove()

    def select_answer(self, choice_idx):
        selected_text = self.current_choices[choice_idx]
        is_correct = (selected_text == self.current_correct_answer)

        if is_correct:
            self.score += 1
            self.choice_buttons[choice_idx].configure(fg_color="#4caf50")
            self.lbl_feedback.configure(text="Correct!", text_color="#4caf50")
        else:
            self.choice_buttons[choice_idx].configure(fg_color="#f44336")
            self.lbl_feedback.configure(text="Incorrect!", text_color="#f44336")
            
            for i, text in enumerate(self.current_choices):
                if text == self.current_correct_answer:
                    self.choice_buttons[i].configure(fg_color="#4caf50")

        for btn in self.choice_buttons:
            btn.configure(state="disabled")

        self.btn_next.grid()

    def next_question(self):
        self.current_q_index += 1
        if self.current_q_index < len(self.selected_questions):
            self.load_question()
        else:
            self.show_results()

    # --- RESULT FRAME ---
    def setup_result_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        self.frames["result"] = frame
        frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(frame, text="Quiz Completed!", font=ctk.CTkFont(size=36, weight="bold"))
        title.grid(row=0, column=0, pady=(80, 20))

        self.lbl_score = ctk.CTkLabel(frame, text="Score: 0/15", font=ctk.CTkFont(size=48, weight="bold"), text_color="#ffb74d")
        self.lbl_score.grid(row=1, column=0, pady=20)

        self.lbl_msg = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=20))
        self.lbl_msg.grid(row=2, column=0, pady=20)

        self.btn_restart = ctk.CTkButton(frame, text="Try Again", font=ctk.CTkFont(size=18), height=50, command=self.start_quiz)
        self.btn_restart.grid(row=3, column=0, pady=10)

        self.btn_home = ctk.CTkButton(frame, text="Back to Menu", font=ctk.CTkFont(size=18), height=50, fg_color="transparent", border_width=2, command=lambda: self.show_frame("menu"))
        self.btn_home.grid(row=4, column=0, pady=10)

    def show_results(self):
        self.progress_bar.set(1.0)
        self.show_frame("result")
        total = len(self.selected_questions)
        self.lbl_score.configure(text=f"Score: {self.score}/{total}")
        
        pct = self.score / total
        if pct >= 0.8:
            msg = "Excellent! You are an eclipse expert."
        elif pct >= 0.5:
            msg = "Good job! But there's more to learn."
        else:
            msg = "Keep exploring to learn more about eclipses!"
        self.lbl_msg.configure(text=msg)

if __name__ == "__main__":
    app = EclipseApp()
    app.mainloop()
