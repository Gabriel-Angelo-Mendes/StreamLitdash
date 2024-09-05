import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Título do Dashboard
st.header('DASHBOARD FATURAMENTO')

# Obter a data e hora atuais
data_hora_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
st.caption('Painel atualizado em tempo real, dados extraídos da opção 455 AEH no sistema SSW, refletindo informações do mês vigente.')

# Carregar e processar o DataFrame
df = pd.read_excel(fr'R:\Controladoria\108. Gabriel\aehminuto\resultado.xlsx')

# Substituir tipos de frete por valores consolidados
df['Tipo do Frete'] = df['Tipo do Frete'].replace({
    'FP': 'FOB',
    'FV': 'FOB',
    'CP': 'CIF',
    'CV': 'CIF'
})

# Remover linhas com tipos de baixa indesejados
df = df[~df['Tipo de Baixa'].isin(['CANCELADO', 'LIQU OCOR'])]

# Remover colunas que não contêm dados
colunas_brancas = [col for col in df.columns if df[col].isnull().all()]
df = df.drop(columns=colunas_brancas)

# Corrigir formato dos valores de frete
df['Valor do Frete'] = df['Valor do Frete'].astype(str).str.replace(',', '.')
df['Valor do Frete'] = pd.to_numeric(df['Valor do Frete'], errors='coerce')

# Calcular a soma total do faturamento
soma_valor_frete_total = df['Valor do Frete'].sum()

# Limpar espaços extras na coluna 'Tipo do Frete'
df['Tipo do Frete'] = df['Tipo do Frete'].astype(str).str.strip()

# Barra lateral de filtros
st.sidebar.header('Filtros')

# Filtros de ano e mês
ano_selecionado = st.sidebar.selectbox('Selecione o Ano', sorted(df['2024'].dropna().unique()))
mes_selecionado = st.sidebar.selectbox('Selecione o Mês', sorted(df['Setembro'].dropna().unique()))

# Converter valores literais "NaN" em valores reais NaN e remover NaNs
df['Tipo do Frete'].replace('nan', pd.NA, inplace=True)
tipo_frete_selecionado = st.sidebar.selectbox('Selecione o Tipo de Frete', sorted(df['Tipo do Frete'].dropna().unique()))

# Filtrar dados com base nas seleções
df_filtrado = df[
    (df['2024'] == ano_selecionado) &
    (df['Setembro'] == mes_selecionado) &
    (df['Tipo do Frete'] == tipo_frete_selecionado)
]

# Exibir data e hora na barra lateral
st.sidebar.text(data_hora_atual)

# Exibir valor total do faturamento com tamanho maior
st.markdown(f"""
    <h2 style='text-align: center; color: #2a9d8f; font-size: 38px;'>FATURAMENTO TOTAL: R$ {soma_valor_frete_total:,.2f}</h2>
""", unsafe_allow_html=True)

# Exibir valor do faturamento filtrado com o nome do tipo de frete
soma_valor_frete = df_filtrado['Valor do Frete'].sum()
st.markdown(f"""
    <h3 style='text-align: center; color: #e76f51; font-size: 28px;'>FATURAMENTO {tipo_frete_selecionado}: R$ {soma_valor_frete:,.2f}</h3>
""", unsafe_allow_html=True)
