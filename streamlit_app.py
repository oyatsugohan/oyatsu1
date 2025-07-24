import streamlit as st

st.title('漢検練習帳')

player_name=st.text_input('あなたの名前を教えてください！')
st.write(player_name+'さんですね！')