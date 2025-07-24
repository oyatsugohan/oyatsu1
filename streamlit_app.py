import streamlit as st

st.title('漢検練習帳')

st.write('このアプリでは「漢検三級」「漢検二級」「漢検準一級」「漢検一級」の[漢字⇒よみ]　の問題が解けます！')
player_name=st.text_input('あなたの名前を教えてください！')
if player_name !=(''):
    st.write(player_name+'さんですね！')