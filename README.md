import streamlit as st
import pandas as pd
import random

def main():
    st.title("Excelデータランダム表示アプリ")

    uploaded_file = st.file_uploader("Excelファイルをアップロードしてください", type=["xlsx", "xls"])
    
    if uploaded_file:
        try:
            # Excelファイルを読み込む
            df = pd.read_excel(uploaded_file)

            st.write("アップロードしたExcelファイルの内容:")
            st.dataframe(df)

            # ランダムに1行を選ぶ
            if len(df) > 0:
                random_row = df.sample(n=1)  # 1行ランダムに選ぶ
                st.write("ランダムに選ばれた1行:")
                st.dataframe(random_row)
            else:
                st.warning("Excelファイルにデータがありません。")
        
        except Exception as e:
            st.error(f"ファイルの読み込みに失敗しました: {e}")

if __name__ == "__main__":
    main()
