import streamlit as st

st.title('自己紹介')

st.write('汝の名を刻め')

user_name=st.text_input('名前を入力してください')

st.header('汝の名は'+str(user_name)+'だ')

h=st.number_input('身長を入力してください(m)',value=1.70)
w=st.number_input('体重を入力してください(kg)',value=70)

bmi=w/(h**2)

dbmi=round(bmi,2)

st.header('あなたのBMIは'+str(dbmi)+'です')