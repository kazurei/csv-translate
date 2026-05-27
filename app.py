import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import time
import os

st.title("Excel翻訳ツール")

SAVE_FILE = "translated_reviews.xlsx"

uploaded_file = st.file_uploader(
    "Excelファイルをアップロード",
    type=["xlsx"]
)

if uploaded_file:

    # 再開用
    if os.path.exists(SAVE_FILE):
        df = pd.read_excel(SAVE_FILE)
        st.success("途中データを読み込みました")
    else:
        df = pd.read_excel(uploaded_file)

        if "content_ja" not in df.columns:
            df["content_ja"] = ""

    st.write(df.head())

    untranslated = df["content_ja"].fillna("") == ""
    remaining = untranslated.sum()

    st.write(f"残り {remaining} 件")

    BATCH_SIZE = st.slider(
        "1回の翻訳件数",
        10,
        200,
        50
    )

    if st.button("翻訳開始"):

        targets = df[untranslated].head(BATCH_SIZE).index

        progress = st.progress(0)

        for count, idx in enumerate(targets):

            text = str(df.loc[idx, "content"])

            try:
                ja = GoogleTranslator(
                    source='en',
                    target='ja'
                ).translate(text)

            except Exception:
                ja = text

            df.loc[idx, "content_ja"] = ja

            progress.progress((count + 1) / len(targets))

            time.sleep(0.3)

        # Excel保存
        df.to_excel(
            SAVE_FILE,
            index=False
        )

        st.success("保存完了")

    # ダウンロード
    if os.path.exists(SAVE_FILE):

        with open(SAVE_FILE, "rb") as f:

            st.download_button(
                "翻訳済みExcelをダウンロード",
                data=f,
                file_name="reviews_japanese.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )