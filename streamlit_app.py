import streamlit as st
import pandas as pd
import random


st.title('クイズを解いて敵を倒す系のやつ、レベルアップの機能を付けたい')

excel_path = "漢字リスト.xlsx"
df = pd.read_excel(excel_path, engine="openpyxl")

fixed_row_index = 0

player_name='player'
player_name=st.text_input('あなたの名前を決定してください')
st.write('あなたの名前は'+player_name+'です！')

if st.write('あなたの名前は'+player_name+'です！'):
    destination=st.text_input('向かう場所を設定してください(始まりの森(漢検三級)なら「始まりの森」)')
    st.write('始まりの森(漢検三級)')
    st.write('名称未定(漢検準二級)')
    st.write('名称未定(漢検二級)')
    st.write('名称未定(漢検準一級)')

if destination=='始まりの森':
    selected_row = df.iloc[fixed_row_index]
    column_name = random.choice(selected_row.index.tolist())
    value = selected_row[column_name]

    st.write(f"✅ 抽出結果：列 `{column_name}` の値 → **{value}**")