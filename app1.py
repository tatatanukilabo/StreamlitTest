import streamlit as st
import pandas as pd

# CSV読み込み
uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 必須列が揃っているか確認
    required_cols = ["機器", "小数点以下", "計算分類", "2024", "2025", "差分"]
    if not all(col in df.columns for col in required_cols):
        st.error("CSVのヘッダーが期待された形式ではありません。")
    else:
        st.write("アップロードされたデータ:", df)

        # 入力フォーム（2025列だけを編集）
        for i in range(len(df)):
            st.subheader(f'{df["機器"][i]} の入力')

            # 小数点ステップを "小数点以下" の値から動的に設定（例：0.1, 0.01 など）
            step_val = float(df["小数点以下"][i]) if pd.notna(df["小数点以下"][i]) else 0.1

            # 入力フォームの表示（初期値がなければ2024を使う）
            default_val = float(df["2025"][i]) if pd.notna(df["2025"][i]) else float(df["2024"][i])
            input_val = st.number_input(
                f'{df["機器"][i]} の 2025 年の値',
                value=default_val,
                step=step_val,
                format="%.4f",
                key=f"input_{i}"
            )
            df.at[i, "2025"] = input_val

        # 差分計算ボタン
        if st.button("差分を計算"):
            for i in range(len(df)):
                calc_type = df["計算分類"][i]
                if calc_type == 1:
                    df.at[i, "差分"] = df["2025"][i] - df["2024"][i]
                elif calc_type == 2:
                    df.at[i, "差分"] = df["2025"][i] + df["2024"][i]

            st.write("計算後のデータ:", df)

            # CSV出力
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "CSVをダウンロード",
                data=csv,
                file_name="編集済み差分データ.csv",
                mime="text/csv"
            )
