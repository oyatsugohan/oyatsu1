import streamlit as st

st.title('英単語学習アプリ')

st.write('難易度を選択してください')
difficulty = st.text_input ('簡単ならeasy,難しめならdifficult')
if difficulty == 'easy':
    st.write ('難易度：easy')
else:
    st.write('難易度：difficult')