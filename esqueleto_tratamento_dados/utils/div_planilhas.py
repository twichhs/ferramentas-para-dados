import pandas as pd
import os

# Caminho do arquivo de entrada
arquivo_entrada = ""

# Pasta de saída
pasta_saida = "/data/merge/break"


def dividir_csv_pandas(caminho_arquivo, linhas_por_arquivo=5000):
    """
    Divide um CSV em arquivos menores usando Pandas.
    """
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        print("Arquivo não encontrado!")
        return

    # Nome base para os arquivos de saída
    nome_base = "base"

    # O chunksize lê o arquivo em pedaços para não sobrecarregar a memória
    for i, chunk in enumerate(pd.read_csv(caminho_arquivo, chunksize=linhas_por_arquivo, sep=";")):
        # Cria o nome do novo arquivo (ex: dados_parte_0.csv, dados_parte_1.csv)
        nome_saida = f"/data/merge/break/{nome_base}_{i + 1}.csv"

        # Salva o pedaço, removendo o índice numérico do pandas
        chunk.to_csv(nome_saida, index=False, sep=";")

        print(f"Arquivo criado: {nome_saida} com {len(chunk)} linhas.")

# --- Como usar ---
# Substitua 'seu_arquivo.csv' pelo nome do seu arquivo real
# dividir_csv_pandas('seu_arquivo.csv', linhas_por_arquivo=1000)

dividir_csv_pandas(arquivo_entrada)