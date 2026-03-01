import pandas as pd
import glob
import os
from pathlib import Path

# Caminho da pasta onde estão os CSVs
pasta = "/data/merge"


def contar_linhas_por_extensao(pasta, extensao=".csv"):
    total = 0

    for arquivo in Path(pasta).glob(f"*{extensao}"):
        with open(arquivo, "r", encoding="utf-8") as f:
            linhas = sum(1 for _ in f)

        print(f"{arquivo.name}: {linhas}")
        total += linhas

    print(f"\nTOTAL ({extensao}): {total}")


# Lista todos os arquivos CSV da pasta
arquivos_csv = glob.glob(os.path.join(pasta, "*.csv"))

# Verificação básica
if not arquivos_csv:
    raise ValueError("Nenhum arquivo CSV encontrado na pasta.")

# Lê e concatena todos os CSVs
df_unificado = pd.concat(
    (pd.read_csv(arquivo, sep=";") for arquivo in arquivos_csv),
    ignore_index=True
)

# Salva o arquivo final

arquivo_unificado = str(input("Nome do arquivo a ser salvo: "))
saida = os.path.join(pasta, f"{arquivo_unificado}.csv")
df_unificado.to_csv(saida, index=False, encoding="utf-8", sep=";")
print("Arquivo salvo com sucesso!")

print(f"Arquivo unificado salvo em: {saida}")
print(f"Total de linhas: {len(df_unificado)}")