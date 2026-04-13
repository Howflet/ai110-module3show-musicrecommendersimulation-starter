# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

> **VibeFinder 1.0**

---

## 2. Intended Use

- Suggests the top 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and acoustic taste.
- Assumes the user can express a single favorite genre and mood up front.
- This is a classroom exploration tool, **not** intended for real end-users or commercial deployment.

---

## 3. How the Model Works

The recommender looks at five things for every song:

1. **Genre match** — if the song's genre matches what the user likes, it gets a large boost.
2. **Mood match** — same idea for mood (happy, chill, intense, etc.).
3. **Energy closeness** — the closer the song's energy is to the user's target, the more points it earns. A perfect match gives full credit; a big difference loses most of the credit.
4. **Acoustic bonus** — if the user says they like acoustic music and the song has high acousticness, an extra bonus is added.
5. **Valence (positivity)** — songs with higher valence (more positive-sounding) get a small extra bump.

All five factors are added together into a single score. Songs are ranked by that score and the top results are returned.

No machine learning is used — the scoring is a hand-tuned weighted sum.

---

## 4. Data

- The catalog contains **20 songs** stored in `data/songs.csv`.
- 10 songs came from the starter template; 10 more were added to broaden genre coverage.
- **Genres represented**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, R&B, electronic, country, classical, hip-hop, folk.
- **Moods represented**: happy, chill, intense, relaxed, moody, focused.
- The dataset mostly reflects mainstream Western music taste — genres like K-pop, Afrobeats, reggaeton, and metal are not represented.
- All data was created manually, so there is no real streaming or popularity information.

---

## 5. Strengths

- **Transparent**: every recommendation comes with a plain-English explanation listing exactly which factors contributed.
- **Accurate for clear preferences**: when a user's profile cleanly matches a niche (e.g., "lofi/chill/low-energy/acoustic"), the top results feel intuitively correct — songs like "Midnight Coding" and "Library Rain" surface immediately.
- **Easy to tune**: because the scoring formula is explicit, changing a single weight produces visible, understandable shifts in output. This makes the system useful for teaching how recommender weights affect outcomes.
- **Fast**: scoring 20 songs is instantaneous, making it ideal for rapid experimentation.

---

## 6. Limitations and Bias

- **Small catalog**: 20 songs cannot represent the breadth of real music. Many genres and languages are absent.
- **Single-slot preferences**: the user can only specify one genre and one mood. Listeners with diverse or fluid tastes are modeled poorly.
- **Valence bias**: the always-on valence bonus subtly favors upbeat, positive-sounding music regardless of the user's stated mood. A user who prefers dark, moody tracks is slightly penalized.
- **Genre over-weight**: genre carries the highest single-factor bonus (+2.0). This can cause the system to cluster recommendations by genre even when mood or energy might be more relevant to the user.
- **No collaborative signal**: the system has no data about what other similar users listened to, so it cannot discover surprising cross-genre recommendations the way Spotify or YouTube can.
- **Fairness concern**: if deployed in a real product, the genre weight and catalog composition would systematically promote popular Western genres and underrepresent minority music cultures.

---

## 7. Evaluation

- **Two user profiles tested via CLI** (`python -m src.main`):
  - Pop/Happy/High-energy → top results were "Summer Breeze" and "Sunrise City" (both pop/happy), which matched expectations.
  - Lofi/Chill/Low-energy/Acoustic → top results were "Midnight Coding" and "Library Rain" (both lofi/chill/acoustic), again matching expectations.
- **Automated test suite** — 6 pytest tests covering sorting, genre priority, acoustic preference, k-limit, explanation non-emptiness, and CSV loading correctness. All pass.
- **Manual weight experiments** — changed genre weight from 2.0 to 0.5 and observed cross-genre songs entering the top 5, confirming the weight has high leverage.
- No numeric precision/recall metric was computed because the catalog is too small and there are no ground-truth "liked" labels.

---

## 8. Future Work

- **Multi-genre / multi-mood profiles** — let users express blended taste (e.g., "60% pop, 40% hip-hop").
- **Diversity-aware ranking** — instead of pure score ranking, inject variety so the top 5 is not all from the same genre.
- **Collaborative filtering** — if multiple users existed, use overlapping preferences to surface unexpected recommendations.
- **More features** — incorporate tempo ranges, lyric themes, song duration, and release year.
- **Explainability dashboard** — a Streamlit UI showing a bar chart breakdown of each factor's contribution to the score.

---

## 9. Personal Reflection

Building this system made it clear how much power sits in small design choices — changing a single weight from 2.0 to 0.5 completely reshuffled the top recommendations. That means the engineers and product managers who set these numbers in real-world apps like Spotify exert enormous influence over what billions of people hear.

What surprised me most was how the valence bonus quietly biases toward "happy" music even when the user hasn't asked for it. It is a reminder that defaults are never neutral — every scoring choice embeds a value judgment. Human oversight still matters because no formula can capture the subjective, cultural, and emotional dimensions of why someone loves a song.
