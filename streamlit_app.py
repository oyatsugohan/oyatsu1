import streamlit as st
import pandas as pd
import random
import os
from pathlib import Path

@st.cache_data
def find_and_load_excel():
    """漢字リスト.xlsxを探して読み込む"""
    possible_paths = [
        "漢字リスト.xlsx",
        str(Path.home() / "Desktop" / "漢字リスト.xlsx"),
        str(Path.home() / "Downloads" / "漢字リスト.xlsx")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                df.columns = ['難易度', '漢字', '読み']
                return df, path
            except Exception as e:
                st.error(f"ファイル読み込みエラー: {e}")
                return None, None
    
    return None, None

def get_random_kanji():
    """漢検三級の漢字をランダム選択"""
    df, file_path = find_and_load_excel()
    
    if df is None:
        return None, None, None
    
    # 漢検三級をフィルタリング
    grade_3 = df[df['難易度'] == '漢検三級']
    
    if grade_3.empty:
        return None, None, None
    
    # ランダム選択
    selected = grade_3.sample(n=1).iloc[0]
    return selected['漢字'], selected['読み'], len(grade_3)

# メイン画面
st.title("🇯🇵 漢字ランダム選択")
st.write("漢検三級の漢字をランダムに表示します")

# ファイル確認
df, file_path = find_and_load_excel()

if df is not None:
    st.success(f"✅ ファイル読み込み成功: {file_path}")
    
    # データ概要
    col1, col2 = st.columns(2)
    with col1:
        st.metric("総データ数", len(df))
    with col2:
        grade_3_count = len(df[df['難易度'] == '漢検三級'])
        st.metric("漢検三級", f"{grade_3_count}件")
    
    st.divider()
    
    # ランダム選択ボタン
    if st.button("🎲 ランダムに漢字を選ぶ", type="primary", use_container_width=True):
        kanji, reading, total = get_random_kanji()
        
        if kanji:
            # 大きく漢字を表示
            st.markdown(f"""
            <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 20px 0;">
                <h1 style="font-size: 150px; margin: 0; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    {kanji}
                </h1>
            </div>
            """, unsafe_allow_html=True)
            
            # 詳細情報
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**漢字**: {kanji}")
            with col2:
                st.info(f"**読み**: {reading}")
        else:
            st.error("漢検三級のデータが見つかりません")

else:
    st.error("❌ 漢字リスト.xlsxが見つかりません")
    st.info("""
    以下の場所にファイルを配置してください：
    - このスクリプトと同じフォルダ
    - デスクトップ
    - ダウンロードフォルダ
    """)
    
    # ファイルアップロード機能
    st.divider()
    st.subheader("📁 ファイルアップロード")
    uploaded_file = st.file_uploader("漢字リスト.xlsxをアップロード", type=['xlsx'])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df.columns = ['難易度', '漢字', '読み']
            
            st.success("✅ ファイルアップロード成功！")
            
            # アップロードファイルでの処理
            grade_3 = df[df['難易度'] == '漢検三級']
            
            if not grade_3.empty and st.button("🎲 アップロードファイルから選ぶ", type="primary"):
                selected = grade_3.sample(n=1).iloc[0]
                
                st.markdown(f"""
                <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin: 20px 0;">
                    <h1 style="font-size: 150px; margin: 0; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                        {selected['漢字']}
                    </h1>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**漢字**: {selected['漢字']}")
                with col2:
                    st.info(f"**読み**: {selected['読み']}")
        
        except Exception as e:
            st.error(f"アップロードエラー: {e}")

# サイドバー情報
with st.sidebar:
    st.header("ℹ️ 使い方")
    st.write("1. 漢字リスト.xlsxを準備")
    st.write("2. ボタンをクリック")
    st.write("3. ランダムに表示される漢字を確認")
    
    st.divider()
    st.caption("Made with Streamlit")