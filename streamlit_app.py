# word_data.pyimport streamlit as st
import random

# -----------------------
# 単語データ（英語: 日本語）
# -----------------------
word_list = [
    {"english": "apple", "japanese": "りんご"},
    {"english": "book", "japanese": "本"},
    {"english": "car", "japanese": "車"},
    {"english": "dog", "japanese": "犬"},
    {"english": "elephant", "japanese": "象"},
    {"english": "flower", "japanese": "花"},
    {"english": "guitar", "japanese": "ギター"},
    {"english": "house", "japanese": "家"},
    {"english": "island", "japanese": "島"},
    {"english": "jacket", "japanese": "上着"}
]

# -----------------------
# 初期化
# -----------------------
st.set_page_config(page_title="英単語学習アプリ", page_icon="📘")

if "word" not in st.session_state:
    st.session_state.word = random.choice(word_list)
if "score" not in st.session_state:
    st.session_state.score = 0
if "total" not in st.session_state:
    st.session_state.total = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None

st.title("📘 英単語学習アプリ")

# -----------------------
# 出題
# -----------------------
st.markdown("### この日本語に対応する英単語は？")
st.markdown(f"👉 **{st.session_state.word['japanese']}**")

user_input = st.text_input("英語で入力してください")

# -----------------------
# 判定
# -----------------------
if st.button("答える"):
    st.session_state.total += 1
    if user_input.strip().lower() == st.session_state.word["english"].lower():
        st.success("正解！🎉")
        st.session_state.score += 1
        st.session_state.last_result = "correct"
    else:
        st.error(f"不正解... 正解は **{st.session_state.word['english']}** です。")
        st.session_state.last_result = "incorrect"

# -----------------------
# 次の問題へ
# -----------------------
if st.button("次の問題へ"):
    st.session_state.word = random.choice(word_list)
    st.session_state.last_result = None
    st.experimental_rerun()

# -----------------------
# スコア表示
# -----------------------
st.markdown("---")
st.metric(label="正解数 / 出題数", value=f"{st.session_state.score} / {st.session_state.total}")

