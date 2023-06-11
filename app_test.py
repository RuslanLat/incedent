import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("Загрузите файл", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.split(".")[-1] == "csv":
        df = pd.read_csv(uploaded_file)
        st.write(df)
    else:
        df = pd.read_excel(uploaded_file)
        st.write(df)