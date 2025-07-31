import streamlit as st
import pandas as pd
import io

# ファイルアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file:
    try:
        # 改行コード統一（CRLF, CR → LF）
        content = uploaded_file.getvalue().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
        df = pd.read_csv(io.StringIO(content))

        # ヘッダー表示（任意）
        # st.write("読み込んだ列名:", df.columns.tolist())

        # 必須列のチェック
        required_cols = ["機器", "ステップ", "計算分類", "2024", "2025", "計算値"]
        if not all(col in df.columns for col in required_cols):
            st.error("CSVのヘッダーが期待された形式ではありません。'ステップ' や '計算値' 列をご確認ください。")
        else:
            st.write("アップロードされたデータ:", df)

            # 入力フォーム生成
            for i in range(len(df)):
                st.subheader(f'{df["機器"][i]} の入力')

                # ステップ取得（0なら1に補正）
                step_raw = float(df["ステップ"][i]) if pd.notna(df["ステップ"][i]) else 0.1
                step_val = 1.0 if step_raw == 0 else step_raw

                # デフォルト値取得
                default_val = float(df["2025"][i]) if pd.notna(df["2025"][i]) else float(df["2024"][i])

                # 入力フィールド
                input_val = st.number_input(
                    f'{df["機器"][i]} の 2025 年の値',
                    value=default_val,
                    step=step_val,
                    format="%.4f",
                    key=f"input_{i}"
                )

                # 入力値をDataFrameに反映
                df.at[i, "2025"] = input_val

            # 計算ボタン
            if st.button("計算値を算出"):
                for i in range(len(df)):
                    calc_type = df["計算分類"][i]
                    if calc_type == 1:
                        df.at[i, "計算値"] = df["2025"][i] - df["2024"][i]
                    elif calc_type == 2:
                        df.at[i, "計算値"] = df["2025"][i] + df["2024"][i]
                    else:
                        df.at[i, "計算値"] = None  # その他の分類に対応（任意）

                st.write("計算後のデータ:", df)

                # CSVダウンロードボタン
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="CSVをダウンロード",
                    data=csv,
                    file_name="編集済みデータ.csv",
                    mime="text/csv"
                )

    except Exception as e:
        st.error("CSV読み込み中にエラーが発生しました。形式や改行コードをご確認ください。")
        st.exception(e)
