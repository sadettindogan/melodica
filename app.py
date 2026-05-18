import streamlit as st
import numpy as np
import wave
import tempfile
import random

st.set_page_config(page_title="Melodi Dedektifi", page_icon="🎵")

# ---------------------------------------------------
# ŞARKILAR (isimler gizli, sadece notalar gösterilir)
# ---------------------------------------------------
songs = {
    "Akdeniz Akşamları": "5 5 6 5 4 3",
    "Twinkle Twinkle": "1 1 5 5 6 6 5",
    "Doğum Günün Kutlu Olsun": "1 1 2 1 4 3",
    "Mini Melodi": "1 2 3 4 5",
    "Sürpriz Senfoni": "3 3 4 5 5 4 3 2",
    "Bahar Ezgisi": "1 3 5 3 1 2 3",
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
def generate_tone(freq, duration=0.4, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave_data = 0.5 * np.sin(2 * np.pi * freq * t)
    return wave_data

def melody_to_audio(numbers):
    sample_rate = 44100
    melody = np.array([], dtype=np.float32)
    for num in numbers.split():
        if num in note_map:
            tone = generate_tone(note_map[num])
            silence = np.zeros(int(sample_rate * 0.05))
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
# SESSION STATE BAŞLAT
# ---------------------------------------------------
def init_state():
    if "selected_song" not in st.session_state:
        st.session_state.selected_song = None
    if "lives" not in st.session_state:
        st.session_state.lives = 5
    if "wrong_letters" not in st.session_state:
        st.session_state.wrong_letters = []
    if "revealed_letters" not in st.session_state:
        st.session_state.revealed_letters = set()
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "result_msg" not in st.session_state:
        st.session_state.result_msg = None
    if "result_type" not in st.session_state:
        st.session_state.result_type = None

def reset_game(song_name):
    st.session_state.selected_song = song_name
    st.session_state.lives = 5
    st.session_state.wrong_letters = []
    st.session_state.revealed_letters = set()
    st.session_state.game_over = False
    st.session_state.game_started = False
    st.session_state.result_msg = None
    st.session_state.result_type = None

init_state()

# ---------------------------------------------------
# YARDIMCI FONKSİYONLAR
# ---------------------------------------------------
def is_fully_revealed():
    name = st.session_state.selected_song.upper().replace(" ", "")
    return all(ch in st.session_state.revealed_letters for ch in name)

def render_blanks():
    name = st.session_state.selected_song
    words = name.upper().split(" ")
    display_words = []
    for word in words:
        letters = []
        for ch in word:
            if ch in st.session_state.revealed_letters:
                letters.append(f"**{ch}**")
            else:
                letters.append("\\_")
        display_words.append(" ".join(letters))
    st.markdown("### " + "　　".join(display_words))

def render_hearts():
    hearts = "❤️" * st.session_state.lives + "🖤" * (5 - st.session_state.lives)
    st.markdown(f"**Hak:** {hearts}")

# ---------------------------------------------------
# SIDEBAR — Melodi Seçimi (isimler gizli)
# ---------------------------------------------------
st.sidebar.title("🎵 Melodi Seç")

song_names = list(songs.keys())

for i, name in enumerate(song_names):
    label = f"Melodi {i+1} — {songs[name]}"
    if st.sidebar.button(label, key=f"song_{i}"):
        reset_game(name)

st.sidebar.markdown("---")
if st.sidebar.button("🎲 Rastgele Seç"):
    reset_game(random.choice(song_names))

# ---------------------------------------------------
# ANA EKRAN
# ---------------------------------------------------
st.title("🎵 Melodi Dedektifi")
st.caption("Melodiyi dinle, harfleri tahmin et, şarkıyı bul!")

if st.session_state.selected_song is None:
    st.info("Sol panelden bir melodi seç veya rastgele seç.")
    st.stop()

song = st.session_state.selected_song
notes = songs[song]

# Nota göster ve çal
st.markdown(f"**Notalar:** `{notes}`")
if st.button("▶️ Çal"):
    wav = melody_to_audio(notes)
    st.audio(wav)
    st.session_state.game_started = True

if not st.session_state.game_started:
    st.info("Melodiyi dinlemek için Çal butonuna bas, sonra tahmin et!")
    st.stop()

st.markdown("---")
st.subheader("🔍 Melodi Dedektifi")

# Harfleri göster
render_blanks()
render_hearts()

# Yanlış harfler
if st.session_state.wrong_letters:
    st.markdown(f"❌ **Yanlış harfler:** {', '.join(st.session_state.wrong_letters)}")

# Oyun bittiyse
if st.session_state.game_over:
    if st.session_state.result_type == "win":
        st.success(st.session_state.result_msg)
    else:
        st.error(st.session_state.result_msg)
    if st.button("🔄 Yeni Oyun"):
        reset_game(random.choice(song_names))
        st.rerun()
    st.stop()

# Harf tahmini
st.markdown("**Harf tahmin et:**")
col1, col2 = st.columns([1, 3])
with col1:
    letter_guess = st.text_input("Harf", max_chars=1, label_visibility="collapsed", key="letter_box").upper().strip()
with col2:
    if st.button("Harf Gönder"):
        if letter_guess and len(letter_guess) == 1:
            if letter_guess in st.session_state.revealed_letters or letter_guess in st.session_state.wrong_letters:
                st.warning("Bu harfi zaten denedin!")
            elif letter_guess in song.upper():
                st.session_state.revealed_letters.add(letter_guess)
                if is_fully_revealed():
                    st.session_state.result_msg = f"🎉 Tüm harfleri buldun! Şarkı adını da yaz bakalım."
                    st.session_state.result_type = "info"
            else:
                st.session_state.wrong_letters.append(letter_guess)
                st.session_state.lives -= 1
                if st.session_state.lives <= 0:
                    st.session_state.game_over = True
                    st.session_state.result_msg = f"💔 Hakkın kalmadı. Doğru cevap: {song}"
                    st.session_state.result_type = "lose"
            st.rerun()

if st.session_state.result_type == "info":
    st.info(st.session_state.result_msg)

# İsim tahmini
st.markdown("**Şarkı adı tahmini:**")
col3, col4 = st.columns([3, 1])
with col3:
    name_guess = st.text_input("Şarkının adını yaz", label_visibility="collapsed", key="name_box")
with col4:
    if st.button("Tahmin Et"):
        if name_guess.strip():
            if name_guess.strip().lower() == song.lower():
                st.session_state.game_over = True
                st.session_state.result_msg = f"🎉 Kazandınız! '{song}' doğru!"
                st.session_state.result_type = "win"
            else:
                st.session_state.lives -= 1
                if st.session_state.lives <= 0:
                    st.session_state.game_over = True
                    st.session_state.result_msg = f"💔 Hakkın kalmadı. Doğru cevap: {song}"
                    st.session_state.result_type = "lose"
                else:
                    st.warning(f"❌ Yanlış! {st.session_state.lives} hakkın kaldı.")
            st.rerun()
