import customtkinter as ctk
import tkinter as tk
import math

class SimulatorFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=15)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        title = ctk.CTkLabel(self, text="Solar Eclipse Simulator", font=ctk.CTkFont(size=28, weight="bold"))
        title.grid(row=0, column=0, pady=10)
        
        self.sim_view_var = ctk.StringVar(value="Earth View")
        self.seg_btn = ctk.CTkSegmentedButton(self, values=["Earth View", "Space View"], variable=self.sim_view_var, command=self.change_sim_view)
        self.seg_btn.grid(row=1, column=0, pady=10)

        self.canvas_width = 800
        self.canvas_height = 300
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="#000000", highlightthickness=0)
        self.canvas.grid(row=2, column=0, pady=10)

        self.info_lbl = ctk.CTkLabel(self, text="Drag the slider to move the Moon.", font=ctk.CTkFont(size=18), wraplength=800, height=120, justify="center")
        self.info_lbl.grid(row=3, column=0, pady=10)

        controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        controls_frame.grid(row=4, column=0, pady=20, sticky="ew", padx=50)
        controls_frame.grid_columnconfigure(1, weight=1)

        self.slider = ctk.CTkSlider(controls_frame, from_=0, to=800, command=self.update_simulation)
        self.slider.set(100)
        self.slider.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))

        btn_auto = ctk.CTkButton(controls_frame, text="Auto-Play", command=self.auto_play_sim)
        btn_auto.grid(row=1, column=0, sticky="w")

        btn_back = ctk.CTkButton(controls_frame, text="Back to Menu", fg_color="transparent", border_width=2, command=self.exit_simulator)
        btn_back.grid(row=1, column=2, sticky="e")
        
        self.auto_playing = False
        self.draw_earth_view()

    def change_sim_view(self, value):
        self.canvas.delete("all")
        self.slider.set(100)
        if value == "Earth View":
            self.draw_earth_view()
        else:
            self.draw_space_view()
        self.update_simulation(100)

    def draw_earth_view(self):
        sun_x, sun_y = self.canvas_width // 2, self.canvas_height // 2
        self.sun_radius = 80
        
        self.canvas.create_oval(sun_x - 100, sun_y - 100, sun_x + 100, sun_y + 100, fill="#331a00", outline="", tags="sun_glow2")
        self.canvas.create_oval(sun_x - 90, sun_y - 90, sun_x + 90, sun_y + 90, fill="#663300", outline="", tags="sun_glow1")
        self.canvas.create_oval(sun_x - self.sun_radius, sun_y - self.sun_radius, 
                                sun_x + self.sun_radius, sun_y + self.sun_radius, 
                                fill="#ffcc00", outline="#ff9900", width=2, tags="sun")
                                           
        self.moon_radius = 78
        self.moon_start_x = 100
        self.canvas.create_oval(self.moon_start_x - self.moon_radius, sun_y - self.moon_radius, 
                                self.moon_start_x + self.moon_radius, sun_y + self.moon_radius, 
                                fill="#1a1a1a", outline="#0a0a0a", width=2, tags="moon")

    def draw_space_view(self):
        sun_x, sun_y = -50, self.canvas_height // 2
        sun_r = 150
        self.canvas.create_oval(sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r, fill="#ffcc00", outline="", tags="space_sun")
        
        earth_x, earth_y = 650, self.canvas_height // 2
        earth_r = 40
        self.canvas.create_oval(earth_x - earth_r, earth_y - earth_r, earth_x + earth_r, earth_y + earth_r, fill="#1976d2", outline="#0d47a1", tags="space_earth")
        
        self.canvas.create_polygon(0,0,0,0,0,0, fill="", tags="penumbra")
        self.canvas.create_polygon(0,0,0,0,0,0, fill="", tags="umbra")
        
        self.space_moon_r = 15
        moon_x = 350
        self.canvas.create_oval(moon_x - self.space_moon_r, sun_y - self.space_moon_r, 
                                moon_x + self.space_moon_r, sun_y + self.space_moon_r, 
                                fill="#888888", outline="#555555", tags="space_moon")

    def update_simulation(self, value):
        moon_x = float(value)
        sun_y = self.canvas_height // 2
        view = self.sim_view_var.get()
        
        if view == "Earth View":
            self.canvas.coords("moon", moon_x - self.moon_radius, sun_y - self.moon_radius,
                                          moon_x + self.moon_radius, sun_y + self.moon_radius)
            center_x = self.canvas_width // 2
            distance = abs(moon_x - center_x)
            
            if distance < 10:
                info = ("TOTAL ECLIPSE (Totality):\n"
                        "The Moon completely covers the Sun. The Sun's delicate outer atmosphere, "
                        "the corona, becomes visible as a pearly white halo. It is millions of degrees hotter than the surface!")
            elif distance < self.sun_radius + 15 and distance >= 10:
                info = ("BAILY'S BEADS / DIAMOND RING:\n"
                        "Just before or after totality, a single point of sunlight shines through a rugged lunar valley "
                        "creating a brilliant 'Diamond Ring' effect.")
            elif distance < self.sun_radius * 2:
                info = ("PARTIAL ECLIPSE:\n"
                        "The Moon is partially obscuring the Sun. Always use protective eyewear (ISO 12312-2)!")
            else:
                info = "NO ECLIPSE:\nThe Moon and Sun are not aligned. (A perfect straight-line alignment is called Syzygy)."
            self.info_lbl.configure(text=info)
            
        elif view == "Space View":
            earth_cx = 650
            earth_cy = self.canvas_height // 2
            orbit_r_x = 250
            orbit_r_y = 120
            
            angle = math.pi/2 + (moon_x / 800.0) * math.pi
            moon_fixed_x = earth_cx + orbit_r_x * math.cos(angle)
            moon_y = earth_cy - orbit_r_y * math.sin(angle)
            
            self.canvas.coords("space_moon", moon_fixed_x - self.space_moon_r, moon_y - self.space_moon_r,
                                              moon_fixed_x + self.space_moon_r, moon_y + self.space_moon_r)
                                              
            sun_x, sun_y = -50, self.canvas_height // 2
            dx = moon_fixed_x - sun_x
            dy = moon_y - sun_y
            length = math.hypot(dx, dy)
            if length == 0: length = 1
            dir_x = dx / length
            dir_y = dy / length
            
            perp_x = -dir_y
            perp_y = dir_x
            
            moon_top_x = moon_fixed_x + perp_x * self.space_moon_r
            moon_top_y = moon_y + perp_y * self.space_moon_r
            moon_bot_x = moon_fixed_x - perp_x * self.space_moon_r
            moon_bot_y = moon_y - perp_y * self.space_moon_r
            
            umbra_tip_x = moon_fixed_x + dir_x * 300
            umbra_tip_y = moon_y + dir_y * 300
            
            self.canvas.coords("umbra", moon_top_x, moon_top_y, moon_bot_x, moon_bot_y, umbra_tip_x, umbra_tip_y)
            self.canvas.itemconfig("umbra", fill="#000000", stipple="gray50")
            
            pen_tip_top_x = moon_fixed_x + dir_x * 800 + perp_x * 200
            pen_tip_top_y = moon_y + dir_y * 800 + perp_y * 200
            pen_tip_bot_x = moon_fixed_x + dir_x * 800 - perp_x * 200
            pen_tip_bot_y = moon_y + dir_y * 800 - perp_y * 200
            
            self.canvas.coords("penumbra", moon_top_x, moon_top_y, moon_bot_x, moon_bot_y, pen_tip_bot_x, pen_tip_bot_y, pen_tip_top_x, pen_tip_top_y)
            self.canvas.itemconfig("penumbra", fill="#666666", stipple="gray25")
            
            self.canvas.tag_raise("space_earth")
            
            W_x = earth_cx - moon_fixed_x
            W_y = earth_cy - moon_y
            dist_to_center = abs(W_x * dir_y - W_y * dir_x)
            
            if dist_to_center < 15:
                info = "UMBRA HITS EARTH:\nThe dark inner shadow (Umbra) reaches Earth, causing a Total Solar Eclipse. The shadow races across the surface at 1,000 to 5,000 mph!"
            elif dist_to_center < 60:
                info = "PENUMBRA HITS EARTH:\nThe lighter outer shadow (Penumbra) sweeps across Earth, causing a Partial Solar Eclipse."
            else:
                info = "NO ECLIPSE:\nThe Moon's shadow misses the Earth entirely due to its 5-degree orbital tilt."
            self.info_lbl.configure(text=info)

    def auto_play_sim(self):
        if self.auto_playing: return
        self.auto_playing = True
        self.slider.set(0)
        self.animate_sim()

    def animate_sim(self):
        if not self.auto_playing: return
        current = self.slider.get()
        if current < 800:
            next_val = current + 3
            self.slider.set(next_val)
            self.update_simulation(next_val)
            self.after(20, self.animate_sim)
        else:
            self.auto_playing = False

    def exit_simulator(self):
        self.auto_playing = False
        self.controller.gamification.user_data["simulations_watched"] += 1
        self.controller.gamification.save()
        self.controller.gamification.award_badge("Astronomer")
        self.controller.show_frame("menu")
