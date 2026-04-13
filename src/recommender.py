import csv
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score_song(self, user: UserProfile, song: Song) -> float:
        """Compute a relevance score for a song given a user profile."""
        score = 0.0

        # Genre match: +2.0
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0

        # Mood match: +1.5
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5

        # Energy closeness: up to +1.0 (closer is better)
        energy_diff = abs(song.energy - user.target_energy)
        score += 1.0 * (1.0 - energy_diff)

        # Acousticness bonus: +0.8 if the user likes acoustic and the song is acoustic
        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.8

        # Valence bonus: up to +0.5 (higher valence adds more)
        score += 0.5 * song.valence

        return round(score, 4)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user."""
        scored = [(song, self.score_song(user, song)) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Build a human-readable explanation of why a song was recommended."""
        reasons: List[str] = []

        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append(f"genre matches your favorite ({user.favorite_genre})")

        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append(f"mood matches your preference ({user.favorite_mood})")

        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff <= 0.15:
            reasons.append(f"energy level ({song.energy:.1f}) is close to your target ({user.target_energy:.1f})")

        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append(f"high acousticness ({song.acousticness:.1f}) fits your acoustic preference")

        if song.valence >= 0.7:
            reasons.append(f"positive vibes with valence of {song.valence:.2f}")

        if reasons:
            return f"Recommended because: {'; '.join(reasons)}."
        return "This song has a moderate fit across several factors."

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dictionaries.
    Numeric fields are cast to float.
    """
    # Resolve path relative to project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, csv_path)

    songs: List[Dict] = []
    with open(full_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for numeric_field in ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]:
                row[numeric_field] = float(row[numeric_field])
            songs.append(row)
    return songs


def _dict_to_song(d: Dict) -> Song:
    """Convert a song dictionary to a Song dataclass."""
    return Song(
        id=d["id"],
        title=d["title"],
        artist=d["artist"],
        genre=d["genre"],
        mood=d["mood"],
        energy=d["energy"],
        tempo_bpm=d["tempo_bpm"],
        valence=d["valence"],
        danceability=d["danceability"],
        acousticness=d["acousticness"],
    )


def _dict_to_user(prefs: Dict) -> UserProfile:
    """Convert a user preferences dict to a UserProfile dataclass."""
    return UserProfile(
        favorite_genre=prefs.get("genre", "pop"),
        favorite_mood=prefs.get("mood", "happy"),
        target_energy=float(prefs.get("energy", 0.5)),
        likes_acoustic=bool(prefs.get("likes_acoustic", False)),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional API for the recommendation logic.
    Returns a list of (song_dict, score, explanation) tuples.
    """
    song_objects = [_dict_to_song(d) for d in songs]
    user = _dict_to_user(user_prefs)
    rec = Recommender(song_objects)

    scored = [(s, rec.score_song(user, s)) for s in song_objects]
    scored.sort(key=lambda x: x[1], reverse=True)

    results: List[Tuple[Dict, float, str]] = []
    for song_obj, score in scored[:k]:
        explanation = rec.explain_recommendation(user, song_obj)
        # Convert back to dict for the caller
        song_dict = {
            "id": song_obj.id,
            "title": song_obj.title,
            "artist": song_obj.artist,
            "genre": song_obj.genre,
            "mood": song_obj.mood,
            "energy": song_obj.energy,
            "tempo_bpm": song_obj.tempo_bpm,
            "valence": song_obj.valence,
            "danceability": song_obj.danceability,
            "acousticness": song_obj.acousticness,
        }
        results.append((song_dict, score, explanation))
    return results
