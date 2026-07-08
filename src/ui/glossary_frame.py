import customtkinter as ctk

class GlossaryFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=15, fg_color="transparent")
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        title = ctk.CTkLabel(self, text="📚 Encyclopedia", font=ctk.CTkFont(size=36, weight="bold"))
        title.grid(row=0, column=0, pady=(40, 10))
        
        sub = ctk.CTkLabel(self, text="Explore the science, safety, and history of eclipses.", font=ctk.CTkFont(size=18), text_color="gray")
        sub.grid(row=1, column=0, pady=(0, 20))

        self.tabview = ctk.CTkTabview(self, width=800, height=500, corner_radius=15, fg_color="#1a1a2e", segmented_button_selected_color="#4a148c", segmented_button_selected_hover_color="#6a1b9a")
        self.tabview.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        
        self.tabview.add("Terminology")
        self.tabview.add("Safety Guide")
        self.tabview.add("History")
        
        self.tabview.tab("Terminology").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Terminology").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Safety Guide").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Safety Guide").grid_rowconfigure(0, weight=1)
        self.tabview.tab("History").grid_columnconfigure(0, weight=1)
        self.tabview.tab("History").grid_rowconfigure(0, weight=1)
        
        self.build_terminology_tab()
        self.build_safety_tab()
        self.build_history_tab()

    def build_cards(self, parent_tab, items):
        scroll_frame = ctk.CTkScrollableFrame(parent_tab, fg_color="transparent")
        scroll_frame.grid(row=0, column=0, sticky="nsew")
        scroll_frame.grid_columnconfigure(0, weight=1)
        
        for i, (term, desc) in enumerate(items):
            card = ctk.CTkFrame(scroll_frame, fg_color="#2b2b2b", corner_radius=10)
            card.grid(row=i, column=0, sticky="ew", padx=10, pady=10)
            card.grid_columnconfigure(0, weight=1)
            
            t_lbl = ctk.CTkLabel(card, text=term, font=ctk.CTkFont(size=22, weight="bold"), text_color="#ffb74d", anchor="w")
            t_lbl.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
            
            d_lbl = ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=16), wraplength=700, justify="left", anchor="w")
            d_lbl.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))

    def build_terminology_tab(self):
        terms = [
            ("Totality", "The maximum phase of an eclipse when the sun is completely covered by the moon."),
            ("Syzygy", "A rough straight-line alignment of three celestial bodies (such as the Earth, Sun, and Moon)."),
            ("Umbra", "The fully shaded inner region of a shadow cast by an opaque object. Experiencing the umbra during a solar eclipse means witnessing Totality."),
            ("Penumbra", "The partially shaded outer region of a shadow. Observers in the penumbra see a Partial Eclipse."),
            ("Antumbra", "The lighter area of a shadow that appears beyond the umbra. Causes Annular (Ring of Fire) Eclipses."),
            ("Baily's Beads", "Bright spots of sunlight caused by the Moon's rugged topography shining through just seconds before/after totality."),
            ("Diamond Ring Effect", "A spectacular phenomenon occurring right before totality, where a single brilliant 'bead' of sunlight shines through a lunar valley."),
            ("Corona", "The outermost part of the Sun's atmosphere, visible only during a total solar eclipse as a pearly white halo."),
            ("Saros Cycle", "An 18-year, 11-day period used to predict eclipses."),
            ("Rayleigh Scattering", "The dispersion of electromagnetic radiation by atmospheric particles. This bends red light into the Earth's shadow, turning the Moon red during a Lunar Eclipse.")
        ]
        self.build_cards(self.tabview.tab("Terminology"), terms)
        
    def build_safety_tab(self):
        safety = [
            ("ISO 12312-2 Standard", "Always ensure your solar viewing glasses comply with the international ISO 12312-2 safety standard. Regular sunglasses, no matter how dark, are never safe for looking at the sun."),
            ("Solar Retinopathy", "Looking directly at the photosphere of the Sun (even during a partial eclipse) can cause solar retinopathy—permanent damage to the retina that has no cure. Always use protection!"),
            ("Pinhole Projector", "A safe, indirect way to view an eclipse. By letting sunlight pass through a small hole in a piece of cardboard, an inverted image of the eclipsed sun is projected onto the ground."),
            ("Telescopes & Binoculars", "NEVER look through a telescope, binoculars, or camera lens without a specialized solar filter securely attached to the FRONT of the device. The concentrated light will instantly burn through your eye.")
        ]
        self.build_cards(self.tabview.tab("Safety Guide"), safety)
        
    def build_history_tab(self):
        history = [
            ("The Battle of the Eclipse (585 BC)", "According to Herodotus, a total solar eclipse occurred during a battle between the Medes and the Lydians. The sudden darkness was interpreted as a sign from the gods, causing both sides to drop their weapons and negotiate a peace treaty. The astronomer Thales of Miletus is said to have predicted this eclipse."),
            ("Christopher Columbus in Jamaica (1504)", "Stranded in Jamaica, Columbus faced a hostile native population refusing to provide food. Knowing a total lunar eclipse was imminent from his almanac, he claimed his God was angry and would 'inflame the moon with wrath'. When the moon turned blood red, the terrified natives immediately brought provisions."),
            ("Proving Einstein's Relativity (1919)", "During the May 29, 1919 total solar eclipse, astronomer Arthur Eddington took photographs of stars near the eclipsed Sun. He proved that the Sun's massive gravity was bending the starlight, confirming Albert Einstein's revolutionary Theory of General Relativity."),
            ("Discovery of Helium (1868)", "French astronomer Pierre Janssen observed a total solar eclipse in India. While analyzing the spectrum of the solar prominences, he noticed a bright yellow line that didn't match any known element. He had discovered Helium, the first element discovered in space before it was found on Earth.")
        ]
        self.build_cards(self.tabview.tab("History"), history)
