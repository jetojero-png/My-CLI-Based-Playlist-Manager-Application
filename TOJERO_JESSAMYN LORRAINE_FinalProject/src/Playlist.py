# playlist.py
# Defines the Playlist class
# This manages a collection of Song objects: add, remove, sort, search, display, categorize, and save/load to/from JSON

from typing import List, Optional, Dict
from Song import Song

class Playlist:
    def __init__(self, name: str):
        # Playlist name cannot be empty
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Playlist name cannot be empty.")

        self.name = name               # Playlist name
        self.songs: List[Song] = []    # List to store all Song objects

    # Playlist Name should be a string
    def __str__(self) -> str:
        return f"Playlist: {self.name} ({len(self.songs)} songs)"
    # Debugging string of the Playlist object
    def __repr__(self) -> str:
        return f"Playlist(name='{self.name}', songs={len(self.songs)} songs)"

    # Add a Song to playlist; prevent duplicates
    # Returns True if added, False if already exists
    def add_song(self, song: Song) -> bool:
        # Ensure only Song objects are added
        if not isinstance(song, Song):
            raise TypeError("Only Song objects can be added to a playlist.")

        # Add only if not already in playlist
        if song not in self.songs:
            self.songs.append(song)
            return True
        return False
    
    # Remove song by title + artist (case-insensitive)
    # Returns True if removed, False if not found
    def remove_song(self, song_title: str, song_artist: str) -> bool:
        target_title = song_title.lower()
        target_artist = song_artist.lower()
        # Loop through songs to find match
        for index, song in enumerate(self.songs):
            if song.title.lower() == target_title and song.artist.lower() == target_artist:
                self.songs.pop(index)
                return True
        return False

    # Group all songs by Genre
    def categorize_by_genre(self) -> Dict[str, List[Song]]:
        genre_groups: Dict[str, List[Song]] = {}
        for song in self.songs:
            genre = song.genre.capitalize()
            if genre not in genre_groups:
                genre_groups[genre] = []
            genre_groups[genre].append(song)
        return genre_groups

    # Display songs grouped by Genre
    def display_by_genre(self) -> None:
        genre_groups = self.categorize_by_genre()
        if not genre_groups:
            print("❌ No songs to categorize.")
            return

        print(f"\n🗂️  PLAYLIST: {self.name} — CATEGORIZED BY GENRE")
        print("-" * 60)
        for genre, songs in sorted(genre_groups.items()):
            print(f"\n🎵 {genre.upper()} ({len(songs)} songs):")
            for song in songs:
                print(f"   • {song.title} — {song.artist} | 📝 Mood: {song.mood_note or 'Not set yet'}")
        print("-" * 60)

    # Print full playlist: all songs
    def display_songs(self) -> None:
        print(f"\n📂 Playlist: {self.name}")
        print("-" * 60)

        if not self.songs:
            print("  This playlist is empty.")
            return

        # Print numbered list of songs
        for idx, song in enumerate(self.songs, 1):
            print(f"{idx}. {song}")
        print("-" * 60)

    # Search and return all songs by a specific artist (case-insensitive)
    def find_songs_by_artist(self, artist_name: str) -> List[Song]:
        target_artist = artist_name.lower()
        return [song for song in self.songs if song.artist.lower() == target_artist]

    # Sort songs by: title / artist / genre
    def sort_songs(self, key: str = 'title') -> None:
        # ✅ REMOVED DURATION OPTION
        valid_keys = ['title', 'artist', 'genre']
        if key not in valid_keys:
            raise ValueError(f"Invalid sort key: {key}. Must be one of: {', '.join(valid_keys)}.")

        # Sort logic (case-insensitive)
        self.songs.sort(
            key=lambda song: getattr(song, key).lower()
        )

    # Convert Playlist object → dictionary (for saving  to JSON)
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "songs": [song.to_dict() for song in self.songs]
        }

    # Create Playlist object FROM dictionary (for loading from JSON)
    @classmethod
    def from_dict(cls, data: dict):
        # Create new playlist instance
        playlist = cls(data["name"])
        # Add all saved songs
        for song_data in data.get("songs", []):
            playlist.add_song(Song.from_dict(song_data))
        return playlist