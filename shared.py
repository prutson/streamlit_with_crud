import streamlit as st
import pandas as pd
from datetime import datetime

class DefaultConfig:
    def __init__(self):
        years = list(range(2023, 2016, -1))
        self.year = st.sidebar.selectbox('Ano', years)

        # Pega os dois últimos dígitos do ano
        year_suffix = str(self.year)[-2:]

        # Constrói o nome do arquivo baseado no ano selecionado
        file_name = f"datasets/CLEAN_FIFA{year_suffix}_official_data.csv"

        if 'data' not in st.session_state or st.session_state['last_loaded_year'] != self.year:
            df_data = pd.read_csv(file_name, index_col=0)
            df_data = df_data[df_data['Contract Valid Until'] >= datetime.today().year]
            df_data = df_data[df_data['Value(£)'] > 0]
            df_data = df_data.sort_values(by='Overall', ascending=False)
            st.session_state['data'] = df_data
            st.session_state['last_loaded_year'] = self.year  # Guarda o ano do arquivo carregado
        self.df_data = st.session_state['data']