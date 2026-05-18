import streamlit as st
import random
import subprocess
import tempfile
import os

st.set_page_config(page_title="Melodi Dedektifi", page_icon="🎵", layout="wide")

# ---------------------------------------------------
# TAMAMEN SÖZSÜZ ENSTRÜMANİ PARÇALAR
# ---------------------------------------------------
songs = {
    # --- GİTAR ENSTRÜMANLERİ ---
    "Smoke On The Water":             "https://www.youtube.com/watch?v=aBo-AGCDpPM",
    "Classical Gas":                  "https://www.youtube.com/watch?v=Ht_sPFyQtjc",
    "Apache":                         "https://www.youtube.com/watch?v=AOIkGkPl1f8",
    "Eruption":                       "https://www.youtube.com/watch?v=yNOkPKuxaV0",
    "Cliffs Of Dover":                "https://www.youtube.com/watch?v=rj4fPBSCKbg",
    "Europa":                         "https://www.youtube.com/watch?v=JyhF5zYKyDY",
    "Albatross":                      "https://www.youtube.com/watch?v=6W_I7zgLmY4",
    "Jessica":                        "https://www.youtube.com/watch?v=lAkj7UAumxo",
    "Always With Me Always With You": "https://www.youtube.com/watch?v=KuD03I6THGI",
    "Little Wing":                    "https://www.youtube.com/watch?v=hg5qFDLhPMw",
    # --- FİLM & DİZİ MÜZİKLERİ ---
    "Game Of Thrones Theme":          "https://www.youtube.com/watch?v=QtkoEFbFGiQ",
    "Pirates Of Caribbean Theme":     "https://www.youtube.com/watch?v=27mB8verLK8",
    "Harry Potter Theme":             "https://www.youtube.com/watch?v=LylntHK8Avg",
    "Star Wars Theme":                "https://www.youtube.com/watch?v=_D0ZQPqeJkk",
    "Godfather Theme":                "https://www.youtube.com/watch?v=2KxYMVOjfHs",
    "Mission Impossible Theme":       "https://www.youtube.com/watch?v=XAYhNHhxN0A",
    "Schindlers List Theme":          "https://www.youtube.com/watch?v=bs-elRmLvb4",
    "Interstellar Theme":             "https://www.youtube.com/watch?v=UDVtMYqUAyw",
    "Gladiator Now We Are Free":      "https://www.youtube.com/watch?v=yMb2OuFEaT8",
    "James Bond Theme":               "https://www.youtube.com/watch?v=ySAIBhIpqgY",
    # --- KLASİK MÜZİK ---
    "Ode To Joy":                     "https://www.youtube.com/watch?v=_2EslFRhbic",
    "Canon In D":                     "https://www.youtube.com/watch?v=NlprozGcs80",
    "Fur Elise":                      "https://www.youtube.com/watch?v=_mVW8tgGY_w",
    "Eine Kleine Nachtmusik":         "https://www.youtube.com/watch?v=oy2zDJPIgwc",
    "Four Seasons Spring":            "https://www.youtube.com/watch?v=6LAPFM3ugag",
    "Moonlight Sonata":               "https://www.youtube.com/watch?v=4Tr0otuiQuU",
    "Clair De Lune":                  "https://www.youtube.com/watch?v=CvFH_6DNRCY",
    "Bolero":                         "https://www.youtube.com/watch?v=HBNKRNKh980",
    "Flight Of The Bumblebee":        "https://www.youtube.com/watch?v=aYAJopwEYv8",
    "Swan Lake Theme":                "https://www.youtube.com/watch?v=9cP0pkBFpYU",
    # --- TÜRK ENSTRÜMANLERİ ---
    "Hicaz Longa":                    "https://www.youtube.com/watch?v=UaO8jqHh3YY",
    "Nihavent Longa":                 "https://www.youtube.com/watch?v=YMeFiFbqL5s",
    "Segah Saz Semaisi":              "https://www.youtube.com/watch?v=KkWi5lF1cK8",
    "Uskudar":                        "https://www.youtube.com/watch?v=8M1gI4BNWCQ",
    "Kapilar":                        "https://www.youtube.com/watch?v=Qv7REtFSKoA",
    # --- FLAMENKO & DÜNYA ---
    "Recuerdos De La Alhambra":       "https://www.youtube.com/watch?v=sUMGfCOOKao",
    "Asturias":                       "https://www.youtube.com/watch?v=MaGGNFfQ_yw",
    "Malagena":                       "https://www.youtube.com/watch?v=1dHQJNg6hRA",
    "Spanish Romance":                "https://www.youtube.com/watch?v=1BNwBuNb2GI",
    "La Paloma":                      "https://www.youtube.com/watch?v=PO3MUddlzyA",
    # --- ROCK ENSTRÜMANLERİ ---
    "Misirlou":                       "https://www.youtube.com/watch?v=UQlFoHvQdxg",
    "Frankenstein":                   "https://www.youtube.com/watch?v=9l0DHjXbEqE",
    "Wipe Out":                       "https://www.youtube.com/watch?v=p13yZAjhU0M",
    "Green Onions":                   "https://www.youtube.com/watch?v=idEBT-NOOPY",
    "Pipeline":                       "https://www.youtube.com/watch?v=BGMbWMJSoQk",
    # --- AMBİYANS & PİYANO ---
    "Comptine D Un Autre Ete":        "https://www.youtube.com/watch?v=rOLuZtSzMmg",
    "Experience":                     "https://www.youtube.com/watch?v=h_tBFMCByLk",
    "River Flows In You":             "https://www.youtube.com/watch?v=7maJOI3QMu0",
    "Nuvole Bianche":                 "https://www.youtube.com/watch?v=ggFKLxAQBbc",
    "Divenire":                       "https://www.youtube.com/watch?v=En5JmXZDFYI",
}

# ---------------------------------------------------
# SES ÇEKME — yt-dlp ile YouTube'dan ses URL'si al
# ---------------------------------------------------
@st.cache_data(show_spinner=False)
def get_audio_bytes(youtube_url: str) -> bytes | None:
    """
    yt-dlp ile sesi indir, bytes olarak döndür.
    Streamlit cache sayesinde aynı parça tekrar indirilmez.
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = os.path.join(tmpdir, "audio.%(ext)s")
            result = subprocess.run(
                [
                    "yt-dlp",
                    "--no-playlist",
                    "-f", "bestaudio[ext=webm]/bestaudio/best",
                    "--extract-audio",
                    "--audio-format", "mp3",
                    "--audio-quality", "5",
                    "-o", out_path,
                    youtube_url,
                ],
                capture_output=True,
                timeout=60,
            )
            mp3_path = os.path.join(tmpdir, "audio.mp3")
            if os.path.exists(mp3_path):
                with open(mp3_path, "rb") as f:
                    return f.read()
    except Exception:
        pass
    return None

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
st.sidebar.caption(f"{len(songs)} enstrümantal parça • Sözsüz")

if st.sidebar.button("🎲 Rastgele Seç", use_container_width=True):
    reset_game(random.choice(song_names))
    st.rerun()

st.sidebar.markdown("---")

categories = {
    "🎸 Gitar Enstrümanleri":  song_names[0:10],
    "🎬 Film & Dizi":          song_names[10:20],
    "🎻 Klasik Müzik":         song_names[20:30],
    "🕌 Türk Enstrümanleri":   song_names[30:35],
    "💃 Flamenko & Dünya":     song_names[35:40],
    "🤘 Rock Enstrümanleri":   song_names[40:45],
    "🌙 Ambiyans & Piyano":    song_names[45:],
}

for cat_name, cat_songs in categories.items():
    with st.sidebar.expander(cat_name, expanded=False):
        for name in cat_songs:
            idx = song_names.index(name)
            is_active = st.session_state.selected_song == name
            label = f"{'▶ ' if is_active else ''}{idx + 1}. Parça"
            if st.button(label, key=f"song_{idx}", use_container_width=True):
                reset_game(name)
                st.rerun()

# ---------------------------------------------------
# ANA EKRAN
# ---------------------------------------------------
st.title("🎵 Melodi Dedektifi")
st.caption("Enstrümantal müziği dinle • Harfleri tahmin et • Parçanın adını bul!")

if st.session_state.selected_song is None:
    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**Nasıl Oynanır?**\n\n1. Sol panelden bir parça seç\n2. Müziği dinle (söz yok!)\n3. Harfleri tahmin et\n4. Parçanın adını bul!")
    with col_b:
        st.warning("**Kurallar**\n\n• 5 hakkın var\n• Yanlış harf = 1 hak\n• Yanlış isim = 1 hak\n• 0 hak = oyun bitti!")
    with col_c:
        st.success("**İpucu**\n\n• Tüm parçalar sözsüz!\n• Önce harfleri tahmin et\n• Rastgele butonu ile dene!")
    st.stop()

song = st.session_state.selected_song
if song not in songs:
    st.session_state.selected_song = None
    st.rerun()

url = songs[song]

# ---------------------------------------------------
# SES OYNATICI
# ---------------------------------------------------
st.markdown("---")

col_play1, col_play2 = st.columns([3, 1])
with col_play1:
    st.markdown("**🎵 Müziği Dinle**")
with col_play2:
    play_clicked = st.button("▶️ Çal", use_container_width=True)

if play_clicked or st.session_state.game_started:
    if not st.session_state.game_started:
        with st.spinner("🎵 Müzik yükleniyor..."):
            audio_bytes = get_audio_bytes(url)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
            st.session_state.game_started = True
        else:
            st.error("Ses yüklenemedi, lütfen başka bir parça seçin.")
            st.stop()
    else:
        audio_bytes = get_audio_bytes(url)
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
        else:
            st.error("Ses yüklenemedi.")
            st.stop()

if not st.session_state.game_started:
    st.info("▶️ Müziği dinlemek için **Çal** butonuna bas!")
    st.stop()

# ---------------------------------------------------
# OYUN ALANI
# ---------------------------------------------------
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
                    st.session_state.result_msg = "🎉 Tüm harfleri buldun! Parça adını da yaz bakalım."
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
st.markdown("**🎯 Parça Adı Tahmini**")
col5, col6 = st.columns([4, 1])
with col5:
    name_guess = st.text_input(
        "Parçanın adını yaz",
        label_visibility="collapsed",
        key="name_box",
        placeholder="Parçanın adını yaz..."
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
