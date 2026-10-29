# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**

---

## 2. Intended Use  

**Goal / task:** VibeMatch suggests the top 5 songs from a small catalog that best fit one listener's taste. It doesn't predict whether you'll *actually* like a song. It ranks songs by how closely they match what you said you want.

**What it assumes about the user:** You can describe your taste with one favorite genre, one favorite mood, a target energy level (0 to 1), and whether you like acoustic sound. It assumes your taste doesn't change and that you mean exactly what you typed.

**Intended use:**

- Classroom exploration of how recommender systems turn data into rankings.
- Experimenting with weights and profiles to see how small rule changes shift results.

**Not intended for:**

- Real users or a real music app. The catalog has only 18 made-up songs.
- Judging what music is "good." A low score only means "not close to this profile."
- Any decision that matters to someone, such as which artists get promoted or paid. The system's biases (see section 6) would treat some artists and listeners unfairly.

---

## 3. How the Model Works  

VibeMatch gives every song a score out of 5 and then shows the 5 highest-scoring songs.

- **Same genre as your favorite?** +2 points.
- **Same mood as your favorite?** +1 point.
- **Energy:** up to 1.5 points. The closer the song's energy is to your target, the more points it gets. A song that's exactly right gets all 1.5. A song that's far off gets very few. It rewards being *close*, not being louder or quieter.
- **Acoustic sound:** up to 0.5 points. If you like acoustic music, more acoustic songs get more points. If you don't, less acoustic songs do.

Every song is scored on its own and then sorted from highest to lowest. Each recommendation lists the reasons it earned points, so you can see *why* it was picked.

**Changes from the starter:** The starter code returned the first few songs with no scoring. I added the scoring recipe above, the ranking step, the explanations, and a profile that also covers acoustic preference.

---

## 4. Data  

- **Size:** 18 songs. The starter had 10, and I added 8.
- **Features per song:** genre, mood, energy, tempo (BPM), valence (how positive it sounds), danceability, and acousticness. Title and artist are only for display.
- **Genres (15):** pop, indie pop, lofi, rock, metal, ambient, jazz, synthwave, hip-hop, classical, country, r&b, edm, reggae, folk.
- **Moods (14):** happy, chill, intense, relaxed, moody, focused, confident, melancholic, angry, nostalgic, romantic, euphoric, uplifting, sad.
- **What I added:** 8 songs in genres and moods the starter file didn't have (hip-hop, classical, metal, country, r&b, edm, reggae, folk).

**Limits:**

- Most genres have only 1 song. Lofi has 3 and pop has 2.
- The songs and numbers are made up, not measured from real audio.
- There are no lyrics, languages, release years, or artist popularity.
- Many styles are missing, such as Latin, K-pop, Afrobeats, gospel, and blues.

---

## 5. Strengths  

- **Clear-cut tastes work well.** The Chill Lofi and Deep Intense Rock profiles got exactly the songs I'd expect at #1 (*Library Rain* and *Storm Runner*, both scoring above 4.8 out of 5).
- **Opposite listeners get opposite lists.** The pop and lofi profiles share no songs in their top 5, so the system really does tell them apart.
- **Energy closeness works.** Without a genre match, it still finds songs with a similar feel. For example, the k-pop listener still got happy, mid-energy songs.
- **It's easy to explain.** Every pick comes with its reasons, so when something looks wrong (like *Gym Hero* for a happy-pop fan), you can see exactly which rule caused it.

---

## 6. Limitations and Bias 

**Main weakness: genre matching is all-or-nothing, so a single text label decides who gets good recommendations.** A genre match is worth 2.0 of the 5.0 possible points, but it only counts when the label is spelled exactly the same. *Rooftop Lights* ("indie pop") gets nothing from a "pop" fan, and a "k-pop" fan gets no genre points at all because that label doesn't exist in the catalog. This builds a filter bubble that's unfair to users with less common tastes. A lofi fan has three lofi songs to fill their top results, but a rock or folk fan has only one matching song, so after that first pick their list drops to songs that just happen to have similar energy. In the "Sad Banger" test, the system put a quiet, low-energy folk song (energy 0.25) at #1 for someone who asked for energy 0.9, because matching the genre and mood labels outweighed a big miss on the feel of the song.

Other limitations:

- `tempo_bpm`, `valence` and `danceability` are loaded but never used in scoring, so the system can't tell apart two songs with the same energy but a different feel.
- The user can name only one genre and one mood, so mixed tastes (for example, rock *and* metal) can't be expressed.
- With only 18 songs, most genres have just one representative, so top-5 lists often end with weak matches.
- There is no listening history (skips, likes, replays), so the system can't learn when it's wrong.

---

## 7. Evaluation  

### Profiles tested

I ran six profiles through `python -m src.main`. The first three are standard listeners. The last three are adversarial edge cases meant to trick the scoring.

| Profile | Genre | Mood | Energy | Likes acoustic | What it tests |
|---|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.8 | No | The default case |
| Chill Lofi | lofi | chill | 0.38 | Yes | The opposite end of the energy scale |
| Deep Intense Rock | rock | intense | 0.9 | No | A genre with only one song in the catalog |
| Sad Banger | folk | sad | 0.9 | No | A conflict: sad mood but high energy |
| Ghost Genre | k-pop | happy | 0.7 | No | A genre that doesn't exist in the catalog |
| Acoustic EDM | edm | euphoric | 0.3 | Yes | A conflict: an electronic genre but acoustic, low-energy preferences |

For each profile, I checked whether the top 5 "felt" right and whether the listed reasons explained the order.

### What surprised me

- **"Gym Hero" shows up for people who just want happy pop.** It's a pop workout track with an *intense* mood, yet it ranks #2 for the High-Energy Pop listener, ahead of *Rooftop Lights*, which is actually happy. In plain terms, the system cares most about the genre label: "pop" earns 2 points and "happy" earns only 1. *Gym Hero* is labeled pop and is very energetic, so it beats a happy song labeled "indie pop," which the system treats as a completely different genre.
- **Labels beat feel in conflicting profiles.** The Sad Banger listener wants a sad song at energy 0.9, but #1 is *Empty Station*, a quiet folk song at energy 0.25. Matching genre and mood was worth 3 points, more than enough to cover the big energy miss. The Acoustic EDM listener had the same thing happen: *Pulse Reactor*, a loud, non-acoustic EDM track, ranked #1 at 3.55, far ahead of everything else.
- **A missing genre doesn't break anything, it just weakens the results.** The k-pop listener still got sensible happy, mid-energy songs, but the best score was only 2.74 out of 5. The system never says "I don't have your genre."

### Comparing profiles

- **High-Energy Pop vs Chill Lofi:** The two lists have no songs in common. The pop list is full of loud, non-acoustic tracks (energy 0.75–0.93), and the lofi list moves to quiet, acoustic tracks (energy 0.28–0.42). This makes sense: energy and acoustic preferences point in opposite directions, so the songs that score well for one score badly for the other.
- **High-Energy Pop vs Deep Intense Rock:** Both lists include *Gym Hero*, but for different reasons. For the pop fan it matched the **genre**, and for the rock fan it matched the **mood** ("intense"). Both profiles want high energy, so the same loud songs fill the bottom of both lists.
- **Chill Lofi vs Deep Intense Rock:** The lofi fan gets three strong matches in a row (scores 4.88, 4.79, 3.86), while the rock fan gets one (4.93) and then a drop to 2.93. Lofi has three songs in the catalog and rock has one, so the scoring treats both fans the same, but the catalog serves them very differently.
- **Deep Intense Rock vs Sad Banger:** Both want energy around 0.9, and places #2–#5 are almost the same loud songs (*Storm Runner*, *Gym Hero*, *Pulse Reactor*, *Iron Tempest*). The only difference is #1: the rock fan's #1 is a good fit, while the Sad Banger's #1 is a song that matches the labels but is much too quiet.
- **Ghost Genre vs High-Energy Pop:** Both want happy songs, and the same two (*Sunrise City* and *Rooftop Lights*) are at the top, but in a different order. Without the "pop" genre bonus, *Sunrise City* loses its 2-point lead and *Rooftop Lights* edges ahead because its energy is closer to 0.7.
- **Acoustic EDM vs Chill Lofi:** Apart from the single EDM track at #1, the Acoustic EDM list is basically a chill playlist (*Spacewalk Thoughts*, *Library Rain*, classical, folk). Once the genre bonus is used up, the low-energy and acoustic preferences take over, so this user gets lofi-style results under an EDM label.

### Baseline output (genre 2.0, mood 1.0, energy 1.5, acoustic 0.5)

```
Loaded songs: 18

============================================================
Profile: High-Energy Pop
  genre=pop, mood=happy, energy=0.8, likes_acoustic=False
============================================================
1. Sunrise City by Neon Echo  [pop / happy]
   Score: 4.88 / 5.00
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.82 vs target 0.80 (+1.47)
     - acoustic fit (+0.41)
2. Gym Hero by Max Pulse  [pop / intense]
   Score: 3.78 / 5.00
     - genre match (+2.00)
     - energy 0.93 vs target 0.80 (+1.30)
     - acoustic fit (+0.47)
3. Rooftop Lights by Indigo Parade  [indie pop / happy]
   Score: 2.77 / 5.00
     - mood match (+1.00)
     - energy 0.76 vs target 0.80 (+1.44)
     - acoustic fit (+0.33)
4. Concrete Crown by Kilo Verse  [hip-hop / confident]
   Score: 1.91 / 5.00
     - energy 0.78 vs target 0.80 (+1.47)
     - acoustic fit (+0.44)
5. Night Drive Loop by Neon Echo  [synthwave / moody]
   Score: 1.81 / 5.00
     - energy 0.75 vs target 0.80 (+1.42)
     - acoustic fit (+0.39)

============================================================
Profile: Chill Lofi
  genre=lofi, mood=chill, energy=0.38, likes_acoustic=True
============================================================
1. Library Rain by Paper Lanterns  [lofi / chill]
   Score: 4.88 / 5.00
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.35 vs target 0.38 (+1.46)
     - acoustic fit (+0.43)
2. Midnight Coding by LoRoom  [lofi / chill]
   Score: 4.79 / 5.00
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.42 vs target 0.38 (+1.44)
     - acoustic fit (+0.35)
3. Focus Flow by LoRoom  [lofi / focused]
   Score: 3.86 / 5.00
     - genre match (+2.00)
     - energy 0.40 vs target 0.38 (+1.47)
     - acoustic fit (+0.39)
4. Spacewalk Thoughts by Orbit Bloom  [ambient / chill]
   Score: 2.81 / 5.00
     - mood match (+1.00)
     - energy 0.28 vs target 0.38 (+1.35)
     - acoustic fit (+0.46)
5. Coffee Shop Stories by Slow Stereo  [jazz / relaxed]
   Score: 1.93 / 5.00
     - energy 0.37 vs target 0.38 (+1.48)
     - acoustic fit (+0.45)

============================================================
Profile: Deep Intense Rock
  genre=rock, mood=intense, energy=0.9, likes_acoustic=False
============================================================
1. Storm Runner by Voltline  [rock / intense]
   Score: 4.93 / 5.00
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.91 vs target 0.90 (+1.48)
     - acoustic fit (+0.45)
2. Gym Hero by Max Pulse  [pop / intense]
   Score: 2.93 / 5.00
     - mood match (+1.00)
     - energy 0.93 vs target 0.90 (+1.46)
     - acoustic fit (+0.47)
3. Pulse Reactor by Kiko Volt  [edm / euphoric]
   Score: 1.91 / 5.00
     - energy 0.95 vs target 0.90 (+1.43)
     - acoustic fit (+0.48)
4. Iron Tempest by Ashen Gate  [metal / angry]
   Score: 1.88 / 5.00
     - energy 0.97 vs target 0.90 (+1.40)
     - acoustic fit (+0.48)
5. Sunrise City by Neon Echo  [pop / happy]
   Score: 1.79 / 5.00
     - energy 0.82 vs target 0.90 (+1.38)
     - acoustic fit (+0.41)

============================================================
Profile: Sad Banger (conflicting mood + energy)
  genre=folk, mood=sad, energy=0.9, likes_acoustic=False
============================================================
1. Empty Station by Grey Harbor  [folk / sad]
   Score: 3.57 / 5.00
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.25 vs target 0.90 (+0.52)
     - acoustic fit (+0.05)
2. Storm Runner by Voltline  [rock / intense]
   Score: 1.93 / 5.00
     - energy 0.91 vs target 0.90 (+1.48)
     - acoustic fit (+0.45)
3. Gym Hero by Max Pulse  [pop / intense]
   Score: 1.93 / 5.00
     - energy 0.93 vs target 0.90 (+1.46)
     - acoustic fit (+0.47)
4. Pulse Reactor by Kiko Volt  [edm / euphoric]
   Score: 1.91 / 5.00
     - energy 0.95 vs target 0.90 (+1.43)
     - acoustic fit (+0.48)
5. Iron Tempest by Ashen Gate  [metal / angry]
   Score: 1.88 / 5.00
     - energy 0.97 vs target 0.90 (+1.40)
     - acoustic fit (+0.48)

============================================================
Profile: Ghost Genre (genre not in catalog)
  genre=k-pop, mood=happy, energy=0.7, likes_acoustic=False
============================================================
1. Rooftop Lights by Indigo Parade  [indie pop / happy]
   Score: 2.74 / 5.00
     - mood match (+1.00)
     - energy 0.76 vs target 0.70 (+1.41)
     - acoustic fit (+0.33)
2. Sunrise City by Neon Echo  [pop / happy]
   Score: 2.73 / 5.00
     - mood match (+1.00)
     - energy 0.82 vs target 0.70 (+1.32)
     - acoustic fit (+0.41)
3. Concrete Crown by Kilo Verse  [hip-hop / confident]
   Score: 1.82 / 5.00
     - energy 0.78 vs target 0.70 (+1.38)
     - acoustic fit (+0.44)
4. Night Drive Loop by Neon Echo  [synthwave / moody]
   Score: 1.81 / 5.00
     - energy 0.75 vs target 0.70 (+1.42)
     - acoustic fit (+0.39)
5. Storm Runner by Voltline  [rock / intense]
   Score: 1.63 / 5.00
     - energy 0.91 vs target 0.70 (+1.18)
     - acoustic fit (+0.45)

============================================================
Profile: Acoustic EDM (genre vs acoustic conflict)
  genre=edm, mood=euphoric, energy=0.3, likes_acoustic=True
============================================================
1. Pulse Reactor by Kiko Volt  [edm / euphoric]
   Score: 3.55 / 5.00
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.95 vs target 0.30 (+0.53)
     - acoustic fit (+0.02)
2. Spacewalk Thoughts by Orbit Bloom  [ambient / chill]
   Score: 1.93 / 5.00
     - energy 0.28 vs target 0.30 (+1.47)
     - acoustic fit (+0.46)
3. Empty Station by Grey Harbor  [folk / sad]
   Score: 1.87 / 5.00
     - energy 0.25 vs target 0.30 (+1.42)
     - acoustic fit (+0.45)
4. Moonlit Sonata Redux by Elena Varga  [classical / melancholic]
   Score: 1.85 / 5.00
     - energy 0.22 vs target 0.30 (+1.38)
     - acoustic fit (+0.47)
5. Library Rain by Paper Lanterns  [lofi / chill]
   Score: 1.85 / 5.00
     - energy 0.35 vs target 0.30 (+1.42)
     - acoustic fit (+0.43)
```

### Experiment: weight shift (genre halved to 1.0, energy doubled to 3.0)

I changed the genre weight from 2.0 to 1.0 and the energy weight from 1.5 to 3.0, and left mood (1.0) and acoustic (0.5) the same. The math is still valid: every part is still non-negative and bounded, the energy part still ranges from 0 to its weight, and the maximum score rises from 5.0 to 5.5. Top-5 results per profile:

```
============================================================
Profile: High-Energy Pop
============================================================
1. Sunrise City by Neon Echo  [pop / happy]
   Score: 5.35 / 5.50
2. Rooftop Lights by Indigo Parade  [indie pop / happy]
   Score: 4.21 / 5.50
3. Gym Hero by Max Pulse  [pop / intense]
   Score: 4.08 / 5.50
4. Concrete Crown by Kilo Verse  [hip-hop / confident]
   Score: 3.38 / 5.50
5. Night Drive Loop by Neon Echo  [synthwave / moody]
   Score: 3.24 / 5.50
============================================================
Profile: Chill Lofi
============================================================
1. Library Rain by Paper Lanterns  [lofi / chill]
   Score: 5.34 / 5.50
2. Midnight Coding by LoRoom  [lofi / chill]
   Score: 5.23 / 5.50
3. Focus Flow by LoRoom  [lofi / focused]
   Score: 4.33 / 5.50
4. Spacewalk Thoughts by Orbit Bloom  [ambient / chill]
   Score: 4.16 / 5.50
5. Coffee Shop Stories by Slow Stereo  [jazz / relaxed]
   Score: 3.41 / 5.50
============================================================
Profile: Deep Intense Rock
============================================================
1. Storm Runner by Voltline  [rock / intense]
   Score: 5.42 / 5.50
2. Gym Hero by Max Pulse  [pop / intense]
   Score: 4.38 / 5.50
3. Pulse Reactor by Kiko Volt  [edm / euphoric]
   Score: 3.33 / 5.50
4. Iron Tempest by Ashen Gate  [metal / angry]
   Score: 3.27 / 5.50
5. Sunrise City by Neon Echo  [pop / happy]
   Score: 3.17 / 5.50
============================================================
Profile: Sad Banger (conflicting mood + energy)
============================================================
1. Storm Runner by Voltline  [rock / intense]
   Score: 3.42 / 5.50
2. Gym Hero by Max Pulse  [pop / intense]
   Score: 3.39 / 5.50
3. Pulse Reactor by Kiko Volt  [edm / euphoric]
   Score: 3.33 / 5.50
4. Iron Tempest by Ashen Gate  [metal / angry]
   Score: 3.27 / 5.50
5. Sunrise City by Neon Echo  [pop / happy]
   Score: 3.17 / 5.50
============================================================
Profile: Ghost Genre (genre not in catalog)
============================================================
1. Rooftop Lights by Indigo Parade  [indie pop / happy]
   Score: 4.14 / 5.50
2. Sunrise City by Neon Echo  [pop / happy]
   Score: 4.05 / 5.50
3. Night Drive Loop by Neon Echo  [synthwave / moody]
   Score: 3.24 / 5.50
4. Concrete Crown by Kilo Verse  [hip-hop / confident]
   Score: 3.20 / 5.50
5. Island Time by Roots Harbor  [reggae / uplifting]
   Score: 2.98 / 5.50
============================================================
Profile: Acoustic EDM (genre vs acoustic conflict)
============================================================
1. Spacewalk Thoughts by Orbit Bloom  [ambient / chill]
   Score: 3.40 / 5.50
2. Empty Station by Grey Harbor  [folk / sad]
   Score: 3.30 / 5.50
3. Library Rain by Paper Lanterns  [lofi / chill]
   Score: 3.28 / 5.50
4. Moonlit Sonata Redux by Elena Varga  [classical / melancholic]
   Score: 3.24 / 5.50
5. Coffee Shop Stories by Slow Stereo  [jazz / relaxed]
   Score: 3.23 / 5.50
```

**More accurate, or just different?** Both, depending on the profile:

- **More accurate for High-Energy Pop.** *Rooftop Lights* (happy, energy 0.76) rose to #2 above *Gym Hero* (intense). For someone asking for happy pop, that feels more correct.
- **Unchanged for Chill Lofi and Deep Intense Rock.** These profiles have labels and energy pointing the same way, so the change in weights didn't change the order.
- **Different but arguably worse for the conflicting profiles.** *Empty Station* fell out of the Sad Banger's top 5 completely, and *Pulse Reactor* fell out of the Acoustic EDM top 5. The system now ignores what those users said they wanted (folk/sad, EDM) and recommends only by energy.

Neither weighting is "correct." Weighting genre more trusts the labels, and weighting energy more trusts the feel. The best balance depends on whether the user's labels or their energy target is the better signal of what they want. I kept the original weights in the code.

---

## 8. Future Work  

1. **Partial genre credit.** Group related genres into families (pop ↔ indie pop ↔ k-pop, rock ↔ metal) and give half points for a near match. Then *Rooftop Lights* would count for a pop fan, and a k-pop fan would get pop songs.
2. **Let users list more than one genre or mood**, and let a user say which matters more to them (for example, "the feel matters more than the label").
3. **Use the unused features and add variety.** Add closeness scores for valence and tempo, and stop one artist or genre from taking over the whole top 5. The system could also warn the user when no song matches their genre.

---

## 9. Personal Reflection  

**Biggest learning moment:** I learned that the weights *are* the opinions of the system. Changing two numbers (genre 2.0 → 1.0, energy 1.5 → 3.0) fixed the happy-pop list but broke the Sad Banger and Acoustic EDM lists. There was no "correct" setting, only trade-offs about which signal to trust more, the labels or the feel. That made me realize that real apps are constantly making choices like this for millions of people.

**Using AI tools:** AI helped me move fast. It explained collaborative vs content-based filtering, suggested the "closeness" formula for energy, generated the new songs, wrote the scoring and ranking code, and came up with tricky edge-case profiles I wouldn't have thought of. But I still had to check its work. The starter `main.py` had a broken import that only showed up when I actually ran the program. When output was copied into the README by hand, one number was typed wrong (0.78 instead of 0.75), so I switched to pasting the real terminal output. The AI's write-ups were also *its* reading of the results, so I had to compare them with my own sense of whether the songs fit.

**What surprised me:** It surprised me how much a few lines of addition and sorting "feel" like a real recommendation. When it explains that *Library Rain* matched my genre, my mood, and was within 0.03 of my energy, it sounds smart. It also surprised me how confidently it gives a bad answer, like a quiet folk song for someone who asked for high energy. It never says "I'm not sure."

**What I'd try next:** I'd add fake listening history (likes and skips) for a few made-up users and try a simple collaborative-filtering step ("people who liked this also liked..."). Then I'd compare it with the content-based version to see which one handles odd tastes like the Sad Banger better.  
