import streamlit as st
import random
from streamlit_player import st_player

st.set_page_config(page_title="Melodi Dedektifi", page_icon="🎵", layout="wide")

# ---------------------------------------------------
# ŞARKILAR — { "İsim": "youtube_url" }
# ---------------------------------------------------
songs = {
    # --- YABANCI KLASİKLER ---
    "Smoke On The Water":          "https://www.youtube.com/watch?v=aBo-AGCDpPM",
    "Eye Of The Tiger":            "https://www.youtube.com/watch?v=btPJPFnesV4",
    "Nothing Else Matters":        "https://www.youtube.com/watch?v=tAGnKpE4NCI",
    "Stairway To Heaven":          "https://www.youtube.com/watch?v=QkF3oxziUI4",
    "Hotel California":            "https://www.youtube.com/watch?v=BciS5krYL80",
    "Bohemian Rhapsody":           "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",
    "Knockin On Heavens Door":     "https://www.youtube.com/watch?v=pRlFSMSRFgs",
    "Sweet Home Alabama":          "https://www.youtube.com/watch?v=ye5BuYf8q4o",
    "Let It Be":                   "https://www.youtube.com/watch?v=qj-oTgCOmCE",
    "Yesterday":                   "https://www.youtube.com/watch?v=wXTJBr9tt8Q",
    "Imagine":                     "https://www.youtube.com/watch?v=YkgkThdzX-8",
    "Wonderwall":                  "https://www.youtube.com/watch?v=bx1Bh8ZvH84",
    "Creep":                       "https://www.youtube.com/watch?v=XFkzRNyygfk",
    "Smells Like Teen Spirit":     "https://www.youtube.com/watch?v=hTWKbfoikeg",
    "Come As You Are":             "https://www.youtube.com/watch?v=vabnZ9-ex7o",
    "Under The Bridge":            "https://www.youtube.com/watch?v=lwmKkblFxzk",
    "Master Of Puppets":           "https://www.youtube.com/watch?v=E0ozmU9cJDg",
    "Wish You Were Here":          "https://www.youtube.com/watch?v=IXdNnw99-Ic",
    "Paint It Black":              "https://www.youtube.com/watch?v=O4irXQhgMqg",
    "House Of The Rising Sun":     "https://www.youtube.com/watch?v=f_RkFcBfFDQ",
    "We Will Rock You":            "https://www.youtube.com/watch?v=-tJYN-eG1zk",
    "Sweet Child O Mine":          "https://www.youtube.com/watch?v=1w7OgIMMRc4",
    "November Rain":               "https://www.youtube.com/watch?v=8SbUC-UaAxE",
    "Comfortably Numb":            "https://www.youtube.com/watch?v=_FrOQC-zEog",
    "Sultans Of Swing":            "https://www.youtube.com/watch?v=0fAQhSRLQnM",
    # --- TÜRKÇE ŞARKILAR ---
    "Firuze":                      "https://www.youtube.com/watch?v=OjQgCeBLg3s",
    "Anlatamam":                   "https://www.youtube.com/watch?v=FpEGFBBvgHw",
    "Bir Derdim Var":              "https://www.youtube.com/watch?v=MJFEnpDqmFk",
    "Gonulcelen":                  "https://www.youtube.com/watch?v=qRvKSELFhO4",
    "Seni Seviyorum":              "https://www.youtube.com/watch?v=Ue1mx_hu-bA",
    "Yalnizlik Senfonisi":         "https://www.youtube.com/watch?v=4C6NH5bKnc8",
    "Kalp Kalbe Karsi":            "https://www.youtube.com/watch?v=eTzSCOhPa_k",
    "Sevdan Kadar":                "https://www.youtube.com/watch?v=o-XjSmb-GGg",
    "Gitme":                       "https://www.youtube.com/watch?v=b7ELWAaYsKo",
    "Donme Dolap":                 "https://www.youtube.com/watch?v=mq36KLAMdvI",
    "Yarim Istanbul":              "https://www.youtube.com/watch?v=Ue3HF_gM8kk",
    "Aglama":                      "https://www.youtube.com/watch?v=VqK3KsHQQmk",
    "Kalbim Seni Secti":           "https://www.youtube.com/watch?v=UW8f7cBqVNE",
    "Cukurova":                    "https://www.youtube.com/watch?v=FUJ3vD7KFVY",
    "Sari Sacli Mavi Gozlum":      "https://www.youtube.com/watch?v=8S-D4VZXY3o",
    # --- FİLM & DİZİ ---
    "Game Of Thrones":             "https://www.youtube.com/watch?v=QtkoEFbFGiQ",
    "Pirates Of Caribbean":        "https://www.youtube.com/watch?v=27mB8verLK8",
    "Harry Potter Theme":          "https://www.youtube.com/watch?v=LylntHK8Avg",
    "Star Wars Theme":             "https://www.youtube.com/watch?v=_D0ZQPqeJkk",
    "Godfather Theme":             "https://www.youtube.com/watch?v=2KxYMVOjfHs",
    "Mission Impossible":          "https://www.youtube.com/watch?v=XAYhNHhxN0A",
    "Schindlers List":             "https://www.youtube.com/watch?v=bs-elRmLvb4",
    "Titanic My Heart Goes On":    "https://www.youtube.com/watch?v=WNIPqafd4As",
    "Lion King Circle Of Life":    "https://www.youtube.com/watch?v=GibiNy4d4gc",
    "James Bond Theme":            "https://www.youtube.com/watch?v=ySAIBhIpqgY",
    "Interstellar Theme":          "https://www.youtube.com/watch?v=UDVtMYqUAyw",
    "Forrest Gump Theme":          "https://www.youtube.com/watch?v=gYPAMwPGPsU",
    "Gladiator Now We Are Free":   "https://www.youtube.com/watch?v=yMb2OuFEaT8",
}

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
            label = f"{'▶ ' if is_active else ''}{idx + 1}. Şarkı"
            if st.button(label, key=f"song_{idx}", use_container_width=True):
                reset_game(name)
                st.rerun()

# ---------------------------------------------------
# ANA EKRAN
# ---------------------------------------------------
st.title("🎵 Melodi Dedektifi")
st.caption("Şarkıyı dinle • Harfleri tahmin et • Adını bul!")

if st.session_state.selected_song is None:
    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.info("**Nasıl Oynanır?**\n\n1. Sol panelden bir şarkı seç\n2. YouTube'dan dinle\n3. Harfleri tahmin et\n4. Şarkı adını bul!")
    with col_b:
        st.warning("**Kurallar**\n\n• 5 hakkın var\n• Yanlış harf = 1 hak\n• Yanlış isim = 1 hak\n• 0 hak = oyun bitti!")
    with col_c:
        st.success("**İpucu**\n\n• Önce harfleri tahmin et\n• Şarkıyı dikkatlice dinle\n• Rastgele butonu ile şansını dene!")
    st.stop()

song = st.session_state.selected_song
if song not in songs:
    st.session_state.selected_song = None
    st.rerun()

url = songs[song]

st.markdown("---")
st.markdown("**🎵 Şarkıyı Dinle**")

# YouTube player — autoplay kapalı, sadece ses için küçük boyut
st_player(url, playing=False, height=80)
st.session_state.game_started = True

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
