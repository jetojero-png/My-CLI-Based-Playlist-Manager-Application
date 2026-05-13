# song.py
# Defines the Song class
# Stores song details: title, artist, duration; includes validation, string formatting, and JSON serialization methods

class Song:
    def __init__(self, title: str, artist: str, duration_seconds: int, mood_note: str = ""):
        # Validate title: must be non-empty string
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Song title cannot be empty.")
        # Validate artist: must be non-empty string
        if not isinstance(artist, str) or not artist.strip():
            raise ValueError("Song artist cannot be empty.")
        # Validate duration: must be positive whole number
        if not isinstance(duration_seconds, int) or duration_seconds < 0:
            raise ValueError("Song duration must be a non-negative integer.")

        # Assign values to instance attributes
        self.title = title
        self.artist = artist
        self.duration_seconds = duration_seconds
        self.mood_note = mood_note

    # Human-readable string output: "Song Title" by Artist (MM:SS)
    def __str__(self) -> str:
        minutes = self.duration_seconds // 60
        seconds = self.duration_seconds % 60
        mood_text = f" [{self.mood_note}]" if self.mood_note else ""
        return f'"{self.title}" by {self.artist} ({minutes:02d}:{seconds:02d}){mood_text}'

    # Debug string representation of the object
    def __repr__(self) -> str:
        return f"Song(title='{self.title}', artist='{self.artist}', duration_seconds={self.duration_seconds})"

    # Convert Song object → dictionary
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "artist": self.artist,
            "duration_seconds": self.duration_seconds,
            "mood_note": self.mood_note
        }

    # Create Song object FROM dictionary
    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["title"], data["artist"], data["duration_seconds"], data.get("mood_note", ""))

    # Define equality: 2 songs = same if title + artist match
    def __eq__(self, other) -> bool:
        if not isinstance(other, Song):
            return NotImplemented
        return (self.title.lower() == other.title.lower() and
                self.artist.lower() == other.artist.lower())

    # Define hash: allows storing songs in sets / using as dictionary keys
    def __hash__(self) -> int:
        return hash((self.title.lower(), self.artist.lower()))
