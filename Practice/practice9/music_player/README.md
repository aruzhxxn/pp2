Music Player (Pygame)

Description:
This project is a simple music player built using Pygame.
It loads audio files from a folder and allows the user to control playback using keyboard keys.
The player also displays the current track name, playback time, and a progress bar.

Features:
- Play and stop music
- Switch tracks (next / previous)
- Display current track name
- Show playback time
- Progress bar visualization
- Object-oriented design using MusicPlayer class

Controls:
P - play music
S - stop music
N - next track
B - previous track
Q - quit program

Project Structure:
- main.py → user interface and controls
- player.py → MusicPlayer class (logic)
- music/ → folder with audio files

Requirements:
- Python 3.x
- pygame

Run:
py -3.13 main.py

Notes:
- Place all music files inside the "music" folder
- Supported format: .mp3
- If no music is found, the program will display "No music"
