import streamlit as st
import numpy as np
import wave
import tempfile
from difflib import SequenceMatcher

st.set_page_config(page_title="Sayıdan Şarkı Tahmin Oyunu")

# ---------------------------------------------------
# ŞARKILAR
# ---------------------------------------------------

songs = {
    "Akdeniz Akşamları": "5 5 6 5 4 3",
    "Twinkle Twinkle": "1 1 5 5 6 6 5",
    "Mini Melodi": "1 2 3 4 5"
}

# ---------------------------------------------------
# NOTA FREKANSLARI
# ---------------------------------------------------

note_map = {
    "1": 261.63,  # C4
    "2": 293.66,  # D4
    "3": 329.63,  # E4
    "4": 349.23,  # F4
    "5": 392.00,  # G4
    "6": 440.00,  # A4
    "7": 493.88   # B4
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

    with wave.open(temp_wav.name, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(melody.tobytes())

    return temp_wav.name

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Hazır Melodiler")

for song_name, melody in songs.items():
    st.sidebar.markdown(f"### {song_name}")
    st.sidebar.code(melody)

# ---------------------------------------------------
# ANA EKRAN
# ---------------------------------------------------

st.title("🎵 Sayıdan Şarkı Tahmin Oyunu")

numbers = st.text_area(
    "Sayıları buraya yapıştır:",
    height=150
)

guess = st.text_input("Şarkı adı tahmini:")

# ---------------------------------------------------
# ÇAL BUTONU
# ---------------------------------------------------

if st.button("Çal"):

    if numbers.strip() == "":
        st.warning("Önce sayı gir.")
    else:

        wav_file = melody_to_audio(numbers)

        st.audio(wav_file)

        matched_song = None

        for song_name, melody in songs.items():

            similarity = SequenceMatcher(
                None,
                melody.strip(),
                numbers.strip()
            ).ratio()

            if similarity > 0.90:
                matched_song = song_name
                break

        if matched_song:

            if guess.strip().lower() == matched_song.lower():
                st.success("🎉 Tebrikler! Doğru bildin.")
            else:
                st.info("Şarkıyı buldun ama isim yanlış.")
                st.write(f"Doğru cevap: {matched_song}")

        else:
            st.error("Bu melodi sistemde yok.")