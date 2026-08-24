import tkinter as tk
from tkinter import font

# Farben im Cyberpunk-/Sci-Fi-Look
BG_COLOR = "#0b0c10"          # Tiefes Dunkelgrau/Schwarz
DISPLAY_BG = "#1f2833"        # Dunkles Schiefergrau
TEXT_COLOR = "#66fcf1"        # Neon-Cyan
BUTTON_BG = "#c5c6c7"         # Helleres Grau für Buttons
BUTTON_FG = "#0b0c10"         # Dunkler Text auf Standard-Buttons
OPERATOR_BG = "#45a29e"       # Milder Neon-Ton für Operatoren
SPECIAL_BG = "#ff007f"        # Neon-Pink/Magenta für C und =
SPECIAL_FG = "#ffffff"        # Weiß

class SpaceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("SPACE_CALC // v2.0")
        self.root.geometry("360x520")
        self.root.config(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.equation = ""
        
        # Benutzerdefinierte Schriftarten
        self.display_font = font.Font(family="Courier", size=24, weight="bold")
        self.btn_font = font.Font(family="Courier", size=14, weight="bold")

        # GUI-Elemente aufbauen
        self.create_widgets()

    def create_widgets(self):
        # Display-Rahmen für den Retro-Terminal-Look
        display_frame = tk.Frame(self.root, bg=BG_COLOR, bd=5)
        display_frame.pack(expand=True, fill="both", padx=15, pady=15)

        self.display_label = tk.Label(
            display_frame, 
            text="0", 
            anchor="e", 
            bg=DISPLAY_BG, 
            fg=TEXT_COLOR, 
            font=self.display_font, 
            padx=15, 
            pady=15,
            relief="sunken",
            bd=2
        )
        self.display_label.pack(expand=True, fill="both")

        # Button-Bereich
        btn_frame = tk.Frame(self.root, bg=BG_COLOR)
        btn_frame.pack(expand=True, fill="both", padx=15, pady=5)

        # Button-Layout (Matrix)
        buttons = [
            ('C', 0, 0, SPECIAL_BG, SPECIAL_FG), ('(', 0, 1, OPERATOR_BG, SPECIAL_FG), (')', 0, 2, OPERATOR_BG, SPECIAL_FG), ('/', 0, 3, OPERATOR_BG, SPECIAL_FG),
            ('7', 1, 0, BUTTON_BG, BUTTON_FG), ('8', 1, 1, BUTTON_BG, BUTTON_FG), ('9', 1, 2, BUTTON_BG, BUTTON_FG), ('*', 1, 3, OPERATOR_BG, SPECIAL_FG),
            ('4', 2, 0, BUTTON_BG, BUTTON_FG), ('5', 2, 1, BUTTON_BG, BUTTON_FG), ('6', 2, 2, BUTTON_BG, BUTTON_FG), ('-', 2, 3, OPERATOR_BG, SPECIAL_FG),
            ('1', 3, 0, BUTTON_BG, BUTTON_FG), ('2', 3, 1, BUTTON_BG, BUTTON_FG), ('3', 3, 2, BUTTON_BG, BUTTON_FG), ('+', 3, 3, OPERATOR_BG, SPECIAL_FG),
            ('0', 4, 0, BUTTON_BG, BUTTON_FG), ('.', 4, 1, BUTTON_BG, BUTTON_FG), ('=', 4, 2, SPECIAL_BG, SPECIAL_FG)
        ]

        # Grid-Konfiguration
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)

        # Buttons dynamisch erstellen
        for (text, row, col, bg, fg) in buttons:
            # Das '=' Zeichen über zwei Spalten ziehen falls gewünscht oder Standard lassen
            if text == '=':
                btn = tk.Button(btn_frame, text=text, font=self.btn_font, bg=bg, fg=fg, 
                                bd=0, activebackground=TEXT_COLOR, activeforeground=BG_COLOR,
                                command=self.calculate)
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=3, pady=3)
            elif text == 'C':
                btn = tk.Button(btn_frame, text=text, font=self.btn_font, bg=bg, fg=fg, 
                                bd=0, activebackground=TEXT_COLOR, activeforeground=BG_COLOR,
                                command=self.clear)
                btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
            else:
                btn = tk.Button(btn_frame, text=text, font=self.btn_font, bg=bg, fg=fg, 
                                bd=0, activebackground=TEXT_COLOR, activeforeground=BG_COLOR,
                                command=lambda t=text: self.append_char(t))
                btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

    def append_char(self, char):
        if self.display_label["text"] == "0" or self.display_label["text"] == "ERROR":
            self.equation = ""
        self.equation += str(char)
        self.display_label.config(text=self.equation)

    def clear(self):
        self.equation = ""
        self.display_label.config(text="0")

    def calculate(self):
        try:
            # Sicherheitshinweis: eval ist hier für lokale Skripte unbedenklich
            result = str(eval(self.equation))
            self.equation = result
            self.display_label.config(text=result)
        except Exception:
            self.display_label.config(text="ERROR")
            self.equation = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceCalculator(root)
    root.mainloop()