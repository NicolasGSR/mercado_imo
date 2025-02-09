# -*- coding: utf-8 -*-
"""mercado_imo.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1DfhPWeIFiVMch7zBvgq6tWA2mb8TG13j
"""

import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Definir o cabeçalho para a requisição HTTP, simulando um navegador real
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36'
}

# Definir URL da API SIDRA do IBGE contendo os dados sobre empresas de construção
url_sidra = 'https://apisidra.ibge.gov.br/values/t/1757/n1/all/n2/all/v/631/p/first%2014/c319/104029'

# Fazer a requisição HTTP para obter os dados da API
response_sidra = requests.get(url_sidra, headers=header)

# Converter a resposta JSON para um dicionário Python
data_construcao = response_sidra.json()

# Carregar o arquivo do IBGE contendo dados de população por idade
populacao_df = pd.read_excel('Analise_de_Mercado\data\projecoes_2024_tab1_idade_simples (1).xlsx')

# Converter os dados da API SIDRA em um DataFrame do Pandas
empresas_df = pd.json_normalize(data_construcao)

# Preparar os DataFrames
empresas_df = empresas_df.drop(columns=['NC', 'MC', 'D1C', 'NN', 'D2C', 'D2N', 'D3C', 'D4C', 'D4N', 'MN'])
empresas_df = empresas_df.drop([0])
empresas_df = empresas_df.rename(columns={"V": "Trabalhadores", "D1N": "Estado", "D3N": "Ano"})
empresas_df = empresas_df[['Ano', 'Estado', 'Trabalhadores']]
populacao_df = populacao_df.drop([0, 1, 2, 3])
populacao_df = populacao_df.drop(columns={'Unnamed: 1'})
populacao_df = populacao_df.applymap(lambda x: int(x) if isinstance(x, (int, float)) else x)
populacao_df.columns = populacao_df.iloc[0]
populacao_df = populacao_df[1:].reset_index(drop=True)
populacao_df = populacao_df.rename(columns={'IDADE': 'Faixa Etaria', 'LOCAL': 'Estado'})

# Verificar DataFrame da população
populacao_df.head()

# Verificar DataFrame dos trabalhadores das empresas de contrução
empresas_df.head()

# Selecionar apenas as faixas etárias entre 38 e 58 anos
faixa_etaria = list(range(38, 59))  # 38 a 58 anos
populacao_filtrada = populacao_df[populacao_df['Faixa Etaria'].isin(faixa_etaria)]

# Agrupar por Estado e somar a população dessa faixa etária para cada ano
populacao_agrupada = populacao_filtrada.groupby('Estado').sum(numeric_only=True).reset_index()

estados = ['Acre', 'Alagoas', 'Amazonas', 'Amapá', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo', 'Goiás',
           'Maranhão', 'Minas Gerais', 'Mato Grosso do Sul', 'Mato Grosso', 'Pará', 'Paraíba', 'Pernambuco',
           'Piauí', 'Paraná', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rondônia', 'Roraima', 'Rio Grande do Sul',
           'Santa Catarina', 'Sergipe', 'São Paulo', 'Tocantins']

# Criar um padrão regex com as palavras da lista de estados
pattern = '|'.join(estados)

# Filtrar o DataFrame para remover linhas com estados
populacao_agrupada = populacao_agrupada[~populacao_agrupada['Estado'].str.contains(pattern, regex=True)]

# Preparar o DataFrame
populacao_agrupada = populacao_agrupada.set_index('Estado').T
populacao_agrupada.index.name = 'Ano'
populacao_agrupada = populacao_agrupada.transpose()
populacao_agrupada = populacao_agrupada.drop(columns=[2000, 2001, 2002, 2003, 2004, 2005, 2006, 2021, 2022])

# Verificar o formato após a agregação
populacao_agrupada.head()

# Agrupar os dados por Estado e Ano, somando o número de empresas
empresas_agrupadas = empresas_df.groupby(['Estado', 'Ano'])['Trabalhadores'].sum().reset_index()

# Exibir o resultado após o agrupamento
empresas_agrupadas.head()

# Pivotar os dados para transformar os anos em colunas
empresas_agrupadas_pivot = empresas_agrupadas.pivot(index='Estado', columns='Ano', values='Trabalhadores')

# Exibir o novo formato
empresas_agrupadas_pivot.head()

# Renomear as colunas de 'populacao_agrupada' para adicionar '_pop'
populacao_agrupada = populacao_agrupada.rename(columns=lambda x: f"{x}_pop" if x != "Regiao" else x)

# Renomear as colunas de 'empresas_agrupadas_pivot' para adicionar '_emp'
empresas_agrupadas_pivot = empresas_agrupadas_pivot.rename(columns=lambda x: f"{x}_emp" if x != "Regiao" else x)

# Verificar os nomes das colunas para garantir que estão corretos
populacao_agrupada.columns, empresas_agrupadas_pivot.columns

# Realizar o merge entre os dois DataFrames
dados_combinados = pd.merge(populacao_agrupada, empresas_agrupadas_pivot, left_index=True, right_index=True)

# Visualizar as colunas após o merge
dados_combinados.columns

# Garantir que as colunas de população e empresas sejam numéricas
for ano in range(2007, 2021):
    coluna_pop = f'{ano}_pop'
    coluna_emp = f'{ano}_emp'

    # Converter as colunas para numérico, caso ainda não estejam
    dados_combinados[coluna_pop] = pd.to_numeric(dados_combinados[coluna_pop], errors='coerce')
    dados_combinados[coluna_emp] = pd.to_numeric(dados_combinados[coluna_emp], errors='coerce')

    # Calcular a razão
    dados_combinados[f'Razao_{ano}'] = dados_combinados[coluna_pop] / dados_combinados[coluna_emp]

# Visualizar o DataFrame com as razões
dados_combinados.head()

# Visualizar as colunas após adição da razão
dados_combinados.columns

# Criar um array de anos (como números inteiros)
anos_disponiveis = np.array(range(2007, 2021)).reshape(-1, 1)  # 2007 a 2020
anos_futuros = np.array([2021, 2022]).reshape(-1, 1)  # Anos a prever

# Criar um loop para cada região e ajustar um modelo de regressão
for index, row in dados_combinados.iterrows():
    # Selecionar os valores conhecidos da razão
    valores_conhecidos = row[[f'Razao_{ano}' for ano in range(2007, 2021)]].values.reshape(-1, 1)

    # Criar e treinar o modelo
    modelo = LinearRegression()
    modelo.fit(anos_disponiveis, valores_conhecidos)

    # Prever 2021 e 2022
    previsoes = modelo.predict(anos_futuros).flatten()

    # Atribuir as previsões ao dataframe
    dados_combinados.loc[index, 'Razao_2021'] = previsoes[0]
    dados_combinados.loc[index, 'Razao_2022'] = previsoes[1]

# Exibir os últimos anos para conferência
dados_combinados[[f'Razao_{ano}' for ano in range(2018, 2023)]].head()

# Selecionar apenas os dados de razão (de 2007 a 2022)
colunas_razao = [f'Razao_{ano}' for ano in range(2007, 2023)]
dados_cluster = dados_combinados[colunas_razao]

# Normalizar os dados (para evitar viés por escalas diferentes)
scaler = StandardScaler()
dados_cluster_normalizado = scaler.fit_transform(dados_cluster)

# Definir intervalo válido para o número de clusters
num_samples = dados_cluster.shape[0]  # Número de regiões disponíveis
max_clusters = min(10, num_samples)  # Garantir que não exceda n_samples

# Determinar o número ideal de clusters pelo método do cotovelo
inercia = []
for k in range(2, max_clusters):  # Corrigindo para um intervalo válido
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(dados_cluster_normalizado)
    inercia.append(kmeans.inertia_)

# Plotar gráfico do método do cotovelo
plt.figure(figsize=(8, 5))
plt.plot(range(2, max_clusters), inercia, marker='o', linestyle='--')
plt.xlabel("Número de Clusters")
plt.ylabel("Inércia")
plt.title("Método do Cotovelo para Seleção do Número de Clusters")
plt.show()

# Definir número ideal de clusters
num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
dados_combinados['Cluster'] = kmeans.fit_predict(dados_cluster_normalizado)

# Visualizar os grupos
dados_combinados[['Cluster'] + colunas_razao].head()

# Ordenar os estados/regiões pelo valor da razão em 2021
dados_saturacao_2021 = dados_combinados[['Cluster', 'Razao_2021']].sort_values(by='Razao_2021')

# Definir limites para identificar saturação e oportunidades
percentil_baixo_2021 = dados_saturacao_2021['Razao_2021'].quantile(0.25)  # 25% menores valores
percentil_alto_2021 = dados_saturacao_2021['Razao_2021'].quantile(0.75)   # 25% maiores valores

# Criar uma nova coluna categorizando os mercados
def classificar_mercado_2021(valor):
    if valor <= percentil_baixo_2021:
        return "Saturado"
    elif valor >= percentil_alto_2021:
        return "Alta Oportunidade"
    else:
        return "Neutro"

dados_combinados['Classificacao_Mercado'] = dados_combinados['Razao_2021'].apply(classificar_mercado_2021)

# Exibir os estados/regiões mais saturadas e com mais oportunidades
print("Mercados Saturados em 2021:")
print(dados_combinados[dados_combinados['Classificacao_Mercado'] == "Saturado"][['Razao_2021']])

print("\nMaiores Oportunidades em 2021:")
print(dados_combinados[dados_combinados['Classificacao_Mercado'] == "Alta Oportunidade"][['Razao_2021']])

# Ordenar os estados/regiões pelo valor da razão em 2022
dados_saturacao_2022 = dados_combinados[['Cluster', 'Razao_2022']].sort_values(by='Razao_2022')

# Definir limites para identificar saturação e oportunidades
percentil_baixo_2022 = dados_saturacao_2022['Razao_2022'].quantile(0.25)  # 25% menores valores
percentil_alto_2022 = dados_saturacao_2022['Razao_2022'].quantile(0.75)   # 25% maiores valores

# Criar uma nova coluna categorizando os mercados
def classificar_mercado_2022(valor):
    if valor <= percentil_baixo_2022:
        return "Saturado"
    elif valor >= percentil_alto_2022:
        return "Alta Oportunidade"
    else:
        return "Neutro"

dados_combinados['Classificacao_Mercado'] = dados_combinados['Razao_2022'].apply(classificar_mercado_2022)

# Exibir os estados/regiões mais saturadas e com mais oportunidades
print("Mercados Saturados em 2022:")
print(dados_combinados[dados_combinados['Classificacao_Mercado'] == "Saturado"][['Razao_2022']])

print("\nMaiores Oportunidades em 2022:")
print(dados_combinados[dados_combinados['Classificacao_Mercado'] == "Alta Oportunidade"][['Razao_2022']])

# Selecionar os dados mais recentes (2022)
df_classificacao = dados_combinados[['Razao_2022']].reset_index()

# Definir a média da razão como referência
media_razao = df_classificacao['Razao_2022'].mean()

# Criar uma nova coluna 'Status' para classificar os mercados
df_classificacao['Status'] = df_classificacao['Razao_2022'].apply(lambda x: 'Oportunidade' if x > media_razao else 'Saturado')

# Remover a linha onde 'Estado' é 'Brasil'
df_classificacao = df_classificacao[df_classificacao['Estado'] != 'Brasil']

# Visualizar os dados
print(df_classificacao)

# Definir cores personalizadas para os status
cores = {'Oportunidade': 'blue', 'Saturado': 'red'}

# Criar o gráfico de barras
plt.figure(figsize=(12, 7))
sns.barplot(data=df_classificacao, x='Estado', y='Razao_2022', hue='Status', palette=cores)

# Adicionar rótulos e título
plt.xlabel('Região', fontsize=14)
plt.ylabel('Razão População/Empresas (2022)', fontsize=14)
plt.title('Mercados Saturados e com Oportunidade - Construção Civil', fontsize=16)

# Rotacionar os nomes das regiões para melhor visualização
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)

# Adicionar uma grade para melhor visualização
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Adicionar anotações nas barras
for p in plt.gca().patches:
    plt.gca().annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='center', fontsize=12, color='black',
                       xytext=(0, 5), textcoords='offset points')

# Personalizar a legenda
plt.legend(title='Classificação', title_fontsize=12, fontsize=12, loc='upper left')

# Exibir o gráfico
plt.show()

