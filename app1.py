import streamlit as st
import pandas as pd
import io

# CSV読み込み
uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file:
    try:
        content = uploaded_file.getvalue().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        df = pd.read_csv(io.StringIO(content))

        st.write("読み込んだ列名:", df.columns.tolist())

        required_cols = ["機器", "ステップ", "計算分類", "2024", "2025", "差分"]
        if not all(col in df.columns for col in required_cols):
            st.error("CSVのヘッダーが期待された形式ではありません。")
        else:
            st.write("アップロードされたデータ:", df)

            for i in range(len(df)):
                st.subheader(f'{df["機器"][i]} の入力')

                # ステップ取得（0なら1.0に補正、またはそのまま使用）
                step_raw = float(df["ステップ"][i]) if pd.notna(df["ステップ"][i]) else 0.1
                step_val = 1.0 if step_raw == 0 else step_raw

                default_val = float(df["2025"][i]) if pd.notna(df["2025"][i]) else float(df["2024"][i])
                input_val = st.number_input(
                    f'{df["機器"][i]} の 2025 年の値',
                    value=default_val,
                    step=step_val,
                    format="%.4f",
                    key=f"input_{i}"
                )
                df.at[i, "2025"] = input_val

            if st.button("差分を計算"):
                for i in range(len(df)):
                    calc_type = df["計算分類"][i]
                    if calc_type == 1:
                        df.at[i, "差分"] = df["2025"][i] - df["2024"][i]
                    elif calc_type == 2:
                        df.at[i, "差分"] = df["2025"][i] + df["2024"][i]

                st.write("計算後のデータ:", df)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "CSVをダウンロード",
                    data=csv,
                    file_name="編集済み差分データ.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error("CSV読み込み中にエラーが発生しました。形式や改行コードを確認してください。")
        st.exception(e)
