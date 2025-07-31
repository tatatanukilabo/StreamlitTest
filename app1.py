import streamlit as st
import pandas as pd

# ファイルをアップロード
uploaded_file = st.file_uploader("CSVファイルを選択してください", type="csv")

if uploaded_file is not None:
    # CSVをDataFrameとして読み込み
    df = pd.read_csv(uploaded_file)
    st.write("CSVファイルの内容:")
    st.dataframe(df)  # 表形式で表示
