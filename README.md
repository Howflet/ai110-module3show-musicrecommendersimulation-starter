# 🎵 Music Recommender Simulation

## Project Summary

This project is a content-based music recommender that scores songs from a 20-song catalog against a user's taste profile. Each song carries numeric features (energy, valence, danceability, acousticness) and categorical tags (genre, mood). The system computes a weighted similarity score, ranks all songs, and returns the top-k results with plain-language explanations of *why* each song was recommended.

---

## How The System Works

### Song Features

Each `Song` has these attributes: **genre**, **mood**, **energy** (0–1), **tempo_bpm**, **valence** (0–1, positivity), **danceability** (0–1), and **acousticness** (0–1).

### User Profile

A `UserProfile` stores:

- `favorite_genre` — one preferred genre (e.g. "pop", "lofi")
- `favorite_mood` — one preferred mood (e.g. "happy", "chill")
- `target_energy` — desired energy level (0–1)
- `likes_acoustic` — boolean flag for acoustic preference

### Scoring Rule

For every song the recommender adds up:

| Factor | Points | Condition |
|--------|--------|-----------|
| Genre match | +2.0 | song genre == user genre |
| Mood match | +1.5 | song mood == user mood |
| Energy closeness | +1.0 × (1 − \|Δenergy\|) | always applied |
| Acoustic bonus | +0.8 | likes_acoustic AND acousticness > 0.6 |
| Valence bonus | +0.5 × valence | always applied |

Songs are sorted by score descending, then the top *k* are returned.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python -m src.main
   ```

### Running Tests

Run the full test suite with:

```bash
pytest tests/test_recommender.py -v
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

- **Genre weight 2.0 → 0.5**: When genre weight was reduced from 2.0 to 0.5, the recommender stopped grouping same-genre songs at the top and instead surfaced cross-genre tracks that matched mood and energy. For a "pop/happy" listener, R&B and indie pop songs started appearing in the top 3.
- **Adding valence to the score**: Including valence as a +0.5 factor gave a slight edge to upbeat tracks. Without it, two songs with identical genre/mood/energy would tie; valence acts as a tiebreaker that favors positivity.
- **Acoustic user vs. non-acoustic user**: A lofi/chill listener with `likes_acoustic=True` saw "Library Rain" (acousticness 0.86) rise to rank 2, while the same profile without the acoustic flag ranked it 3rd. The +0.8 bonus swapped the ordering.
- **High-energy rock listener**: A rock/intense/energy-0.9 user correctly received "Storm Runner" at rank 1, but also got "Gym Hero" (pop/intense) at rank 2, showing that mood similarity can bridge genre gaps.

---

## Limitations and Risks

- **Tiny catalog**: Only 20 songs means many genres (e.g., metal, K-pop, Latin) are absent.
- **Single-genre preference**: The user profile allows only one favorite genre, so listeners with blended taste (e.g., "pop and hip-hop") are under-served.
- **No lyrics or language awareness**: The system cannot distinguish English from Spanish tracks, or filter by lyrical content.
- **Valence bias**: The valence bonus always rewards positive-sounding songs, which could over-favor "happy" music even for a user who prefers darker moods.
- **Cold-start problem**: There is no listening history — the system relies entirely on the user explicitly stating their preferences.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender highlighted how quantifying "taste" forces simplification. Real apps like Spotify use dozens of audio features plus collaborative filtering from millions of users, but even this small system can produce reasonable rankings once the weights are tuned. The most revealing experiment was changing the genre weight: a small number change reshaped the entire recommendation list, which shows how sensitive algorithmic outputs are to design choices that individual engineers make.

Bias can enter at multiple points — the song catalog itself skews toward English-language pop and lofi, the scoring weights assume genre is the strongest signal, and the valence bonus bakes in a preference for "positive" music. In a real product these choices could systematically exclude entire music cultures or reinforce existing popularity loops, making it harder for new or niche artists to surface.

---
