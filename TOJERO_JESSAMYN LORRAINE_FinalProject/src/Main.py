# main.py
# Main application file for CLI Playlist Manager
# Contains PlaylistManager class: handles all playlists, data loading, and user interaction

import json
import os
from typing import Dict, List, Optional

# Import custom classes from other python files in the folder
from Song import Song
from Playlist import Playlist

# Manages all playlists, data persistence, user menus
class PlaylistManager:
    def __init__(self, data_file: str = "data/playlists.json"):
        # File where all playlist data will be saved/loaded
        self.data_file = data_file


        # Store all playlists in a dictionary
        self.playlists: Dict[str, Playlist] = {}
        # Auto-load saved data
        self._load_data()

    # Load saved playlists from JSON file
    # Runs automatically
    def _load_data(self) -> None:
        if not os.path.exists(self.data_file) or os.path.getsize(self.data_file) == 0:
            print(f"No existing data found in '{self.data_file}'. Starting fresh.")
            return
        # Try to read and parse JSON data
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Convert each saved playlist into a Playlist object
                for playlist_data in data:
                    try:
                        playlist = Playlist.from_dict(playlist_data)
                        self.playlists[playlist.name.lower()] = playlist
                    except (ValueError, KeyError) as e:
                        print(f"Warning: Skipping invalid playlist → {e}")
                print(f"✅ Successfully loaded playlists from '{self.data_file}'")

        # Handle corrupted JSON file
        except json.JSONDecodeError:
            print(f"❌ Error: '{self.data_file}' is corrupted or invalid JSON")
            self.playlists = {}

        # Handles file read errors
        except IOError as e:
            print(f"❌ Error reading file: {e}")
            self.playlists = {}

    # Save all current playlists to JSON file
    # Runs automatically or when user exits
    def _save_data(self) -> None:
        try:
            # Convert all Playlist objects → dictionaries for JSON storage
            data_to_save = [playlist.to_dict() for playlist in self.playlists.values()]
            # Write formatted JSON to file
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4)
            print(f"✅ Playlists saved to '{self.data_file}'")

        except IOError as e:
            print(f"❌ Error saving file: {e}")

    # Get playlist by name
    def _get_playlist_by_name(self, name: str) -> Optional[Playlist]:
        return self.playlists.get(name.lower())
    
    # Display Main Menu
    def _display_main_menu(self) -> None:
        print("\n" + "-"*35)
        print("      🎵 CLI PLAYLIST MANAGER      ")
        print("-"*35)
        print("1. Create New Playlist")
        print("2. View All Playlists")
        print("3. Manage Existing Playlist")
        print("4. Search All Songs")
        print("5. Delete All Playlists")
        print("6. Save & Exit")
        print("-"*35)

    # Display menu for actions inside ONE specific playlist
    def _display_playlist_management_menu(self, playlist_name: str) -> None:
        print("\n" + "-"*45)
        print(f"      MANAGING: {playlist_name.upper()}      ")
        print("-"*45)
        print("1. Add New Song + Mood Note")
        print("2. Remove Song")
        print("3. View All Songs")
        print("4. Find Songs by Artist")
        print("5. Sort Songs")
        print("6. Show Total Duration")
        print("7. Back to Main Menu")
        print("-"*45)

    # Create a new empty playlist
    def create_new_playlist(self) -> None:
        name = input("Enter new playlist name: ").strip()

        # Input cannot be empty
        if not name:
            print("❌ Playlist name cannot be empty!")
            return

        # No duplicates allowed
        if self._get_playlist_by_name(name):
            print(f"❌ Playlist '{name}' already exists!")
            return

        # Create and save new playlist
        try:
            new_playlist = Playlist(name)
            self.playlists[name.lower()] = new_playlist
            print(f"✅ Playlist '{name}' created successfully!")
        except ValueError as e:
            print(f"❌ Error: {e}")

    # List all playlists currently stored
    def view_all_playlists(self) -> None:
        print("\n📂 YOUR PLAYLISTS")
        print("-"*20)
        if not self.playlists:
            print("No playlists found. Create one first!")
            return

        # Print numbered list of all playlists
        for index, playlist in enumerate(self.playlists.values(), 1):
            print(f"{index}. {playlist}")

    # Remove every playlist from memory with user confirmation
    def delete_all_playlists(self) -> None:
        if not self.playlists:
            print("❌ No playlists exist to delete.")
            return

        confirm = input("Type DELETE to confirm removing ALL playlists: ").strip()
        if confirm != "DELETE":
            print("⚠️  Delete cancelled.")
            return

        self.playlists.clear()
        if os.path.exists(self.data_file):
            try:
                os.remove(self.data_file)
            except OSError as e:
                print(f"⚠️  Warning: could not remove data file: {e}")

        print("✅ All playlists deleted.")

    # Get song details from user input
    def _get_song_details(self) -> Optional[Song]:
        title = input("Enter song title: ").strip()
        artist = input("Enter artist name: ").strip()
        duration_str = input("Enter duration (seconds, e.g. 210): ").strip()
        mood_note = input("Enter mood note (optional): ").strip()
        # Required fields
        if not title or not artist or not duration_str:
            print("❌ All fields are required!")
            return None

        try:
            duration = int(duration_str)
            return Song(title, artist, duration, mood_note)
        except ValueError:
            print("❌ Duration must be a whole number (seconds only)")
            return None

    # Main logic: Select and manage one playlist
    def manage_playlist(self) -> None:
        # Show all playlists so user can choose
        self.view_all_playlists()
        if not self.playlists:
            return

        # Get playlist by number
        try:
            choice = int(input("\nEnter number of playlist to manage: ").strip())
            playlist_list = list(self.playlists.values())
            if 1 <= choice <= len(playlist_list):
                playlist = playlist_list[choice - 1]
            else:
                print("❌ Invalid number!")
                return
        except ValueError:
            print("❌ Please enter a valid number!")
            return

        while True:
            self._display_playlist_management_menu(playlist.name)
            choice = input("Enter your choice: ").strip()

            # 1. Add Song
            if choice == '1':
                print("\n🎵 ADD NEW SONG")
                song = self._get_song_details()
                if song:
                    if playlist.add_song(song):
                        print(f"✅ Added: {song.title} by {song.artist}")
                    else:
                        print(f"⚠️ That song is already in this playlist!")

            # 2. Remove Song
            elif choice == '2':
                title = input("Enter title of song to remove: ").strip()
                artist = input("Enter artist name: ").strip()
                if playlist.remove_song(title, artist):
                    print("✅ Song removed successfully")
                else:
                    print("❌ Song not found in this playlist")

            # 3. View All Songs
            elif choice == '3':
                playlist.display_songs()

            # 4. Search Songs by Artist
            elif choice == '4':
                artist = input("Enter artist name to search: ").strip()
                results = playlist.find_songs_by_artist(artist)
                if results:
                    print(f"\n🎵 Songs by {artist}:")
                    for s in results:
                        print(f"  • {s.title} ({s.duration_seconds}s)")
                else:
                    print(f"❌ No songs found by '{artist}'")

            # 5. Sort Songs
            elif choice == '5':
                print("\nSort by: 1=Title | 2=Artist | 3=Duration")
                sort_choice = input("Enter choice: ").strip()
                sort_map = {'1':'title', '2':'artist', '3':'duration'}
                if sort_choice in sort_map:
                    playlist.sort_songs(by=sort_map[sort_choice])
                    print("✅ Playlist sorted!")
                else:
                    print("❌ Invalid sort option")

            # 6. Show Total Playlist Duration
            elif choice == '6':
                total = playlist.total_duration()
                print(f"⏱️ Total duration: {total} seconds")

            # 7. Back to Main Menu
            elif choice == '7':
                break

            # Invalid input handling
            else:
                print("❌ Invalid choice! Enter a number 1–7")

    # Search EVERY playlist for songs matching keyword/artist
    def search_all_songs(self) -> None:
        keyword = input("Enter keyword or artist to search: ").strip().lower()
        found = False

        print("\n🔎 SEARCH RESULTS")
        print("-"*30)
        # Check all playlist
        for playlist in self.playlists.values():
            matches = [s for s in playlist.songs if keyword in s.title.lower() or keyword in s.artist.lower()]
            if matches:
                found = True
                print(f"\n📂 In Playlist: {playlist.name}")
                for song in matches:
                    print(f"  • {song.title} — {song.artist} ({song.duration_seconds}s)")

        if not found:
            print("❌ No matching songs found in any playlist")

    # MAIN APP LOOP: Run until user chooses Exit
    def run(self) -> None:
        print("🎶 WELCOME TO CLI PLAYLIST MANAGER 🎶")
        while True:
            self._display_main_menu()
            choice = input("Enter your choice: ").strip()

            # 1. Create Playlist
            if choice == '1':
                self.create_new_playlist()
            # 2. View All Playlists
            elif choice == '2':
                self.view_all_playlists()
            # 3. Manage Playlist
            elif choice == '3':
                self.manage_playlist()
            # 4. Search All Songs
            elif choice == '4':
                self.search_all_songs()
            # 5. Delete All Playlists
            elif choice == '5':
                self.delete_all_playlists()
            # 6. Save & Exit
            elif choice == '6':
                self._save_data()
                print("👋 Saved and exited. Goodbye!")
                break
            else:
                print("❌ Invalid choice! Enter a number 1–6")

# Run the app when this file is executed directly
if __name__ == "__main__":
    app = PlaylistManager()
    app.run()
