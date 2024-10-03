import sys
import os
import openai
import keyboard
import pyperclip
import time
from langdetect import detect
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageDraw, ImageTk

openai.api_key = '#API KEY'

class TextImprovementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jarvis Text Improvement")
        self.master.geometry('700x600')
        self.master.attributes('-topmost', True)
        self.master.configure(bg='#666666')

        self.set_custom_icon("logo.png")

        self.original_text = ""
        self.language = 'en'

        self.modern_font = tkfont.Font(family="Helvetica", size=12)

        self.master.withdraw()

        self.master.protocol("WM_DELETE_WINDOW", self.minimize_window)

        self.setup_ui()

    def set_custom_icon(self, icon_filename):
        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, icon_filename)
        else:
            icon_path = os.path.join(os.path.dirname(__file__), icon_filename)
        
        logo = Image.open(icon_path)
        logo_tk = ImageTk.PhotoImage(logo)
        self.master.iconphoto(False, logo_tk)

    def setup_ui(self):
        self.canvas = tk.Canvas(self.master, width=600, height=600, bg='#666666', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.content_frame = tk.Frame(self.master, bg='#666666')
        self.content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.original_label = tk.Label(self.content_frame, text="Original Text", bg='#666666', fg='white', font=self.modern_font)
        self.original_label.pack(pady=(10, 0))

        self.original_text_box = tk.Text(self.content_frame, height=10, width=70, bg='white', fg='black', font=self.modern_font, borderwidth=0, highlightthickness=0)
        self.original_text_box.pack(pady=(5, 10))

        self.improved_label = tk.Label(self.content_frame, text="Improved Text", bg='#666666', fg='white', font=self.modern_font)
        self.improved_label.pack(pady=(10, 0))

        self.improved_text_box = tk.Text(self.content_frame, height=10, width=70, bg='white', fg='black', font=self.modern_font, borderwidth=0, highlightthickness=0)
        self.improved_text_box.pack(pady=(5, 10))

        self.button_frame = tk.Frame(self.content_frame, bg='#666666')
        self.button_frame.pack(pady=(10, 0))

        self.professional_button = tk.Button(self.button_frame, text="Professional", command=lambda: self.update_text("Professional"), bg='white', fg='black', font=self.modern_font)
        self.professional_button.pack(side=tk.LEFT, padx=5)

        self.normal_button = tk.Button(self.button_frame, text="Normal", command=lambda: self.update_text("Normal"), bg='white', fg='black', font=self.modern_font)
        self.normal_button.pack(side=tk.LEFT, padx=5)

        self.rewrite_button = tk.Button(self.button_frame, text="Rewrite", command=lambda: self.update_text("Rewrite"), bg='white', fg='black', font=self.modern_font)
        self.rewrite_button.pack(side=tk.LEFT, padx=5)

        self.spell_check_button = tk.Button(self.button_frame, text="Spell Check", command=lambda: self.update_text("Spell Check"), bg='white', fg='black', font=self.modern_font)
        self.spell_check_button.pack(side=tk.LEFT, padx=5)

    def update_text(self, improvement_style):
        self.original_text_box.delete(1.0, tk.END)
        self.improved_text_box.delete(1.0, tk.END)

        self.original_text_box.insert(tk.END, "Loading...")
        self.improved_text_box.insert(tk.END, "Loading...")

        self.master.update()

        self.original_text_box.delete(1.0, tk.END)
        self.original_text_box.insert(tk.END, self.original_text)

        improved_text = improve_text_via_gpt(self.original_text, self.language, improvement_style)
        self.improved_text_box.delete(1.0, tk.END)
        self.improved_text_box.insert(tk.END, improved_text)

    def refresh_ui(self, new_text):
        self.original_text = new_text

        try:
            self.language = detect(self.original_text)
        except Exception:
            self.language = 'en'

        self.update_text("Normal")

    def minimize_window(self):
        self.master.withdraw()

    def restore_window(self):
        self.master.deiconify()


def improve_text_via_gpt(text, language, improvement_style):
    if language == 'nl':
        if improvement_style == "Professional":
            prompt = "You are a helpful assistant that improves Dutch text to be more professional and formal."
        elif improvement_style == "Normal":
            prompt = "You are a helpful assistant that improves Dutch text in a normal, natural style."
        elif improvement_style == "Rewrite":
            prompt = "You are a helpful assistant that rewrites Dutch text entirely while maintaining the original meaning."
        else:
            prompt = "You are a helpful assistant that focuses on checking and correcting the spelling of Dutch text."
    else:
        if improvement_style == "Professional":
            prompt = "You are a helpful assistant that improves English text to be more professional and formal."
        elif improvement_style == "Normal":
            prompt = "You are a helpful assistant that improves English text in a normal, natural style."
        elif improvement_style == "Rewrite":
            prompt = "You are a helpful assistant that rewrites English text entirely while maintaining the original meaning."
        else:
            prompt = "You are a helpful assistant that focuses on checking and correcting the spelling of English text."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Please improve the following text:\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        improved_text = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        improved_text = f"Error: {e}"

    return improved_text


def process_text(app):
    selected_text = pyperclip.paste()

    if selected_text:
        app.master.after(0, lambda: app.refresh_ui(selected_text))

        time.sleep(2)
        pyperclip.copy('')


def on_ctrl_q(app):
    app.restore_window()
    app.master.after(0, lambda: process_text(app))


if __name__ == "__main__":
    root = tk.Tk()
    app = TextImprovementApp(root)

    keyboard.add_hotkey('ctrl+q', lambda: on_ctrl_q(app))

    root.mainloop()

    keyboard.wait('esc')
