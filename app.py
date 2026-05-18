import streamlit as st
import random
from urllib.parse import quote

st.set_page_config(page_title="Melodi Dedektifi", page_icon="🎵", layout="wide")

# ---------------------------------------------------
# BASE URL
# ---------------------------------------------------
BASE = "https://raw.githubusercontent.com/sadettindogan/melodica1/main/assets"

def mp3_url(filename):
    return f"{BASE}/{quote(filename)}"

# ---------------------------------------------------
# ŞARKILAR — { "Görünen İsim": "dosya_adi.mp3" }
# ---------------------------------------------------
songs = {
    "Game Of Thrones":           mp3_url("Game Of Thrones.mp3"),
    "Harry Potter":              mp3_url("Harry Potter.mp3"),
    "Pirates Of The Caribbean":  mp3_url("Pirates of the Caribbean.mp3"),
    "Star Wars":                 mp3_url("Star Wars.mp3"),
    "The Godfather":             mp3_url("The Godfather.mp3"),
}

categories = {
    "🎬 Film & Dizi": list(songs.keys()),
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
st.sidebar.caption(f"{len(songs)} enstrümantal parça • Sözsüz")

if st.sidebar.button("🎲 Rastgele Seç", use_container_width=True):
    reset_game(random.choice(song_names))
    st.rerun()

st.sidebar.markdown("---")

for cat_name, cat_songs in categories.items():
    with st.sidebar.expander(cat_name, expanded=True):
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
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("**🎵 Müziği Dinle**")
with col2:
    if st.button("▶️ Çal", use_container_width=True):
        st.session_state.game_started = True

if st.session_state.game_started:
    st.audio(url, format="audio/mp3")
else:
    st.info("▶️ Müziği dinlemek için **Çal** butonuna bas, sonra tahmin et!")
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
