import streamlit as st
import pandas as pd

st.title("📋 CSV列編集ツール")

# CSVアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("🛠 データを編集してください")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    st.subheader("💾 編集内容をCSVとして保存")
    csv = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="更新されたCSVをダウンロード",
        data=csv,
        file_name="updated_data.csv",
        mime="text/csv"
    )
else:
    st.info("まずはCSVファイルをアップロードしてください。")
