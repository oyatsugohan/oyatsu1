import streamlit as st
import pandas as pd
import random

st.title("漢字ランダム選択")

# ファイルアップロード
file = st.file_uploader("漢字リスト.xlsxをアップロード", type='xlsx')

if file:
    df = pd.read_excel(file)
    df.columns = ['難易度', '漢字', '読み']
    
    # 漢検三級のみ
    data = df[df['難易度'] == '漢検三級']
    
    if st.button("ランダム選択"):
        result = data.sample(1).iloc[0]
        st.write(f"## {result['漢字']}")
        st.write(f"読み: {result['読み']}")