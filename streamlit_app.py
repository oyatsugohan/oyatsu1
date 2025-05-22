import streamlit

st.title('あいうえお')

st.write('aaaa')

user_name=st.text_imput('名前を入力してください')

st.header('あなたの名前は'+str(user_name)+'です')