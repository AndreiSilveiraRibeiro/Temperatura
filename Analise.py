import pandas as pd
import numpy as np

#Lendo o .csv e transformando em DataFrame
tabela = pd.read_csv("projeto2_limpeza_pesada.csv")

#Lendo o Dataframe inteiro para analisar oque tenho que fazer
print(tabela.head())
print(tabela.shape)


# --- TRATAMENTO DA COLUNA NOME ---

# Exibe os nomes originais e bagunçados no terminal
print(tabela['nome'])

# Padroniza: Primeira Letra Maiúscula (.title) e remove espaços inúteis (.strip)
tabela['nome'] = tabela['nome'].str.title().str.strip()

# Exibe os nomes únicos e a coluna tratada para conferência
print(tabela['nome'].unique())
print(tabela['nome'])


# --- TRATAMENTO E SEGURANÇA DO CPF ---

# Exibe os CPFs originais na tela
print(tabela['cpf'])

# Cria uma nova coluna camuflando o CPF por LGPD, mantendo só os 3 últimos dígitos
tabela['cpf_camuflado'] = 'xxx.xxx.xxx' + tabela['cpf'].str[-3:]

# Exibe a tabela e os CPFs para validar o mascaramento
print(tabela)
print(tabela['cpf'])


# --- DICIONÁRIOS DE SUPORTE PARA ESTADO E TELEFONE ---

# Dicionário mapeando a sigla do estado para o seu respectivo DDD
ddd = {
    "ES": "(27)",
    "MG": "(31)",
    "SP": "(11)",
    "RJ": "(21)",
}

# Dicionário de tradução para corrigir os estados escritos errados ou por extenso
estados = {
    'S.Paulo': 'SP',
    'sp': 'SP',
    'Espírito Santo': 'ES',
    'Minas Gerais': 'MG',
    'São Paulo': 'SP',
    'Rio de Janeiro': 'RJ'
}


# --- TRATAMENTO DA COLUNA ESTADO ---

# Remove espaços invisíveis no início ou fim dos estados
tabela['estado'] = tabela['estado'].str.strip()

# Mostra no terminal quais estados únicos existem na base antes da correção
print(tabela['estado'].unique())

# Cria uma máscara identificando quem NÃO está no padrão de 2 letras maiúsculas (ex: SP)
estado_errado = ~tabela['estado'].str.contains(r'^[A-Z]{2}$', regex=True, na=False)

# Aplica o dicionário 'estados' usando .map() apenas nas linhas que estavam incorretas
tabela.loc[estado_errado, 'estado'] = tabela.loc[estado_errado, 'estado'].map(estados)

# Exibe os estados corrigidos e padronizados
print(tabela['estado'])


# --- TRATAMENTO DA COLUNA TELEFONE ---

# Mostra os telefones originais da tabela
print(tabela['telefone'])

# Se o telefone começar com DDD solto (ex: 11 91234...), coloca parênteses no DDD: (11) 91234...
tabela['telefone'] = tabela['telefone'].str.replace(r'^(\d{2})\s(.*)$', r'(\1) \2', regex=True)

# Cria uma máscara para encontrar os telefones que NÃO começam com parênteses (sem DDD)
sem_ddd = ~tabela['telefone'].str.startswith("(", na=False)

# Mapeia o estado daquela linha para o DDD correto e cola antes do telefone sem DDD
tabela.loc[sem_ddd, 'telefone'] = tabela.loc[sem_ddd, 'estado'].map(ddd) + tabela.loc[sem_ddd, 'telefone']
print(tabela['telefone'])

# Ajusta números que ficaram colados após a junção (ex: )9 vira ) 9)
tabela['telefone'] = tabela['telefone'].str.replace(r'\)(\d)', r') \1', regex=True)

# Exibe o resultado final dos telefones totalmente padronizados
print(tabela['telefone'])


# --- TRATAMENTO DA COLUNA DATA DE NASCIMENTO ---

# Mostra as datas de nascimento brutas
print(tabela['data_nascimento'])

# Substitui traços por barras para unificar os separadores de data
tabela['data_nascimento'] = tabela['data_nascimento'].str.replace('-', '/')

# Se a data estiver no formato americano (AAAA/MM/DD), inverte usando Regex para (DD/MM/AAAA)
tabela['data_nascimento'] = tabela['data_nascimento'].str.replace(r'^(\d{4})\/(\d{2})\/(\d{2})', r'\3/\2/\1', regex=True)

# Converte a coluna para data oficial do Pandas, transformando datas impossíveis em NaT (vazio)
tabela['data_nascimento'] = pd.to_datetime(tabela['data_nascimento'], dayfirst=True, errors='coerce')


# --- TRATAMENTO DA COLUNA DATA DE VENDA ---

# Mostra as datas de venda originais
print(tabela['data_venda'])

# Substitui traços por barras para unificar os separadores da data de venda
tabela['data_venda'] = tabela['data_venda'].str.replace('-', '/')

# Se a data de venda estiver em formato americano (AAAA/MM/DD), inverte para (DD/MM/AAAA)
tabela['data_venda'] = tabela['data_venda'].str.replace(r'^(\d{4})\/(\d{2})\/(\d{2})', r'\3/\2/\1', regex=True)

# Converte para data oficial do Pandas, isolando erros bizarros como nulos (NaT)
tabela['data_venda'] = pd.to_datetime(tabela['data_venda'], dayfirst=True, errors='coerce')


# --- VALIDAÇÃO CRITICA: CRUZAMENTO DE DATAS ---

# Exibe se há alguma linha onde a venda aconteceu ANTES do cliente nascer (viagem no tempo)
print(f"Teste de Consistência (Venda < Nascimento): \n{tabela[tabela['data_venda'] < tabela['data_nascimento']]}")


# --- FINALIZAÇÃO E FORMATAÇÃO DAS DATAS ---

# Agora que as validações foram feitas, transforma as datas em texto no formato brasileiro (DD/MM/AAAA)
tabela['data_nascimento'] = tabela['data_nascimento'].dt.strftime('%d/%m/%Y')
tabela['data_venda'] = tabela['data_venda'].dt.strftime('%d/%m/%Y')

# Substitui os erros ou vazios das duas colunas pelo texto "Data Errada"
tabela['data_nascimento'] = tabela['data_nascimento'].fillna("Data Errada")
tabela['data_venda'] = tabela['data_venda'].fillna("Data Errada")

# Exibe as colunas de datas totalmente higienizadas e prontas
print(tabela['data_nascimento'])
print(tabela['data_venda'])


# --- TRATAMENTO DA COLUNA SALÁRIO ---

# Mostra os salários brutos (ex: R$ 2.500,00)
print(tabela['salario'])

# Remove o prefixo "R$ " do início da string usando Regex e mantém só o número
tabela['salario'] = tabela['salario'].str.replace(r'^.{2}\s(.*)', r'\1', regex=True)

# Remove o ponto indicador de milhar (ex: 2.500 vira 2500) - regex=False garante busca literal
tabela['salario'] = tabela['salario'].str.replace('.', '', regex=False)

# Troca a vírgula decimal por ponto para o Python entender (ex: 2500,00 vira 2500.00)
tabela['salario'] = tabela['salario'].str.replace(',', '.', regex=False)

# Converte a coluna de texto para número decimal (float) para permitir cálculos matemáticos
tabela['salario'] = tabela['salario'].astype(float)

# Exibe os salários limpos e convertidos em números reais
print(tabela['salario'])


# --- TRATAMENTO DA COLUNA QUANTIDADE VENDIDA ---

# Filtra e exibe linhas com valores impossíveis (menores que zero) ou nulos originais
print(tabela[tabela['quantidade_vendida'] < 0 ])
print(tabela[tabela['quantidade_vendida'].isna()])

# Aplica uma função lambda: se a quantidade for negativa, vira nulo (pd.NA), se não, mantém
tabela['quantidade_vendida'] = tabela['quantidade_vendida'].apply(lambda x: pd.NA if x < 0 else x)

# Exibe a tabela filtrando apenas pelos nulos atuais para conferência
print(tabela[tabela['quantidade_vendida'].isna()])

# Preenche todos os valores nulos com zero e força a coluna a ser número inteiro (int)
tabela['quantidade_vendida'] = tabela['quantidade_vendida'].fillna(0).astype(int)

# Exibe as linhas que agora possuem quantidade igual a zero para conferir o preenchimento
print(tabela[tabela['quantidade_vendida'] == 0])


# --- TRATAMENTO DA COLUNA EMAIL ---

# Exibe os e-mails originais para checagem visual final
print(tabela['email'])

# Padroniza os e-mails: tudo em letras minúsculas (.lower) e sem espaços extras (.strip)
tabela['email'] = tabela['email'].str.lower().str.strip()


# --- AUDITORIA FINAL DA BASE (PENTE FINO) ---

# Exibe a quantidade total de linhas completamente duplicadas na base
print("Quantidade de linhas duplicadas encontradas:", tabela.duplicated().sum())

# Remove as linhas duplicadas da tabela, mantendo apenas a primeira ocorrência
tabela = tabela.drop_duplicates()

# Exibe o resumo final para validação e auditoria dos dados limpos
print(tabela.head())
print(tabela.describe()) # Traz o resumo estatístico (médias, mínimos e máximos) dos números
print(tabela.shape)      # Mostra o tamanho final da tabela após o drop de colunas e duplicadas

# Remove a coluna de CPF original (sujo/exposto) por segurança de dados e conformidade com LGPD
tabela = tabela.drop('cpf', axis=1)

tabela.to_csv("projeto2_limpeza_concluida.csv", index=False)