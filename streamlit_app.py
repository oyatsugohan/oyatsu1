import streamlit as st
import pandas as pd
import random
import os
import time
import json
from datetime import datetime

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

def get_random_kanji_2nd_grade(df):
    """漢検二級の漢字からランダムに一つ選択"""
    if df is None:
        return None
    
    # 漢検二級の行をフィルタリング
    grade_2_df = df[df['難易度'] == '漢検二級']
    
    if grade_2_df.empty:
        st.warning("漢検二級のデータが見つかりません。")
        # デバッグ情報を追加
        st.write("利用可能な難易度:")
        st.write(df['難易度'].unique())
        return None
    
    # ランダムに一つ選択
    random_row = grade_2_df.sample(n=1)
    return random_row.iloc[0]

def get_random_kanji_1st_grade(df):
    """漢検一級の漢字からランダムに一つ選択"""
    if df is None:
        return None
    
    # 漢検一級の行をフィルタリング
    grade_1_df = df[df['難易度'] == '漢検一級']
    
    if grade_1_df.empty:
        st.warning("漢検一級のデータが見つかりません。")
        # デバッグ情報を追加
        st.write("利用可能な難易度:")
        st.write(df['難易度'].unique())
        return None
    
    # ランダムに一つ選択
    random_row = grade_1_df.sample(n=1)
    return random_row.iloc[0]

def calculate_required_exp(level):
    """レベルに応じて必要経験値を計算（1.3倍ずつ増加）"""
    base_exp = 100
    return int(base_exp * (1.3 ** (level - 1)))

def save_game_data():
    """ゲームデータをJSONで保存"""
    save_data = {
        "player_name": st.session_state.get('player_name', ''),
        "player_level": st.session_state.get('player_level', 1),
        "experience_points": st.session_state.get('experience_points', 0),  # 0からスタート
        "question_count": st.session_state.get('question_count', 0),
        "save_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0"
    }
    return json.dumps(save_data, ensure_ascii=False, indent=2)

def load_game_data(uploaded_file):
    """ゲームデータをJSONから読み込み"""
    try:
        # アップロードされたファイルからJSONを読み込み
        save_data = json.load(uploaded_file)
        
        # データをセッション状態に設定
        st.session_state.player_name = save_data.get('player_name', '')
        st.session_state.player_level = save_data.get('player_level', 1)
        st.session_state.experience_points = save_data.get('experience_points', 0)  # 0からスタート
        st.session_state.question_count = save_data.get('question_count', 0)
        
        return True, save_data.get('save_date', '不明')
    except Exception as e:
        return False, str(e)

def display_practice_interface(df, get_kanji_function, level_name):
    """練習インターフェースを表示する共通関数"""
    # メッセージ用のセッション状態を初期化
    if 'message' not in st.session_state:
        st.session_state.message = ""
    if 'level_up_message' not in st.session_state:
        st.session_state.level_up_message = ""
    
    # 現在のレベルの必要経験値を計算
    current_required_exp = calculate_required_exp(st.session_state.player_level)
    
    # データの概要を表示
    st.sidebar.header("プレイヤー情報")
    st.sidebar.write(f'プレイヤー名: {st.session_state.get("player_name", "未設定")}')
    st.sidebar.write(f'あなたのレベル: {st.session_state.player_level}')
    st.sidebar.write(f'経験値: {st.session_state.experience_points} / {current_required_exp}')
    st.sidebar.write(f"問題数: {st.session_state.question_count}")
    
    st.sidebar.header("データ概要")
    st.sidebar.write(f"総データ数: {len(df)}行")
    
    # 難易度別の件数を表示
    difficulty_counts = df['難易度'].value_counts()
    st.sidebar.write("難易度別件数:")
    for difficulty, count in difficulty_counts.items():
        st.sidebar.write(f"- {difficulty}: {count}件")
    
    # レベルアップメッセージを表示（優先して表示）
    if st.session_state.level_up_message:
        st.balloons()  # レベルアップエフェクト
        st.success(st.session_state.level_up_message)
        # 「OK」ボタンでメッセージを消す
        if st.button("🎉 OK", type="primary", key=f'levelup_ok_{level_name}'):
            st.session_state.level_up_message = ""
            st.rerun()
        return  # レベルアップメッセージが表示されている間は他の処理をしない
    
    # 通常のメッセージを表示
    if st.session_state.message:
        st.info(st.session_state.message)
    
    # 最初の問題を出すボタン、または次の問題へのボタン
    if not st.session_state.show_kanji:
        if st.button("🎲 最初の問題", type="primary", key=f'start_btn_{level_name}'):
            st.session_state.current_kanji = get_kanji_function(df)
            st.session_state.show_kanji = True
            st.session_state.show_answer = False
            st.session_state.question_count += 1
            st.session_state.message = ""  # メッセージをクリア
            st.rerun()
    
    # 漢字表示エリア
    if st.session_state.show_kanji and st.session_state.current_kanji is not None:
        st.markdown("---")
        
        # 大きく漢字を表示
        st.markdown(f"""
        <div style="text-align: center; padding: 40px;">
            <h1 style="font-size: 120px; margin: 0; color: #1f77b4;">
                {st.session_state.current_kanji['漢字']}
            </h1>
        </div>
        """, unsafe_allow_html=True)
        
        # 回答欄とギブアップボタンを横並びに配置
        col_input, col_giveup = st.columns([3, 1])
        
        with col_input:
            answer_1 = st.text_input('oyatsu「この漢字なんだ？(送り仮名があるときは送り仮名も含めてひらがなで答えてね)」', key=f'answer_{st.session_state.question_count}_{level_name}')
        
        with col_giveup:
            st.write("")  # 空行で位置調整
            if st.button("😵 ギブアップ", key=f'giveup_{st.session_state.question_count}_{level_name}'):
                st.session_state.message = 'oyatsu「大丈夫！次は頑張ろう！」'
                st.session_state.show_answer = True
                st.rerun()
        
        # 正解判定（一度だけ実行されるように制御）
        if answer_1 and answer_1 == st.session_state.current_kanji['読み'] and not st.session_state.show_answer:
            # 難易度に応じて経験値を設定
            difficulty = st.session_state.current_kanji['難易度']
            if difficulty == '漢検三級':
                exp_gain = 10
            elif difficulty == '漢検二級':
                exp_gain = 15
            elif difficulty == '漢検一級':
                exp_gain = 20
            else:
                exp_gain = 5  # デフォルト値
            
            st.success(f'oyatsu「正解！+{exp_gain}EXP獲得！」')
            
            # 経験値を増やす
            st.session_state.experience_points += exp_gain
            st.session_state.show_answer = True
            
            # 現在のレベルの必要経験値を取得
            current_required_exp = calculate_required_exp(st.session_state.player_level)
            
            # レベルアップ判定
            if st.session_state.experience_points >= current_required_exp:
                # レベルアップ処理
                st.session_state.player_level += 1
                
                # 余った経験値を次のレベルに繰り越し
                overflow = st.session_state.experience_points - current_required_exp
                st.session_state.experience_points = overflow
                
                # 連続レベルアップの処理
                while True:
                    new_required_exp = calculate_required_exp(st.session_state.player_level)
                    if st.session_state.experience_points >= new_required_exp:
                        st.session_state.player_level += 1
                        st.session_state.experience_points -= new_required_exp
                    else:
                        break
                
                # レベルアップメッセージを設定
                st.session_state.level_up_message = f'🎉 レベルアップ！ レベル{st.session_state.player_level}になりました！'
            
        elif answer_1 and answer_1 != st.session_state.current_kanji['読み'] and not st.session_state.show_answer:
            st.error('oyatsu「惜しい！もう一度考えてみて！」')
        
        # 詳細情報を表示（正解時またはギブアップ時）
        if st.session_state.show_answer:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("難易度", st.session_state.current_kanji['難易度'])
            
            with col2:
                st.metric("漢字", st.session_state.current_kanji['漢字'])
            
            with col3:
                st.metric("読み", st.session_state.current_kanji['読み'])
        
        # 次へボタン（正解後のみ表示）
        if st.session_state.show_answer:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("➡️ 次の問題", type="primary", key=f'next_btn_{level_name}'):
                    st.session_state.current_kanji = get_kanji_function(df)
                    st.session_state.show_answer = False
                    st.session_state.question_count += 1
                    st.session_state.message = ""  # メッセージをクリア
                    st.rerun()
            
            with col2:
                if st.button("🔄 練習終了", key=f'end_btn_{level_name}'):
                    st.session_state.show_kanji = False
                    st.session_state.current_kanji = None
                    st.session_state.show_answer = False
                    st.session_state.message = 'oyatsu「お疲れ様！今日もよく頑張ったね！」'
                    st.rerun()

# メイン画面
st.title("漢検練習帳")
st.write("???「やあ！」")
st.write('???「僕はoyatsu!　君をサポートするためにきたよ！」')

# セーブ・ロード機能
st.sidebar.header("💾 セーブ・ロード")

# セーブ機能
if st.sidebar.button("📥 セーブデータ作成"):
    save_json = save_game_data()
    st.sidebar.download_button(
        label="⬇️ セーブファイルをダウンロード",
        data=save_json,
        file_name=f"kanji_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )
    st.sidebar.success("セーブデータを作成しました！")

# ロード機能
uploaded_file = st.sidebar.file_uploader(
    "📁 セーブファイルを選択",
    type=['json'],
    help="以前保存したセーブファイル(.json)をアップロードしてください"
)

if uploaded_file is not None:
    success, message = load_game_data(uploaded_file)
    if success:
        st.sidebar.success(f"✅ データを読み込みました！\n保存日時: {message}")
        st.rerun()
    else:
        st.sidebar.error(f"❌ データの読み込みに失敗しました: {message}")

st.sidebar.markdown("---")

# プレイヤー名入力
if 'player_name' not in st.session_state:
    st.session_state.player_name = ''

player_name = st.text_input(
    'oyatsu「君の名前を教えてほしいな」', 
    value=st.session_state.player_name,
    key='player_name_input'
)

# プレイヤー名をセッション状態に保存
if player_name != st.session_state.player_name:
    st.session_state.player_name = player_name

if player_name != '':
    st.write('oyatsu「'+player_name + 'っていうのかぁ')
    st.write('oyatsu「これからよろしくね！' + player_name + '」！')
    st.write('oyatsu「今日は何しようか？」')
    
    # セッション状態の初期化
    if 'selected_level' not in st.session_state:
        st.session_state.selected_level = None
    if 'show_kanji' not in st.session_state:
        st.session_state.show_kanji = False
    if 'current_kanji' not in st.session_state:
        st.session_state.current_kanji = None
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    if 'question_count' not in st.session_state:
        st.session_state.question_count = 0
    if 'player_level' not in st.session_state:
        st.session_state.player_level = 1
    if 'experience_points' not in st.session_state:
        st.session_state.experience_points = 0  # 0からスタート
    
    # ボタンの配置
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button('漢検三級', key='level3'):
            st.session_state.selected_level = '三級'
            st.session_state.show_kanji = False
            st.session_state.current_kanji = None
            st.session_state.show_answer = False
            st.session_state.question_count = 0
    
    with col2:
        if st.button('漢検二級', key='level2'):
            st.session_state.selected_level = '二級'
            st.session_state.show_kanji = False
            st.session_state.current_kanji = None
            st.session_state.show_answer = False
            st.session_state.question_count = 0
    
    with col3:
        if st.button('漢検一級', key='level1'):
            st.session_state.selected_level = '一級'
            st.session_state.show_kanji = False
            st.session_state.current_kanji = None
            st.session_state.show_answer = False
            st.session_state.question_count = 0
    
    # データ読み込み
    df = load_kanji_data()
    
    if df is not None:
        # 選択されたレベルに応じて処理
        if st.session_state.selected_level == '三級':
            st.write('oyatsu「漢検三級だね。OK　任せてよ！」')
            display_practice_interface(df, get_random_kanji_3rd_grade, '三級')
        
        elif st.session_state.selected_level == '二級':
            st.write('oyatsu「漢検二級だね。OK　任せてよ！」')
            display_practice_interface(df, get_random_kanji_2nd_grade, '二級')
        
        elif st.session_state.selected_level == '一級':
            st.write('oyatsu「漢検一級だね。OK　任せてよ！」')
            display_practice_interface(df, get_random_kanji_1st_grade, '一級')