import streamlit as st
import pandas as pd

# CSV読み込み（2024の値と機器名は含まれている前提）
uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("元データ:", df)

    # 入力用に2025列を空で準備
    df["2025"] = None

    # 行ごとに整数入力フォームを表示（step=1指定）
    for i in range(len(df)):
        input_val = st.number_input(
            f'{df["機器"][i]} の 2025 年の値を入力',
            key=f"input_{i}",
            step=1,
            format="%d"
        )
        df.at[i, "2025"] = int(input_val)

    # 差分を計算するボタン
    if st.button("差分を計算"):
        df["差分"] = df["2025"] - df["2024"]
        st.write("計算後のデータ:", df)

        # CSV出力
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("CSVをダウンロード", data=csv, file_name="差分結果.csv", mime="text/csv")
