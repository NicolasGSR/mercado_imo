# mercado_imo

## Índice

1. [Visão Geral](#visão-geral)
2. [Objetivo](#objetivo)
3. [Tecnologias Utilizadas](#tecnologias-utilizadas)
4. [Instalação](#instalação)
5. [Estrutura do Projeto](#estrutura-do-projeto)
6. [Como Usar](#como-usar)

---

## Visão Geral

Este projeto visa analisar o mercado da construção civil, identificando os estados/regiões mais saturados e aqueles com mais oportunidades para o setor. A análise é realizada com base na razão entre a população de 38 a 58 anos (um grupo etário relevante para o mercado de trabalho) e o número de trabalhadores no setor. A partir dessa análise, geramos uma classificação de "Saturado" ou "Oportunidade" para cada região do Brasil.

## Objetivo

O objetivo deste projeto é fornecer uma análise do mercado da construção civil com base em dados estatísticos, ajudando a identificar as áreas mais saturadas e as que oferecem maiores oportunidades para expansão do setor. Utilizamos dados históricos e estimativas para os anos de 2021 e 2022, gerando previsões sobre a dinâmica do mercado.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal para o desenvolvimento da análise e criação dos gráficos.
- **Pandas**: Manipulação e análise de dados.
- **Matplotlib** e **Seaborn**: Criação de visualizações gráficas.
- **Scikit-learn**: Algoritmos de aprendizado de máquina, utilizados para a análise de agrupamento (K-Means).
- **Requests**: Realização de requisições HTTP para obter dados do IBGE (API SIDRA).
- **Jupyter Notebook**: Ambiente utilizado para desenvolver o código inicialmente (Google Colab).

## Instalação

Para rodar este projeto, siga as instruções abaixo:

### Pré-requisitos

Antes de instalar, certifique-se de que você possui o Python 3.x instalado em seu sistema. Você também pode precisar instalar algumas dependências.

### Passo 1: Clonar o Repositório

Primeiro, clone o repositório para o seu computador:

```bash
git clone https://github.com/usuario/nome-do-repositorio.git
```

### Passo 2: Criar um Ambiente Virtual (opcional, mas recomendado)

```python
python -m venv venv
source venv/bin/activate  # Para sistemas Linux/macOS
venv\Scripts\activate  # Para sistemas Windows
```

### Passo 3: Instalar Dependências

```python
pip install -r requirements.txt
```

## Estrutura do Projeto
O projeto está organizado da seguinte forma:

```
seu-projeto/
│
├── data/                        # Pasta para armazenar os arquivos de dados (ex. arquivos Excel ou CSV)
│   ├── projecoes_2024_tab1_idade_simples (1).xlsx   # Exemplo de arquivo Excel
│
├── src/                         # Código fonte do projeto
│   ├── main.py                  # Arquivo principal com o código do projeto
│
├── requirements.txt             # Arquivo de dependências
├── .gitignore                   # Arquivo para ignorar arquivos não desejados no Git
└── README.md                    # Documentação do projeto
```

## Como Usar
Após a instalação das dependências, siga as etapas abaixo para executar a análise:

Certifique-se de que os arquivos de dados estão na pasta data/.

Execute o arquivo principal:
```
python src/main.py
```

O código irá carregar os dados de população e de trabalhadores, realizar a análise de saturação e gerar gráficos com os resultados.