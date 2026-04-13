"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from the catalog.\n")

    # --- Profile 1: Pop / Happy / High-Energy listener ---
    user_prefs_1 = {"genre": "pop", "mood": "happy", "energy": 0.8}

    print("=" * 50)
    print("User Profile 1: Pop / Happy / Energy 0.8")
    print("=" * 50)
    recommendations = recommend_songs(user_prefs_1, songs, k=5)
    for song, score, explanation in recommendations:
        print(f"  {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"    Because: {explanation}")
        print()

    # --- Profile 2: Lofi / Chill / Low-Energy acoustic fan ---
    user_prefs_2 = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    }

    print("=" * 50)
    print("User Profile 2: Lofi / Chill / Energy 0.4 / Acoustic")
    print("=" * 50)
    recommendations = recommend_songs(user_prefs_2, songs, k=5)
    for song, score, explanation in recommendations:
        print(f"  {song['title']} by {song['artist']} - Score: {score:.2f}")
        print(f"    Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
