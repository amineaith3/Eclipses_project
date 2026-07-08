# Eclipse Explorer Q&A Pro 🌑☀

Welcome to **Eclipse Explorer Q&A Pro** – a highly educational, fully modular Python desktop application dedicated to the wonders of solar and lunar eclipses! 

This project has been extensively overhauled from a simple Pygame prototype into a professional-grade CustomTkinter desktop application, complete with accurate astrophysics simulations and deep gamification mechanics.

## ✨ Key Features

* **Interactive 2D Simulators:** 
  * *Earth View:* Drag the moon to manually simulate a solar transit, complete with dynamic educational facts about Baily's Beads, Totality, and the Corona.
  * *Space View:* Watch the Moon orbit the Earth along a mathematically accurate elliptical path, casting Umbra and Penumbra shadow cones dynamically.
* **Massive Factual Database:** Contains exactly 150 hand-crafted, scientifically and historically accurate trivia questions.
* **Categorized Quizzes:** Before starting a quiz, customize your session by selecting categories (Solar, Lunar, Astrophysics, History, or General) and adjusting the question count (5, 10, 20, 50, or All).
* **Adaptive Learning:** A strict 40-second timer keeps you on your toes! If you answer incorrectly or run out of time, an adaptive "Mini-Lesson" popup appears to explain the concept.
* **Deep Gamification:** Unlocks persist globally on your machine (saving to Windows `%APPDATA%`). Play 20+ question quizzes to unlock exclusive high-tier badges:
  * 🥉 *Novice Eclipse Chaser*
  * 🥈 *Silver Corona* (80%+)
  * 🥇 *Golden Umbra* (90%+)
  * 💎 *Diamond Ring Master* (100% Flawless)

## 🛠 Tech Stack

* **Language:** Python 3
* **GUI Framework:** `CustomTkinter` (Modern Dark-Mode UI)
* **Graphics:** Native Tkinter Canvas for 2D Astrophysics Simulations
* **Data Persistence:** Local JSON saving to Windows `%APPDATA%`
* **Architecture:** Modular `src/` component structure (Core Logic vs. UI Frames)

## 🚀 How to Run

1. Make sure you have Python installed.
2. Install the required UI library:
   ```bash
   pip install customtkinter
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## 🎥 Original Educational Video
If you want to view the original educational video that inspired this project, you can watch it here:
[Link to the Video](https://drive.google.com/file/d/1X5XwW19XvjC5gL_yA3Z88uQ-D-X7T-e0/view?usp=sharing)
