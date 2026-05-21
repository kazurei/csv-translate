import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from tqdm import tqdm
import time

st.set_page_config(page_title="CSV翻訳ツール", layout="wide")

st.title("CSV content列 日本語翻訳ツール")

uploaded_file = st.file_uploader(
    "英語レビューCSVをアップロード",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.write("読み込み完了")
    st.write(df.head())

    if "content" not in df.columns:
        st.error("content列が見つかりません")
    else:

        if st.button("翻訳開始"):

            progress = st.progress(0)
            translated = []

            contents = df["content"].fillna("").tolist()

            for i, text in enumerate(contents):

                try:
                    ja = GoogleTranslator(
                        source='en',
                        target='ja'
                    ).translate(text)

                except Exception:
                    ja = text

                translated.append(ja)

                progress.progress((i + 1) / len(contents))

                # API負荷軽減
                time.sleep(0.1)

            df["content"] = translated

            csv = df.to_csv(
                index=False,
                encoding="utf-8-sig"
            ).encode("utf-8-sig")

            st.success("翻訳完了")

            st.download_button(
                label="日本語CSVをダウンロード",
                data=csv,
                file_name="reviews_japanese.csv",
                mime="text/csv"
            )