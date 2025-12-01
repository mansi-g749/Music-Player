import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pygame import mixer # Use the mixer module from pygame

class MusicPlayerApp:

    def __init__(self, master):
        self.master = master
        master.title("CodeClause Python Music Player")
        
        # 1. Initialize the Pygame Mixer
        try:
            mixer.init()
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Could not initialize audio mixer. Error: {e}")
            master.destroy()
            return
        
        # State variables
        self.current_folder = ""
        self.playlist = []
        self.current_track_index = 0
        self.is_paused = False

        # Configure styles
        self.button_font = ('Helvetica', 10, 'bold')
        self.label_font = ('Helvetica', 12)
        
        # --- UI Elements ---
        
        # Frame for controls
        control_frame = tk.Frame(master, padx=10, pady=10, bg="#f0f0f0")
        control_frame.pack(pady=20, padx=20, fill='x')
        
        # Folder Selection Button
        self.select_button = tk.Button(control_frame, text="Select Music Folder", command=self.select_folder, 
                                       font=self.button_font, bg="#4CAF50", fg="white", 
                                       activebackground="#66BB6A", relief=tk.RAISED, bd=3)
        self.select_button.pack(pady=10, fill='x')

        # Current Track Display
        self.track_label = tk.Label(master, text="No folder selected", font=self.label_font, 
                                    bg="#2c3e50", fg="white", pady=10, padx=20, 
                                    relief=tk.SUNKEN, bd=2)
        self.track_label.pack(pady=(0, 20), padx=20, fill='x')

        # Frame for Playback Controls (buttons)
        playback_frame = tk.Frame(master, padx=10, pady=10, bg="#f0f0f0")
        playback_frame.pack(pady=10)

        # Buttons (Adjusted columns since Stop button is removed)
        self.prev_button = tk.Button(playback_frame, text="<< Previous", command=self.play_previous, 
                                     font=self.button_font, bg="#3498db", fg="white", width=12)
        self.prev_button.grid(row=0, column=0, padx=5, pady=5) # Column 0

        self.play_button = tk.Button(playback_frame, text="Play", command=self.play_music, 
                                     font=self.button_font, bg="#2ecc71", fg="white", width=10)
        self.play_button.grid(row=0, column=1, padx=5, pady=5) # Column 1

        self.pause_button = tk.Button(playback_frame, text="Pause", command=self.pause_music, 
                                      font=self.button_font, bg="#f39c12", fg="white", width=10)
        self.pause_button.grid(row=0, column=2, padx=5, pady=5) # Column 2
        
        # self.stop_button (REMOVED)

        self.next_button = tk.Button(playback_frame, text="Next >>", command=self.play_next, 
                                     font=self.button_font, bg="#3498db", fg="white", width=12)
        self.next_button.grid(row=0, column=3, padx=5, pady=5) # Column 3 (was 4)
        
        # Set up a function to check if the current song has finished
        master.after(1000, self.check_music_end)

    def select_folder(self):
        """Opens a dialog to select a folder and creates the playlist."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.current_folder = folder_selected
            self.playlist = []
            
            # Find all common music files (you can extend this list)
            for filename in os.listdir(folder_selected):
                if filename.endswith(('.mp3', '.wav', '.ogg')):
                    full_path = os.path.join(folder_selected, filename)
                    self.playlist.append(full_path)

            if not self.playlist:
                self.track_label.config(text="No music files (.mp3, .wav, .ogg) found in folder.")
                self.current_folder = ""
            else:
                self.current_track_index = 0
                self.track_label.config(text=f"Folder: {os.path.basename(self.current_folder)} | Ready to play.")
                self.play_music() # Auto-start playback on selection

    def load_track(self, index):
        """Loads and prepares a specific track for playback."""
        if not self.playlist:
            return

        track_path = self.playlist[index]
        track_name = os.path.basename(track_path)
        
        # Stop any currently playing music
        if mixer.music.get_busy():
            mixer.music.stop()
            
        try:
            mixer.music.load(track_path)
            self.track_label.config(text=f"Now Playing: {track_name}")
            return True
        except Exception as e:
            messagebox.showerror("Playback Error", f"Could not load track: {track_name}\nError: {e}")
            self.playlist.pop(index) # Remove problematic file
            self.current_track_index = index % len(self.playlist) # Wrap around index
            return False

    def play_music(self):
        """Starts or resumes music playback."""
        if not self.playlist:
            messagebox.showinfo("Player Info", "Please select a music folder first.")
            return

        if self.is_paused:
            # Resume if paused
            mixer.music.unpause()
            self.is_paused = False
            self.play_button.config(text="Playing")
        else:
            # Start fresh playback
            if self.load_track(self.current_track_index):
                mixer.music.play()
                self.is_paused = False
                self.play_button.config(text="Playing")

    def pause_music(self):
        """Pauses the current track."""
        if mixer.music.get_busy() or not self.is_paused:
            mixer.music.pause()
            self.is_paused = True
            self.play_button.config(text="Play")

    # The stop_music method has been removed entirely.

    def play_next(self):
        """Skips to the next track in the playlist."""
        if not self.playlist:
            return
        
        # Calculate next index (wraps around)
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.play_music()
    
    def play_previous(self):
        """Skips to the previous track in the playlist."""
        if not self.playlist:
            return
        
        # Calculate previous index (wraps around)
        self.current_track_index = (self.current_track_index - 1 + len(self.playlist)) % len(self.playlist)
        self.play_music()

    def check_music_end(self):
        """Checks if the music has stopped playing and advances to the next track."""
        # mixer.music.get_busy() returns False when music stops playing,
        # but only if it wasn't explicitly paused or stopped.
        if self.playlist and not mixer.music.get_busy() and not self.is_paused:
            # Music finished playing, load next track
            self.play_next()

        # Reschedule the check for the next second
        self.master.after(1000, self.check_music_end)

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Initialize and run the application
    app = MusicPlayerApp(root)
    root.mainloop()