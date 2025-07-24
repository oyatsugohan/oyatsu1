import streamlit as st
import pandas as pd
import random
import os
import time

def load_kanji_data():
    """漢字リスト.xlsxを読み込む"""
    try:
        # ファイルパスを指定（現在のディレクトリにある場合）
        file_path = "漢字リスト.xlsx"
        
        # ファイルが存在するかチェック
        if not os.path.exists(file_path):
            st.error(f"ファイル '{file_path}' が見つかりません。")
            st.info("ファイルをこのPythonスクリプトと同じフォルダに配置してください。")
            return None
        
        # Excelファイルを読み込み
        df = pd.read_excel(file_path)
        
        # 列数に応じて処理を分岐（修正点）
        if len(df.columns) >= 3:
            # 最初の3列のみを取得して列名を設定
            df_selected = df.iloc[:, :3].copy()
            df_selected.columns = ['難易度', '漢字', '読み']
            return df_selected
        else:
            st.error("Excelファイルの列数が不足しています。")
            return None
            
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
        # デバッグ情報を追加
        st.write("利用可能な難易度:")
        st.write(df['難易度'].unique())
        return None
    
    # ランダムに一つ選択
    random_row = grade_3_df.sample(n=1)
    return random_row.iloc[0]

# メイン画面
st.title("漢検練習帳")
st.write("???「やあ！」")
st.write('???「僕はoyatsu!　君をサポートするためにきたよ！」')

player_name = st.text_input('oyatsu「君の名前を教えてほしいな」')

if player_name != '':
    st.write('oyatsu「'+player_name + 'っていうのかぁ')
    st.write('oyatsu「これからよろしくね！' + player_name + '」！')
    st.write('oyatsu「今日は何しようか？」')
    
    # セッション状態の初期化（修正点）
    if 'selected_level' not in st.session_state:
        st.session_state.selected_level = None
    if 'show_kanji' not in st.session_state:
        st.session_state.show_kanji = False
    
    # ボタンの配置
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button('漢検三級', key='level3'):
            st.session_state.selected_level = '三級'
            st.session_state.show_kanji = False  # リセット
    
    with col2:
        if st.button('漢検二級', key='level2'):
            st.session_state.selected_level = '二級'
    
    # 漢検三級が選択された場合の処理
    if st.session_state.selected_level == '三級':
        st.write('oyatsu「OK！　任せてよ！」')
        
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
                if st.button("🎲 ランダム表示", type="primary", key='random_btn'):
                    st.session_state.show_kanji = True
            
            with col1:
                if st.button("🔄 リセット", key='reset_btn'):
                    st.session_state.show_kanji = False
                    st.rerun()
            
            # 漢字表示エリア
            if st.session_state.show_kanji:
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
                    answer_1=st.text_input('oyatsu「この漢字なんだ？(送り仮名があるときは送り仮名も含めてひらがなで答えてね)」')
                    if answer_1 = random_kanji_data['読み']
                        st.write('oyatsu「正解！」')
                        # 詳細情報を表示
                        col1, col2, col3 = st.columns(3)
                    
                        with col1:
                            st.metric("難易度", random_kanji_data['難易度'])
                    
                        with col2:
                            st.metric("漢字", random_kanji_data['漢字'])
                    
                        with col3:
                            st.metric("読み", random_kanji_data['読み'])
    
    # 漢検二級が選択された場合の処理
    elif st.session_state.selected_level == '二級':
        st.write('oyatsu「ごめん！それは今製作中なんだ。乞うご期待（笑）！」')