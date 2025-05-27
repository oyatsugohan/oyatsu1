import streamlit as st
import random

# タイトル
st.title("📚 英単語学習アプリ")

# 単語リスト（辞書形式）
word_dict = {
    "りんご": "apple",
    "本": "book",
    "犬": "dog",
    "猫": "cat",
    "家": "house",
    "机": "desk",
    "学校": "school"
}

# セッション状態の初期化
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    st.session_state.question = random.choice(list(word_dict.items()))

# 現在の問題
jp_word, correct_answer = st.session_state.question

st.write(f"次の日本語の英語は？ 👉 **{jp_word}**")

# 入力フォーム
answer = st.text_input("あなたの答え（英語）を入力してください", "")

# ボタンを押すと判定
if st.button("答える"):
    if answer.strip().lower() == correct_answer:
        st.success("✅ 正解！")
        st.session_state.score += 1
    else:
        st.error(f"❌ 不正解。正解は **{correct_answer}** でした。")

    # 次の問題に更新
    st.session_state.question = random.choice(list(word_dict.items()))

# スコア表示
st.write(f"現在のスコア：**{st.session_state.score}** 点")