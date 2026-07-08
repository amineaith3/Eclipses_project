import customtkinter as ctk
import random

class QuizFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=15)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        # Header: Timer & Progress
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(1, weight=1)

        self.lbl_timer = ctk.CTkLabel(header_frame, text="⏱ 40s", font=ctk.CTkFont(weight="bold", size=24), text_color="#ffb74d")
        self.lbl_timer.grid(row=0, column=0, padx=20)

        self.progress_bar = ctk.CTkProgressBar(header_frame, height=10)
        self.progress_bar.grid(row=0, column=1, sticky="ew", padx=20)
        self.progress_bar.set(0)

        self.lbl_progress = ctk.CTkLabel(header_frame, text="1/1", font=ctk.CTkFont(weight="bold"))
        self.lbl_progress.grid(row=0, column=2, padx=20)

        # Question
        self.lbl_question = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=22, weight="bold"), wraplength=800)
        self.lbl_question.grid(row=1, column=0, pady=(40, 40), padx=20)

        # Choices
        self.choice_buttons = []
        for i in range(4): # Assuming max 4 choices
            btn = ctk.CTkButton(self, text=f"Choice {i+1}", font=ctk.CTkFont(size=16), height=60, 
                                anchor="w", fg_color="#2b2b2b", hover_color="#3b3b3b",
                                command=lambda idx=i: self.select_answer(idx))
            btn.grid(row=2+i, column=0, sticky="ew", padx=50, pady=10)
            self.choice_buttons.append(btn)

        # Footer
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=6, column=0, sticky="ew", padx=50, pady=40)
        footer_frame.grid_columnconfigure(0, weight=1)

        self.lbl_feedback = ctk.CTkLabel(footer_frame, text="", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_feedback.grid(row=0, column=0, sticky="w")

        self.btn_next = ctk.CTkButton(footer_frame, text="Next Question →", font=ctk.CTkFont(weight="bold"), 
                                      command=self.next_question)
        self.btn_next.grid(row=0, column=1, sticky="e")
        self.btn_next.grid_remove()

        self.questions = []
        self.current_q_index = 0
        self.score = 0
        self.time_left = 40
        self.timer_id = None
        self.current_q_time_taken = 0

    def start(self, questions):
        self.questions = questions
        self.current_q_index = 0
        self.score = 0
        self.load_question()

    def load_question(self):
        self.lbl_feedback.configure(text="")
        self.btn_next.grid_remove()

        q_data = self.questions[self.current_q_index]
        self.lbl_question.configure(text=f"{self.current_q_index + 1}. {q_data['question']}")
        self.lbl_progress.configure(text=f"{self.current_q_index + 1}/{len(self.questions)}")
        
        progress_val = (self.current_q_index) / len(self.questions)
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
                
        # Timer
        self.time_left = 40
        self.current_q_time_taken = 0
        self.lbl_timer.configure(text=f"⏱ {self.time_left}s", text_color="#ffb74d")
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.current_q_time_taken += 1
            
            color = "#ffb74d" if self.time_left > 10 else "#f44336"
            self.lbl_timer.configure(text=f"⏱ {self.time_left}s", text_color=color)
            self.timer_id = self.after(1000, self.update_timer)
        else:
            self.handle_timeout()

    def handle_timeout(self):
        self.lbl_feedback.configure(text="Time's Up!", text_color="#f44336")
        for i, text in enumerate(self.current_choices):
            if text == self.current_correct_answer:
                self.choice_buttons[i].configure(fg_color="#4caf50")
        self.disable_choices()
        self.show_adaptive_lesson()

    def select_answer(self, choice_idx):
        if self.timer_id:
            self.after_cancel(self.timer_id)
            
        selected_text = self.current_choices[choice_idx]
        is_correct = (selected_text == self.current_correct_answer)

        if is_correct:
            self.score += 1
            self.choice_buttons[choice_idx].configure(fg_color="#4caf50")
            self.lbl_feedback.configure(text="Correct!", text_color="#4caf50")
            
            if self.current_q_time_taken < 5:
                self.controller.gamification.award_badge("Speed Demon")
                
        else:
            self.choice_buttons[choice_idx].configure(fg_color="#f44336")
            self.lbl_feedback.configure(text="Incorrect!", text_color="#f44336")
            for i, text in enumerate(self.current_choices):
                if text == self.current_correct_answer:
                    self.choice_buttons[i].configure(fg_color="#4caf50")
            self.show_adaptive_lesson()

        self.disable_choices()
        self.btn_next.grid()

    def disable_choices(self):
        for btn in self.choice_buttons:
            btn.configure(state="disabled")

    def show_adaptive_lesson(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Adaptive Learning: Mini-Lesson")
        popup.geometry("600x400")
        popup.attributes("-topmost", True)
        
        lbl = ctk.CTkLabel(popup, text="Let's Review That Concept 🧠", font=ctk.CTkFont(size=22, weight="bold"))
        lbl.pack(pady=20)
        
        text = ctk.CTkLabel(popup, text=self.current_correct_answer, font=ctk.CTkFont(size=16), wraplength=550, justify="left")
        text.pack(padx=20, pady=10)
        
        btn = ctk.CTkButton(popup, text="Got it!", command=popup.destroy)
        btn.pack(pady=20)

    def next_question(self):
        self.current_q_index += 1
        if self.current_q_index < len(self.questions):
            self.load_question()
        else:
            self.controller.current_score = self.score
            self.controller.show_frame("result")
