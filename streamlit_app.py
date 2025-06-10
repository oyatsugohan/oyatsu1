import streamlit as st
import pandas as pd
import random

def main():
    st.title('未定：')
    uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=["xlsx", "xls"])
    if uploaded_file:
        try:
            player_name='player'
            player_name=st.text_input('あなたの名前を決定してください')
            st.write('あなたの名前は'+player_name+'です！')

            destination=st.text_input('向かう場所を設定してください(始まりの森(漢検三級)なら「始まりの森」)')
            st.write('始まりの森(漢検三級)')
            st.write('名称未定(漢検準二級)')
            st.write('名称未定(漢検二級)')
            st.write('名称未定(漢検準一級)')
            
        except Exception as e:
            st.error(f'なんかちがーう:{e}')