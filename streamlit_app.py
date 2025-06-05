import streamlit as st

import random

st.title('未定：')

player_name='player'
player_name=st.text_input('playerの名前を決定してください')

destination=st.text_input('向かう場所を設定してください')
st.write('始まりの森(漢検三級)')
if destination==(''):
    