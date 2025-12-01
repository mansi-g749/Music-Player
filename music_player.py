import os
import pygame
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, END, Button

# Initializing pygame mixer
pygame.mixer.init()

current_song = ""
paused = False
music_files = []

def select_folder():
    global music_files

    folder = filedialog.askdirectory()
    if not folder:
        return

    music_files = []
    song_list.delete(0, END)

    for file in os.listdir(folder):
        if file.endswith(".mp3") or file.endswith(".wav"):
            music_files.append(os.path.join(folder, file))
            song_list.insert(END, file)

    if not music_files:
        messagebox.showinfo("No songs", "No music files found in this folder.")

def play_song():
    global current_song, paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
        return

    selected = song_list.curselection()
    if not selected:
        messagebox.showwarning("Select Song", "Please select a song first.")
        return

    song_path = music_files[selected[0]]
    current_song = song_path

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

def pause_song():
    global paused
    pygame.mixer.music.pause()
    paused = True

def stop_song():
    pygame.mixer.music.stop()

# GUI Window
window = tk.Tk()
window.title("Simple Music Player")
window.geometry("350x350")

song_list = Listbox(window, width=50, height=10)
song_list.pack(pady=10)

Button(window, text="Open Music Folder", command=select_folder).pack(pady=5)
Button(window, text="Play", command=play_song).pack(pady=5)
Button(window, text="Pause", command=pause_song).pack(pady=5)
Button(window, text="Stop", command=stop_song).pack(pady=5)

window.mainloop()