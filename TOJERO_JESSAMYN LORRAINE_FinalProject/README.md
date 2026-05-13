# Project Overview
This Python Application reflects my music playlists. I prefer my playlist to be organized and to keep the music vibe all through out listening hours. This CLI based application follows a modular design and Object Oriented Programming (OOP) principles with clean separation of data, logic and user inteface.

Users can easily create unlimited playlists, add songs with mood notes for keeping the reason what made you add the song into your playlist or what it made you feel to like the song. You can also search by the name of the artist, sort the playlist and save all the data automatically to the json file.

# KEY FEATURES OF THE CLI-based Playlist
* Create & delete playlists
* Add songs + custom mood note for each track
* Remove songs
* View full playlist with formatted duration
* Search songs by artist
* Sort songs by: Title | Artist | Duration
* View total playlist duration
* Search across all playlists at once
* Delete all playlists
* Data persistence: Auto-save / auto-load from  JSON 
* Full error handling (never crashes on invalid input)

# Error Handling
  Built-in protection ensures the app never crashes:
- Empty input → Clear message
- Duplicate names → Blocked
- Invalid menu choices → Guided correction
- Corrupted/missing JSON → Auto-reset safely
- Wrong data type → Rejected with instruction

# Advanced Python Concepts Used
 
1. List Comprehension - Filter/search data in one line ( Playlist.py  Line 99,  main.py  Line 272)
2. Context Manager - Safe file handling ( main.py  Line 53, 80)
3.  @classmethod - Create objects from saved JSON ( Song.py  Line 67,  Playlist.py  Line 139)
4. Magic/Dunder Methods -  _str_ ,  _eq_ ,  _hash_  for clean object behavior
5. Type Hints - Clear data types for readability & error prevention
6. Error Handling ( try...except ) → Handles missing files, corrupted data, invalid input

# Installation & How to Run
1. Requirements
    - Python 3.7 or higher
    - No external packages needed (uses only built-in modules)
2. Run the App
    - Open terminal / command prompt
    - Navigate to the project folder
3. Run
    - Create: Make a new empty playlist
    - Manage: Add/remove/sort/view songs inside a playlist
    - Search: Find any song by keyword or artist

- Save & Exit: Saves everything automatically
# Author
STUDENT: TOJERO, JESSAMYN LORRAINE S.
Section: BSCS 1A
Course: INTRODUCTION TO PROGRAMMING
Instructor: ALLAN IBO JR.
FINAL PROJECT