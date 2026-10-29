"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src import recommender
from src.recommender import load_songs, recommend_songs

# Taste profiles: keys mirror the UserProfile dataclass
PROFILES = {
    # Standard profiles
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.38,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    # Adversarial / edge-case profiles
    "Sad Banger (conflicting mood + energy)": {
        "favorite_genre": "folk",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Ghost Genre (genre not in catalog)": {
        "favorite_genre": "k-pop",
        "favorite_mood": "happy",
        "target_energy": 0.7,
        "likes_acoustic": False,
    },
    "Acoustic EDM (genre vs acoustic conflict)": {
        "favorite_genre": "edm",
        "favorite_mood": "euphoric",
        "target_energy": 0.3,
        "likes_acoustic": True,
    },
}


def max_score() -> float:
    """Return the highest score a song can earn under the current weights."""
    return (
        recommender.GENRE_WEIGHT
        + recommender.MOOD_WEIGHT
        + recommender.ENERGY_WEIGHT
        + recommender.ACOUSTIC_WEIGHT
    )


def print_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one profile with scores and reasons."""
    print("=" * 60)
    print(f"Profile: {name}")
    print(
        f"  genre={user_prefs['favorite_genre']}, mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']}, likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommend_songs(user_prefs, songs, k=k), start=1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']} / {song['mood']}]")
        print(f"   Score: {score:.2f} / {max_score():.2f}")
        for reason in explanation.split(", "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print()
    for name, user_prefs in PROFILES.items():
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
