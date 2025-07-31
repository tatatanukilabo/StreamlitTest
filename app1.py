import streamlit as st
import pandas as pd

st.title("📊 CSV編集ツール")

# CSVアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 現在のデータ")
    st.dataframe(df)

    # 新しい行を追加する入力フォーム
    st.subheader("➕ 新しい行を追加")
    new_data = {}
    with st.form("new_row_form"):
        for column in df.columns:
            new_data[column] = st.text_input(f"{column}")
        submitted = st.form_submit_button("追加")

    # 追加されたらDataFrameに統合して表示
    if submitted:
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)
        st.success("新しい行が追加されました！")
        st.dataframe(df)

    # CSVとして保存・ダウンロード
    st.subheader("💾 編集内容を保存")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="更新されたCSVをダウンロード",
        data=csv,
        file_name="updated_data.csv",
        mime="text/csv"
    )
else:
    st.info("まずはCSVファイルをアップロードしてください。")
