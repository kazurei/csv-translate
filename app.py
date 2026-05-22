import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import time
import os

st.set_page_config(page_title="CSV翻訳ツール", layout="wide")

st.title("CSV content列 日本語翻訳ツール")

uploaded_file = st.file_uploader(
    "CSVをアップロード",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.write(f"レビュー数: {len(df)}")

    if "content" not in df.columns:
        st.error("content列がありません")
        st.stop()

    if st.button("翻訳開始"):

        # 保存用列
        if "content_ja" not in df.columns:
            df["content_ja"] = ""

        progress = st.progress(0)
        status = st.empty()

        total = len(df)

        SAVE_EVERY = 100

        for i in range(total):

            # 既に翻訳済みならスキップ
            if pd.notna(df.loc[i, "content_ja"]) and df.loc[i, "content_ja"] != "":
                continue

            text = str(df.loc[i, "content"])

            try:
                ja = GoogleTranslator(
                    source='en',
                    target='ja'
                ).translate(text)

            except Exception as e:
                ja = text
                st.warning(f"{i}行目でエラー")

            df.loc[i, "content_ja"] = ja

            # 進捗表示
            progress.progress((i + 1) / total)
            status.text(f"{i+1}/{total} 件 翻訳中")

            # 一定件数ごとに自動保存
            if i % SAVE_EVERY == 0:

                df.to_csv(
                    "translated_backup.csv",
                    index=False,
                    encoding="utf-8-sig"
                )

            # 制限回避
            time.sleep(0.2)

        # 最終保存
        output_file = "reviews_japanese.csv"

        df.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )

        with open(output_file, "rb") as f:
            st.download_button(
                "日本語CSVをダウンロード",
                f,
                file_name=output_file,
                mime="text/csv"
            )

        st.success("完了")