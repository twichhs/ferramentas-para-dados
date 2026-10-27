from pathlib import Path
from zipfile import ZipFile

# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Diretório onde estão os arquivos ZIP
DIRETORIO_ORIGEM = Path("/home/leo/CBD/tratamento_pandas/notebooks/CLOUD_WALK/zips")

# Diretório onde os arquivos serão extraídos
DIRETORIO_DESTINO = Path("/home/leo/CBD/tratamento_pandas/notebooks/CLOUD_WALK/descompactados")


# ============================================================
# PROCESSAMENTO
# ============================================================

# Cria a pasta de destino, caso ela não exista (exist_ok = True)
DIRETORIO_DESTINO.mkdir(parents=True, exist_ok=True)

# Busca todos os arquivos com extensão .zip no diretório de origem
arquivos_zip = list(DIRETORIO_ORIGEM.glob("*.zip"))

# Exibe a quantidade de arquivos encontrados
print(f"Arquivos ZIP encontrados: {len(arquivos_zip)}")

# Percorre cada arquivo ZIP encontrado
for arquivo in arquivos_zip:

    try:
        # Abre o arquivo ZIP no modo de leitura
        with ZipFile(arquivo, "r") as zip_ref:

            # Cria uma pasta específica para cada ZIP
            pasta_destino = DIRETORIO_DESTINO / arquivo.stem
            pasta_destino.mkdir(parents=True, exist_ok=True)

            # Extrai todos os arquivos para a pasta de destino
            zip_ref.extractall(pasta_destino)

            print(f"Extraído: {arquivo.name} -> {pasta_destino}")

    except Exception as erro:
        print(f"Erro ao extrair {arquivo.name}: {erro}")

print("Processamento concluído!")