from pathlib import Path
from zipfile import ZipFile, BadZipFile

# ============================================================
# CONFIGURAÇÕES
# ============================================================

DIRETORIO_ORIGEM = Path("/home/leo/CBD/tratamento_pandas/notebooks/CLOUD_WALK/descompactados")
DIRETORIO_DESTINO = Path("/home/leo/CBD/tratamento_pandas/notebooks/CLOUD_WALK/bases_full_service")


# ============================================================
# PREPARAÇÃO
# ============================================================

# Cria a pasta de destino, caso não exista
DIRETORIO_DESTINO.mkdir(parents=True, exist_ok=True)

# Busca arquivos ZIP no diretório e em todas as subpastas
arquivos_zip = list(DIRETORIO_ORIGEM.rglob("*.zip"))

# Contadores
sucessos = 0
falhas = 0

print(f"Arquivos ZIP encontrados: {len(arquivos_zip)}")


# ============================================================
# EXTRAÇÃO
# ============================================================

for arquivo in arquivos_zip:

    try:
        with ZipFile(arquivo, "r") as zip_ref:

            # Verifica a integridade do ZIP
            arquivo_corrompido = zip_ref.testzip()

            if arquivo_corrompido is not None:
                raise BadZipFile(
                    f"Arquivo corrompido: {arquivo_corrompido}"
                )

            # Preserva a estrutura das subpastas de origem
            caminho_relativo = arquivo.relative_to(DIRETORIO_ORIGEM)

            # Cria uma pasta de destino para cada ZIP
            pasta_destino = (
                DIRETORIO_DESTINO
                / caminho_relativo.parent
                / arquivo.stem
            )

            pasta_destino.mkdir(parents=True, exist_ok=True)

            # Extrai os arquivos
            zip_ref.extractall(pasta_destino)

        sucessos += 1
        print(f"[OK] {arquivo}")

    except (BadZipFile, OSError, RuntimeError) as erro:
        falhas += 1
        print(f"[ERRO] {arquivo}: {erro}")


# ============================================================
# RESUMO
# ============================================================

print("\n========== RESUMO ==========")
print(f"Encontrados: {len(arquivos_zip)}")
print(f"Extraídos:   {sucessos}")
print(f"Com falha:   {falhas}")