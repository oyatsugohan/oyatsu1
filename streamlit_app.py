import streamlit as st

st.title('英単語学習アプリ')

st.write('日本語訳を英単語に直しなさい')
st.write('難易度を選択してください')
difficulty = st.text_input ('高校１年生レベルなら１,高校２～３年生レベルなら２')
if difficulty == '１':
    st.write ('難易度：高校１年生')
    st.write (' ')
    question_1 = st.text_input('問題１　「重要な、大切な」') 
    if question_1 == '':
        st.write('入力してください')
    elif question_1 == "important":
        st.write('正解！')
        
    else:
        st.write('不正解　解答：important')
elif difficulty == '２':
    st.write('難易度：高校２～３年生')
else:
    st.write('難易度を設定してください')