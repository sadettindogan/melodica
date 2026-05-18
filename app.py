import streamlit as st
import numpy as np
import wave
import tempfile
import random

st.set_page_config(page_title="Melodi Dedektifi", page_icon="🎵", layout="wide")

# ---------------------------------------------------
# 50 ŞARKI — Yerli & Yabancı Karışık
# Do=1 Re=2 Mi=3 Fa=4 Sol=5 La=6 Si=7
# ---------------------------------------------------
songs = {
    # --- YABANCI KLASİKLER (25 şarkı) ---
    "Twinkle Twinkle Little Star":   "1 1 5 5 6 6 5 4 4 3 3 2 2 1",
    "Happy Birthday":                "1 1 2 1 4 3 1 1 2 1 5 4",
    "Jingle Bells":                  "3 3 3 3 3 3 3 5 1 2 3",
    "Ode To Joy":                    "3 3 4 5 5 4 3 2 1 1 2 3 3 2 2",
    "We Will Rock You":              "1 1 3 1 1 3 1 1 3 5 5",
    "Smoke On The Water":            "1 3 4 1 3 5 4 1 3 4 3 1",
    "Eye Of The Tiger":              "3 3 3 1 3 3 3 1 3 5 4 3",
    "Nothing Else Matters":          "6 5 4 5 6 5 4 3 4 5",
    "Stairway To Heaven":            "6 5 4 3 4 5 6 7 1 2 3",
    "Hotel California":              "3 2 1 6 1 3 5 4 3",
    "Bohemian Rhapsody":             "5 5 5 3 4 5 6 5 4",
    "Knockin On Heavens Door":       "1 5 6 1 5 7 1 5 6",
    "Sweet Home Alabama":            "5 4 3 2 1 2 3 4 5",
    "Let It Be":                     "1 3 5 6 5 3 1 3 5 7 6",
    "Yesterday":                     "5 3 2 1 2 3 5 6 5",
    "Imagine":                       "1 3 5 1 3 5 6 5 3 1",
    "Wonderwall":                    "3 3 3 3 5 6 5 3 3 3",
    "Creep":                         "1 3 4 4 1 3 4 4 6 7",
    "Smells Like Teen Spirit":       "1 1 1 4 4 4 6 6 6 5 5 5",
    "Come As You Are":               "3 3 3 2 3 3 3 2 4 4 4",
    "Under The Bridge":              "5 3 2 1 2 3 5 6 5 3",
    "Master Of Puppets":             "1 1 1 7 1 7 1 6 1",
    "Wish You Were Here":            "5 5 3 5 5 3 5 4 3 2 3",
    "Paint It Black":                "3 2 1 7 1 2 3 4 5",
    "House Of The Rising Sun":       "1 3 4 6 1 3 4 6 5",
    # --- TÜRKÇE ŞARKILAR (15 şarkı) ---
    "Akdeniz Aksamlari":             "5 5 6 5 4 3 2 3 4 5",
    "Sari Sacli Mavi Gozlum":        "1 2 3 4 5 4 3 2 1 7 6",
    "Firuze":                        "5 6 5 4 3 4 5 6 5 3",
    "Gonulcelen":                    "3 4 5 6 5 4 3 2 1 2 3",
    "Seni Seviyorum":                "1 3 5 3 1 6 5 3 2 1",
    "Anlatamam":                     "5 5 4 3 4 5 6 5 4 3 2",
    "Aglama":                        "3 3 2 1 2 3 4 3 2 1 7",
    "Kalbim Seni Secti":             "1 2 3 5 3 2 1 7 1 2 3",
    "Donme Dolap":                   "5 5 3 3 4 4 2 2 1 1 7 7 6",
    "Cukurova":                      "1 1 2 3 4 5 5 4 3 2 1",
    "Yarim Istanbul":                "3 5 6 5 3 2 1 2 3 5",
    "Bir Derdim Var":                "5 4 3 2 1 2 3 4 5 6 5",
    "Kalp Kalbe Karsi":              "1 3 3 2 1 7 1 2 3 3",
    "Sevdan Kadar":                  "5 5 6 5 4 3 2 1 2 3 4",
    "Gitme":                         "3 4 5 6 5 4 3 2 3 4 5",
    # --- FİLM & DİZİ (10 şarkı) ---
    "Game Of Thrones":               "1 3 4 5 3 4 5 1 3 4 3 1 7",
    "Pirates Of Caribbean":          "3 1 3 1 3 4 3 1 2 1",
    "Harry Potter Theme":            "3 4 5 2 6 5 4 7 3 2",
    "Star Wars Theme":               "1 1 1 5 3 2 1 5 3 2 1",
    "Godfather Theme":               "4 3 4 2 1 2 1 7 1",
    "Mission Impossible":            "3 4 3 4 3 6 3 4 3 2",
    "Schindlers List":               "5 4 3 2 1 2 3 4 5 6 7",
    "Titanic My Heart Goes On":      "5 4 3 2 3 4 5 3 2 1",
    "Lion King Circle Of Life":      "5 5 6 5 4 3 4 5 6 7 1",
    "James Bond Theme":              "1 3 4 5 1 3 4 5 6 5 4",
}

# ---------------------------------------------------
# NOTA FREKANSLARI
# ---------------------------------------------------
note_map = {
    "1": 261.63,
    "2": 293.66,
    "3": 329.63,
    "4": 349.23,
    "5": 392.00,
    "6": 440.00,
    "7": 493.88,
}

# ---------------------------------------------------
# SES ÜRETME
# ---------------------------------------------------
def generate_tone(freq, duration=0.35, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave_data = 0.5 * np.sin(2 * np.pi * freq * t)
    fade = np.linspace(1, 0, len(wave_data))
    return wave_data * fade

def melody_to_audio(numbers):
    sample_rate = 44100
    melody = np.array([], dtype=np.float32)
    for num in numbers.split():
        if num in note_map:
            tone = generate_tone(note_map[num])
            silence = np.zeros(int(sample_rate * 0.06))
            melody = np.concatenate((melody, tone, silence))
    melody = np.int16(melody * 32767)
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_wav.name, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(melody.tobytes())
    return temp_wav.name

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
def init_state():
    defaults = {
        "selected_song": None,
        "lives": 5,
        "wrong_letters": [],
        "revealed_letters": set(),
        "game_over": False,
        "game_started": False,
        "result_msg": None,
        "result_type": None,
        "wrong_name_msg": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_game(song_name):
    st.session_state.selected_song = song_name
    st.session_state.lives = 5
    st.session_state.wrong_letters = []
    st.session_state.revealed_letters = set()
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.result_msg = None
    st.session_state.result_type = None
    st.session_state.wrong_name_msg = None

init_state()

# ---------------------------------------------------
# YARDIMCI
# ---------------------------------------------------
def is_fully_revealed():
    name = st.session_state.selected_song.upper().replace(" ", "")
    return all(ch in st.session_state.revealed_letters for ch in name)

def render_blanks():
    name = st.session_state.selected_song
    words = name.upper().split(" ")
    parts = []
    for word in words:
        letters = ["**" + ch + "**" if ch in st.session_state.revealed_letters else "\\_" for ch in word]
        parts.append(" ".join(letters))
    st.markdown("## " + "　　".join(parts))

def render_hearts():
    hearts = "❤️" * st.session_state.lives + "🖤" * (5 - st.session_state.lives)
    st.markdown(f"**Hak:** {hearts}")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
song_names = list(songs.keys())

st.sidebar.title("🎵 Melodi Listesi")
st.sidebar.caption(f"{len(songs)} şarkı • Yerli & Yabancı")

if st.sidebar.button("🎲 Rastgele Şarkı Seç", use_container_width=True):
    reset_game(random.choice(song_names))
    st.rerun()

st.sidebar.markdown("---")

categories = {
    "🌍 Yabancı Klasikler": song_names[:25],
    "🇹🇷 Türkçe Şarkılar": song_names[25:40],
    "🎬 Film & Dizi": song_names[40:],
}

for cat_name, cat_songs in categories.items():
    with st.sidebar.expander(cat_name, expanded=True):
        for name in cat_songs:
            idx = song_names.index(name)
            is_active = st.session_state.selected_song == name
            label = f"{'▶ ' if is_active else ''}{idx + 1}. `{songs[name]}`"
            if st.button(label, key=f"song_{idx}", use_container_width=True):
                reset_game(name)
                st.rerun()

# ---------------------------------------------------
# ANA EKRAN
# ---------------------------------------------------
st.title("🎵 Melodi Dedektifi")
st.caption("Melodiyi dinle • Harfleri tahmin et • Şarkıyı bul!")

if st.session_state.selected_song is None:
    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**Nasıl Oynanır?**\n\n1. Sol panelden bir melodi seç\n2. Çal butonuna bas\n3. Harfleri tahmin et\n4. Şarkı adını bul!")
    with col_b:
        st.warning("**Kurallar**\n\n• 5 hakkın var\n• Yanlış harf = 1 hak\n• Yanlış isim = 1 hak\n• 0 hak = oyun bitti!")
    with col_c:
        st.success("**İpucu**\n\n• Önce harfleri tahmin et\n• Notaları dikkatlice dinle\n• Rastgele butonu ile şansını dene!")
    st.stop()

song = st.session_state.selected_song
if song not in songs:
    st.session_state.selected_song = None
    st.rerun()
notes = songs[song]

st.markdown("---")
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(f"**Notalar:** `{notes}`")
with col2:
    if st.button("▶️ Melodiyi Çal", use_container_width=True):
        wav = melody_to_audio(notes)
        st.audio(wav)
        st.session_state.game_started = True

if not st.session_state.game_started:
    st.info("▶️ Melodiyi dinlemek için **Melodiyi Çal** butonuna bas, sonra tahmin etmeye başla!")
    st.stop()

st.markdown("---")
st.subheader("🔍 Melodi Dedektifi")

render_blanks()
render_hearts()

if st.session_state.wrong_letters:
    st.markdown(f"❌ **Yanlış harfler:** `{'  '.join(st.session_state.wrong_letters)}`")

# Oyun bitti
if st.session_state.game_over:
    if st.session_state.result_type == "win":
        st.success(st.session_state.result_msg)
        st.balloons()
    else:
        st.error(st.session_state.result_msg)
    if st.button("🔄 Yeni Oyun"):
        reset_game(random.choice(song_names))
        st.rerun()
    st.stop()

# Harf tahmini
st.markdown("---")
st.markdown("**🔤 Harf Tahmin Et**")
col3, col4 = st.columns([1, 4])
with col3:
    letter_guess = st.text_input(
        "Harf", max_chars=1,
        label_visibility="collapsed",
        key="letter_box",
        placeholder="?"
    ).upper().strip()
with col4:
    if st.button("Harf Gönder", use_container_width=True):
        if letter_guess and len(letter_guess) == 1:
            if letter_guess in st.session_state.revealed_letters or letter_guess in st.session_state.wrong_letters:
                st.toast("Bu harfi zaten denedin!", icon="⚠️")
            elif letter_guess in song.upper():
                st.session_state.revealed_letters.add(letter_guess)
                st.toast(f"'{letter_guess}' doğru!", icon="✅")
                if is_fully_revealed():
                    st.session_state.result_msg = "🎉 Tüm harfleri buldun! Şarkı adını da yaz bakalım."
                    st.session_state.result_type = "info"
            else:
                st.session_state.wrong_letters.append(letter_guess)
                st.session_state.lives -= 1
                st.toast(f"'{letter_guess}' yanlış!", icon="❌")
                if st.session_state.lives <= 0:
                    st.session_state.game_over = True
                    st.session_state.result_msg = f"💔 Hakkın kalmadı. Doğru cevap: **{song}**"
                    st.session_state.result_type = "lose"
            st.rerun()

if st.session_state.result_type == "info":
    st.info(st.session_state.result_msg)

# İsim tahmini
st.markdown("---")
st.markdown("**🎯 Şarkı Adı Tahmini**")
col5, col6 = st.columns([4, 1])
with col5:
    name_guess = st.text_input(
        "Şarkının adını yaz",
        label_visibility="collapsed",
        key="name_box",
        placeholder="Şarkının adını yaz..."
    )
with col6:
    if st.button("Tahmin Et", use_container_width=True):
        if name_guess.strip():
            if name_guess.strip().lower() == song.lower():
                st.session_state.game_over = True
                st.session_state.result_msg = f"🎉 Kazandınız! **{song}** doğru!"
                st.session_state.result_type = "win"
            else:
                st.session_state.lives -= 1
                if st.session_state.lives <= 0:
                    st.session_state.game_over = True
                    st.session_state.result_msg = f"💔 Hakkın kalmadı. Doğru cevap: **{song}**"
                    st.session_state.result_type = "lose"
                else:
                    st.session_state.wrong_name_msg = f"❌ **'{name_guess}'** yanlış! {st.session_state.lives} hakkın kaldı."
            st.rerun()

if st.session_state.wrong_name_msg and not st.session_state.game_over:
    st.warning(st.session_state.wrong_name_msg)
