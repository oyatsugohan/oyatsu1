import streamlit as st

import random

st.title('未定：')

player_name='player'
player_name=st.text_input('playerの名前を決定してください')

destination=st.text_input('向かう場所を設定してください(始まりの森(漢検三級)なら「始まりの森」)')
st.write('始まりの森(漢検三級)')
st.write('名称未定(漢検準二級)')
st.write('名称未定(漢検二級)')
st.write('名称未定(漢検準一級)')
if destination==('始まりの森'):
    