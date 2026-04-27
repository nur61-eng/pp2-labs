import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()  
        
        
        self.music_folder = "music"
        
        
        self.tracks = [
            os.path.join(self.music_folder, "track1.mp3"),
            os.path.join(self.music_folder, "track2.mp3"),
            os.path.join(self.music_folder, "track3.mp3")
        ]
        
        self.current_index = 0   
        self.is_playing = False  
    
    def play(self):
        pygame.mixer.music.load(self.tracks[self.current_index])
        pygame.mixer.music.play()
        self.is_playing = True
    
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
    
    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.tracks)
        self.play()
    
    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.play()
    
    def get_track_name(self):
        return os.path.basename(self.tracks[self.current_index])