# word_data.py
word_dict = {
    "apple": "りんご",
    "book": "本",
    "car": "車",
    "dog": "犬",
    "elephant": "象",
    "flower": "花",
    "guitar": "ギター",
    "house": "家",
    "island": "島",
    "jacket": "上着"
}

import streamlit as st
import random
from word_data import word_dict

st.set_page_config(page_title="英単語学習アプリ", page_icon="📘")

st.title("📘 英単語学習アプリ")

# セッション状態の初期化
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.current_word = None

# 新しい単語をランダムに選択
def get_new_question():
    word, meaning = random.choice(list(word_dict.items()))
    st.session_state.current_word = (word, meaning)

# 最初の表示時
if st.session_state.current_word is None:
    get_new_question()

# 出題
current_word, current_meaning = st.session_state.current_word
st.write(f"この単語の英語は何？：**{current_meaning}**")

user_answer = st.text_input("あなたの答えを入力してください", "")

if st.button("答える"):
    st.session_state.total += 1
    if user_answer.strip().lower() == current_word.lower():
        st.success("正解！🎉")
        st.session_state.score += 1
    else:
        st.error(f"不正解！正解は **{current_word}** です。")

    get_new_question()

st.markdown("---")
st.write(f"✅ スコア: **{st.session_state.score} / {st.session_state.total}**")
