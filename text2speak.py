import tkinter as tk
from tkinter import filedialog, Text
from gtts import gTTS
import pygame
import PyPDF2
import pytesseract
from PIL import Image
import os

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech App")

        self.text_area = Text(root, wrap='word', width=50, height=15)
        self.text_area.pack(padx=20, pady=10)

        self.load_pdf_button = tk.Button(root, text="Load PDF", command=self.load_pdf)
        self.load_pdf_button.pack(pady=5)

        self.load_image_button = tk.Button(root, text="Load Image", command=self.load_image)
        self.load_image_button.pack(pady=5)

        self.convert_button = tk.Button(root, text="Convert to Speech", command=self.convert_to_speech)
        self.convert_button.pack(pady=5)

        self.play_button = tk.Button(root, text="Play", command=self.play_audio)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_audio)
        self.pause_button.pack(pady=5)

        self.resume_button = tk.Button(root, text="Resume", command=self.resume_audio)
        self.resume_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_audio)
        self.stop_button.pack(pady=5)

        pygame.mixer.init()

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ''
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, text)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            text = pytesseract.image_to_string(Image.open(file_path))
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, text)

    def convert_to_speech(self):
        text = self.text_area.get(1.0, tk.END)
        tts = gTTS(text)
        tts.save("output.mp3")

    def play_audio(self):
        if os.path.exists("output.mp3"):
            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play()

    def pause_audio(self):
        pygame.mixer.music.pause()

    def resume_audio(self):
        pygame.mixer.music.unpause()

    def stop_audio(self):
        pygame.mixer.music.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
