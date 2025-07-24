import streamlit as st
import pandas as pd
import random
import os
from pathlib import Path

def load_kanji_data():
    """漢字リスト.xlsxを読み込む"""
    try:
        # 複数のファイルパスを試行
        possible_paths = [
            "漢字リスト.xlsx",
            "./漢字リスト.xlsx",
            str(Path.home() / "Desktop" / "漢字リスト.xlsx"),
            str(Path.home() / "Downloads" / "漢字リスト.xlsx")
        ]
        
        file_path = None
        for path in possible_paths:
            if os.path.exists(path):
                file_path = path
                break
        
        if file_path is None:
            st.error("ファイル '漢字リスト.xlsx' が見つかりません。")
            st.info("以下の場所にファイルを配置してください：")
            st.info("- このスクリプトと同じフォルダ")
            st.info("- デスクトップ")
            st.info("- ダウンロードフォルダ")
            return None
        
        # Excelファイルを読み込み
        df = pd.read_excel(file_path)
        
        # 列名を確認・設定
        expected_columns = ['難易度', '漢字', '読み']
        if len(df.columns) >= 3:
            df.columns = expected_columns[:len(df.columns)]
        else:
            st.error("Excelファイルの列数が不足しています。")
            return None
            
        return df
        
    except Exception as e:
        st.error(f"ファイル読み込みエラー: {str(e)}")
        return None

def get_random_kanji_3rd_grade(df):
    """漢検三級の漢字からランダムに一つ選択"""
    if df is None:
        return None
    
    # 漢検三級の行をフィルタリング
    grade_3_df = df[df['難易度'] == '漢検三級']
    
    if grade_3_df.empty:
        st.warning("漢検三級のデータが見つかりません。")
        return None
    
    # ランダムに一つ選択
    random_row = grade_3_df.sample(n=1)
    return random_row.iloc[0]

def main():
    st.title("🇯🇵 漢検三級 漢字ランダム表示")
    st.write("漢検三級の漢字をランダムに表示します")
    
    # データ読み込み
    df = load_kanji_data()
    
    if df is not None:
        # データの概要を表示
        st.sidebar.header("データ概要")
        st.sidebar.write(f"総データ数: {len(df)}行")
        
        # 難易度別の件数を表示
        difficulty_counts = df['難易度'].value_counts()
        st.sidebar.write("難易度別件数:")
        for difficulty, count in difficulty_counts.items():
            st.sidebar.write(f"- {difficulty}: {count}件")
        
        # メインコンテンツ
        col1, col2 = st.columns([2, 1])
        
        with col2:
            if st.button("🎲 ランダム表示", type="primary"):
                st.session_state.show_kanji = True
        
        with col1:
            if st.button("🔄 リセット"):
                st.session_state.show_kanji = False
                st.rerun()
        
        # 漢字表示エリア
        if hasattr(st.session_state, 'show_kanji') and st.session_state.show_kanji:
            random_kanji_data = get_random_kanji_3rd_grade(df)
            
            if random_kanji_data is not None:
                st.markdown("---")
                
                # 大きく漢字を表示
                st.markdown(f"""
                <div style="text-align: center; padding: 40px;">
                    <h1 style="font-size: 120px; margin: 0; color: #1f77b4;">
                        {random_kanji_data['漢字']}
                    </h1>
                </div>
                """, unsafe_allow_html=True)
                
                # 詳細情報を表示
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("難易度", random_kanji_data['難易度'])
                
                with col2:
                    st.metric("漢字", random_kanji_data['漢字'])
                
                with col3:
                    st.metric("読み", random_kanji_data['読み'])
    
    else:
        st.info("📁 「漢字リスト.xlsx」ファイルを準備してからアプリを実行してください。")

if __name__ == "__main__":
    main()