import streamlit as st
import random
import pandas as pd


st.title('クイズを解いて敵を倒す系のやつ、レベルアップの機能を付けたい')

player_name=st.text_input('あなたの名前を決定してください')
if player_name:
    st.write('あなたの名前は'+player_name+'です！')
else:
    st.write('名前を入力してください')

st.write('向かう向かう場所を選んでください')
col_1,col_2,col_3,col_4 = st.columns(4)

with col_1:
    if st.button('始まりの森(漢検三級)'):
        st.session_state.action = 'question_1'
        
with col_2:
    if st.button('未定(漢検二級)'):
        st.session_state.action = 'question_2'

with col_3:
    if st.button('未定(漢検準一級)'):
        st.session_state.action = 'question_3'

with col_4:
    if st.button('未定(漢検一級)'):
        st.session_state.action = 'question_4'


if st.session_state.action == 'question_1':
        if file_method == "プロジェクトフォルダ内のファイル":
        # 現在のディレクトリ内のExcelファイルのみを検索（サブフォルダは除外）
        excel_files = glob.glob("*.xlsx") + glob.glob("*.xls")
        
        if excel_files:
            selected_file = ("漢字リスト.elsx", excel_files)
            
            if selected_file:
                try:
                    # プロジェクトフォルダ内のExcelファイルを読み込み
                    df = pd.read_excel(selected_file)
                    st.success(f"ファイル '{selected_file}' を読み込みました")
                except Exception as e:
                    st.error(f"ファイル読み込みエラー: {str(e)}")
                    return
        else:
            st.warning("プロジェクトフォルダ内にExcelファイル(.xlsx, .xls)が見つかりません")
            st.info("Excelファイルを以下の場所に配置してください：")
            
            # ファイル配置のヒント
            st.info("💡 ファイル配置のヒント：")
            st.write("- Streamlitアプリ(.py)と同じフォルダに配置")
            st.write("- 対応形式: .xlsx, .xls")
            st.write("- サブフォルダ内のファイルは検索されません")
    
    else:  # ファイルアップロード
        uploaded_file = st.file_uploader("Excelファイルを選択してください", type=['xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                # Excelファイルを読み込み
                df = pd.read_excel(uploaded_file)
            except Exception as e:
                st.error(f"ファイル読み込みエラー: {str(e)}")
                return
    
    if df is not None:
            
            # 列名を標準化（列の位置で判断）
            if len(df.columns) >= 3:
                df.columns = ['難易度', '漢字', '読み'] + list(df.columns[3:])
            else:
                st.error("Excelファイルには最低3列（難易度、漢字、読み）が必要です")
                return
            
            st.subheader("データプレビュー")
            st.dataframe(df.head())
            
            # 漢検三級のデータをフィルタリング
            kanken_3_df = df[df['難易度'] == '漢検三級']
            
            st.subheader("漢検三級のデータ")
            st.write(f"漢検三級の問題数: {len(kanken_3_df)}問")
            
            if not kanken_3_df.empty:
                st.dataframe(kanken_3_df)
                
    question, answer = random.choice(question_data)
    st.write(f"問題: {question}")
# 問題の表示
    st.write(f"問題: {question}")

# ユーザーの解答入力
    user_answer = st.text_input("答えを入力してください:")

# 解答の確認
    if st.button("回答する"):
        if user_answer == str(answer): # str() で型を合わせる
            st.write('正解！')
        else:
            st.write('不正解…　　　正解は'+str(answer))

