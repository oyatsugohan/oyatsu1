import streamlit as st
import pandas as pd
import random


st.title('クイズを解いて敵を倒す系のやつ、レベルアップの機能を付けたい')

player_name='player'
player_name=st.text_input('あなたの名前を決定してください')
st.write('あなたの名前は'+player_name+'です！')

if st.write('あなたの名前は'+player_name+'です！'):
    destination=st.text_input('向かう場所を設定してください(始まりの森(漢検三級)なら「始まりの森」)')
    st.write('始まりの森(漢検三級)')
    st.write('名称未定(漢検準二級)')
    st.write('名称未定(漢検二級)')
    st.write('名称未定(漢検準一級)')

enemy_1=('コボルト','ゴブリン','スライム')
excel_path = "漢字リスト.xlsx"  # 例: 同じディレクトリにある場合
#excel_path = "data/漢字リスト.xlsx"  # 例: dataフォルダ内にある場合

# Excelファイルから問題と正解を読み込む関数
@st.cache_data  # データをキャッシュして、再読み込みを避ける
def load_questions(excel_path):
    try:
        df = pd.read_excel(excel_path, engine="openpyxl")  # openpyxl エンジンを指定
        # '問題文' と '正解' という列名があることを前提
        questions = df['問題文'].tolist()
        answers = df['正解'].tolist()
        return list(zip(questions, answers)) # 問題と解答をペアにしたリストを返す
    except FileNotFoundError:
        st.error(f"エラー: ファイル '{excel_path}' が見つかりません。")
        return []  # 空のリストを返すことで、エラー時の処理を行う
    except KeyError as e:
        st.error(f"エラー: Excelファイルに列 '{e}' がありません。問題文と正解という列名があることを確認してください。")
        return []
    except Exception as e: # その他のエラー
        st.error(f"Excelファイルの読み込み中にエラーが発生しました: {e}")
        return []


# アプリケーションのタイトル
st.title("漢字クイズ")

# 問題と解答の読み込み
question_data = load_questions(excel_path)

if not question_data:
    st.stop() # 問題が読み込めなかった場合は、ここでアプリを停止

# 問題と解答のペアをランダムに選択
question, answer = random.choice(question_data)

# 問題の表示
st.write(f"問題: {question}")

# ユーザーの解答入力
user_answer = st.text_input("答えを入力してください:")

# 解答の確認
if st.button("回答する"):
    if user_answer == str(answer): # str() で型を合わせる
        st.write('正解！')