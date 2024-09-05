import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Importar NumPy

# Obter a data e hora atuais
data_hora_atual = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

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

# Exibir valor total do faturamento
st.markdown(f"""
    <h2 style='text-align: center; color: #2a9d8f;'>FATURAMENTO TOTAL: R$ {soma_valor_frete_total:,.2f}</h2>
""", unsafe_allow_html=True)

# Exibir valor do faturamento filtrado
soma_valor_frete = df_filtrado['Valor do Frete'].sum()
st.markdown(f"""
    <h3 style='text-align: center; color: #e76f51;'>FATURAMENTO FILTRADO: R$ {soma_valor_frete:,.2f}</h3>
""", unsafe_allow_html=True)

# Preparar dados para gráficos
df_filtrado_grouped = df_filtrado.groupby('Tipo do Frete')['Valor do Frete'].sum().reset_index()

# Adicionar gráfico de velocímetro
def criar_velocimetro(valor, max_valor=100, tipo_frete=''):
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))

    # Dados do gráfico
    dados = [valor, max_valor - valor]
    cores = ['#FF0000', '#D3D3D3']
    
    # Criar gráfico de pizza
    wedges, texts = ax.pie(dados, colors=cores, startangle=90, wedgeprops=dict(width=0.3))
    
    # Adicionar porcentagens dentro do gráfico
    porcentagens = [f'{dado / max_valor * 100:.1f}%' for dado in dados]
    for wedge, pct in zip(wedges, porcentagens):
        ang = (wedge.theta2 - wedge.theta1) / 2. + wedge.theta1
        x = 0.4 * wedge.r * np.cos(np.radians(ang))
        y = 0.4 * wedge.r * np.sin(np.radians(ang))
        ax.text(x, y, pct, ha='center', va='center', fontsize=12, color='black')
    
    # Adicionar ponteiro
    angulo = 180 * (valor / max_valor)
    ax.annotate('', xy=(0, 0), xytext=(0, 1),
                arrowprops=dict(facecolor='black', shrink=0.05, width=2))
    
    # Configurações do gráfico
    ax.set_aspect('equal')
    plt.title(f'Em vermelho para - {tipo_frete}')

    # Adicionar limite de valores
    plt.xlim(-1.5, 1.5)
    plt.ylim(-0.5, 1.5)
    
    return fig

# Exibir gráficos de velocímetro para cada tipo de frete
for tipo_frete in df_filtrado_grouped['Tipo do Frete']:
    valor = df_filtrado_grouped[df_filtrado_grouped['Tipo do Frete'] == tipo_frete]['Valor do Frete'].values[0]
    fig = criar_velocimetro(valor, max_valor=soma_valor_frete_total, tipo_frete=tipo_frete)
    st.pyplot(fig)
