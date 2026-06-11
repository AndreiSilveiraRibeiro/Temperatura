import pandas as pd
import numpy as np

tabela = pd.read_csv("projeto2_limpeza_pesada.csv")

print(tabela.head())
print(tabela.shape)

print(tabela['nome'])

tabela['nome'] = tabela['nome'].str.title().str.strip()

print(tabela['nome'].unique())
print(tabela['nome'])

print(tabela['cpf'])

tabela['cpf_camuflado'] = 'xxx.xxx.xxx' + tabela['cpf'].str[-3:]

print(tabela)
print(tabela['cpf'])

ddd = {

    "ES": "(27)",
    "MG": "(31)",
    "SP": "(11)",
    "RJ": "(21)",

}

estados = {
 
    'S.Paulo': 'SP',
    'sp': 'SP',
    'Espírito Santo': 'ES',
    'Minas Gerais': 'MG',
    'São Paulo': 'SP',
    'Rio de Janeiro': 'RJ'

}

tabela['estado'] = tabela['estado'].str.strip()

print(tabela['estado'].unique())

estado_errado = ~tabela['estado'].str.contains(r'^[A-Z]{2}$', regex=True, na=False)

tabela.loc[estado_errado, 'estado'] = tabela.loc[estado_errado, 'estado'].map(estados)

print(tabela['estado'])

print(tabela['telefone'])

tabela['telefone'] = tabela['telefone'].str.replace(r'^(\d{2})\s(.*)$', r'(\1) \2', regex=True)

sem_ddd = ~tabela['telefone'].str.startswith("(", na=False)

tabela.loc[sem_ddd, 'telefone'] = tabela.loc[sem_ddd, 'estado'].map(ddd) + tabela.loc[sem_ddd, 'telefone']
print(tabela['telefone'])

tabela['telefone'] = tabela['telefone'].str.replace(r'\)(\d)', r') \1', regex=True)

print(tabela['telefone'])

print(tabela['data_nascimento'])

tabela['data_nascimento'] = tabela['data_nascimento'].str.replace('-', '/')

tabela['data_nascimento'] = tabela['data_nascimento'].str.replace(r'^(\d{4})\/(\d{2})\/(\d{2})', r'\3/\2/\1', regex=True)

tabela['data_nascimento'] = pd.to_datetime(tabela['data_nascimento'], dayfirst=True, errors='coerce')

tabela['data_nascimento'] = tabela['data_nascimento'].dt.strftime('%d/%m/%Y')

tabela['data_nascimento'] = tabela['data_nascimento'].fillna("Data Errada")

print(tabela['data_nascimento'])

print(tabela['salario'])

tabela['salario'] = tabela['salario'].str.replace(r'^.{2}\s(.*)', r'\1', regex=True)

tabela['salario'] = tabela['salario'].str.replace('.', '', regex=False)

tabela['salario'] = tabela['salario'].str.replace(',', '.', regex=False)

tabela['salario'] = tabela['salario'].astype(float)

print(tabela['salario'])

print(tabela[tabela['quantidade_vendida'] < 0 ])
print(tabela[tabela['quantidade_vendida'].isna()])

tabela['quantidade_vendida'] = tabela['quantidade_vendida'].apply(lambda x: pd.NA if x < 0 else x)

print(tabela[tabela['quantidade_vendida'].isna()])

tabela['quantidade_vendida'] = tabela['quantidade_vendida'].fillna(0)

print(tabela[tabela['quantidade_vendida'] == 0])

print(tabela['data_venda'])

tabela['data_venda'] = tabela['data_venda'].str.replace('-', '/')

tabela['data_venda'] = tabela['data_venda'].str.replace(r'^(\d{4})\/(\d{2})\/(\d{2})', r'\3/\2/\1', regex=True)

tabela['data_venda'] = pd.to_datetime(tabela['data_venda'], dayfirst=True, errors='coerce')

tabela['data_venda'] = tabela['data_venda'].dt.strftime('%d/%m/%Y')

tabela['data_venda'] = tabela['data_venda'].fillna("Data Errada")

print(tabela['data_venda'])

print(tabela['email'])

tabela = tabela.drop('cpf', axis=1)

tabela.to_csv('projeto2_limpo', index=False)