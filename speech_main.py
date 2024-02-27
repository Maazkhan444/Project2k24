import os
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog
import pygame
from PIL import Image, ImageTk

# Initialize Tkinter root
root = tk.Tk()
root.title("Text-to-Speech Converter")
root.geometry("600x300")  # Adjusted dimensions
root.configure(bg="#ADD8E6")  # Light blue background color

# Initialize pygame mixer
pygame.mixer.init()

# Function to download language
def download_language(language):
    os.system(f"gtts-cli --all | findstr {language} > nul || gtts-cli __all{language}")

# Function to perform text-to-speech conversion
def text_to_speech(text, language, output_file):
    try:
        download_language(language)
    except Exception as e:
        print("Error downloading language:", e)
        return
    tts = gTTS(text, lang=language)
    tts.save(output_file)
    print("Text-to-speech conversion complete.")

# to extract text from URL
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text
    except Exception as e:
        print("Error extracting text from URL:", e)
        return None

#  to read text from file
def read_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except Exception as e:
        print("Error reading text from file:", e)
        return None

#  to convert text from URL
def convert_url():
    root.withdraw()
    url_root = tk.Toplevel(root)
    url_root.title("URL Converter")
    url_root.geometry("400x150")
    url_root.configure(bg="#ADD8E6")  

    def execute_conversion():
        url = url_entry.get()
        text = extract_text_from_url(url)
        process_text(text)

    url_entry = tk.Entry(url_root, width=40, bg="#FFFFFF", fg="#000000", bd=1, relief=tk.FLAT)  # White background with black text
    url_entry.pack(pady=(20, 10))
    convert_button = tk.Button(url_root, text="Convert", command=execute_conversion, bg="#1ED760", fg="#FFFFFF", bd=1, relief=tk.RAISED,
                                font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2")  # Green button with white text and bold font
    convert_button.pack(pady=10)

# to convert text
def convert_text():
    root.withdraw()
    text_root = tk.Toplevel(root)
    text_root.title("Text Converter")
    text_root.geometry("400x200")
    text_root.configure(bg="#ADD8E6")  

    def execute_conversion():
        text = text_entry.get("1.0", tk.END)
        process_text(text)

    text_entry = tk.Text(text_root, height=10, width=40, bg="#FFFFFF", fg="#000000", bd=1, relief=tk.FLAT)  # White background with black text
    text_entry.pack(pady=(20, 10))
    convert_button = tk.Button(text_root, text="Convert", command=execute_conversion, bg="#1ED760", fg="#FFFFFF", bd=1, relief=tk.RAISED,
                                font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2")  # Green button with white text and bold font
    convert_button.pack(pady=10)


def convert_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        text = read_text_from_file(file_path)
        process_text(text)


def process_text(text):
    if text:
        language = detect(text)
        output_file = "output.mp3"  # Output file 
        text_to_speech(text, language, output_file)
        status_label.config(text="Conversion successful. Audio file saved as 'output.mp3'.")
        
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue  
    else:
        status_label.config(text="Failed to extract text from the provided source.")

# GUI 
url_button = tk.Button(root, text="URL", command=convert_url, bg="#1ED760", fg="#FFFFFF", bd=1, relief=tk.RAISED,
                        font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2")  # Green button with white text and bold font
url_button.grid(row=0, column=0, padx=(50, 10), pady=(50, 10))  # Adjusted padding and margins

text_button = tk.Button(root, text="Text to Speech", command=convert_text, bg="#1ED760", fg="#FFFFFF", bd=1, relief=tk.RAISED,
                        font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2")  # Green button with white text and bold font
text_button.grid(row=0, column=1, padx=10, pady=(50, 10))

file_button = tk.Button(root, text="Choose File to Speech", command=convert_file, bg="#1ED760", fg="#FFFFFF", bd=1, relief=tk.RAISED,
                        font=("Arial", 14, "bold"), padx=20, pady=10, cursor="hand2")  # Green button with white text and bold font
file_button.grid(row=0, column=2, padx=(10, 50), pady=(50, 10))  # Adjusted padding and margins

status_label = tk.Label(root, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#ADD8E6")  # Light blue background color
status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky=tk.W+tk.E)


image = Image.open("XD.png")  
image = image.resize((500, 500), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(image)


image_label = tk.Label(root, image=photo, bg="#ADD8E6")  # Light blue background color
image_label.image = photo
image_label.grid(row=0, column=3, padx=(10, 50), pady=(50, 10))  # Adjusted padding and margins

root.mainloop()
