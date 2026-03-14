import pandas as pd
import requests
import time
from pathlib import Path

# =========================
# CONFIGURAÇÕES
# =========================

COLUNA_CEP = "CEP"
ARQUIVO_CACHE = "cache_ceps_enriquecidos.csv"

BATCH_SIZE = 20
SLEEP = 0.2
MAX_RETRY = 3


# =========================
# NORMALIZA CEP
# =========================

def normalizar_cep(cep):

    return (
        str(cep)
        .replace("-", "")
        .replace(".0", "")
        .strip()
        .zfill(8)
    )


# =========================
# CONSULTA API COM RETRY
# =========================

def consultar_cep(cep):

    url = f"https://cep.awesomeapi.com.br/json/{cep}"

    for tentativa in range(1, MAX_RETRY + 1):

        try:

            r = requests.get(url, timeout=5)

            if r.status_code == 200:

                data = r.json()

                resultado = {
                    "cep": data.get("cep"),
                    "cidade": data.get("city"),
                    "uf": data.get("state"),
                    "bairro": data.get("district"),
                    "lat": data.get("lat"),
                    "lng": data.get("lng"),
                    "ibge": data.get("city_ibge"),
                    "ddd": data.get("ddd")
                }

                print(f"""
CEP encontrado
CEP: {resultado['cep']}
Cidade: {resultado['cidade']}
UF: {resultado['uf']}
Bairro: {resultado['bairro']}
Lat/Lng: {resultado['lat']} , {resultado['lng']}
""")

                return resultado

        except Exception as e:

            print(f"Erro tentativa {tentativa} para CEP {cep}")

            time.sleep(1)

    print(f"CEP falhou após {MAX_RETRY} tentativas -> {cep}")

    return {"cep": cep}


# =========================
# CARREGAR BASE
# =========================

df_base = pd.read_csv("df_base.csv" , sep=",")

df_base[COLUNA_CEP] = df_base[COLUNA_CEP].apply(normalizar_cep)


# =========================
# OTIMIZAÇÃO - CEPs ÚNICOS
# =========================

ceps_unicos = df_base[COLUNA_CEP].dropna().unique()

print("Total linhas base:", len(df_base))
print("CEPs únicos:", len(ceps_unicos))


# =========================
# CARREGAR CACHE
# =========================

if Path(ARQUIVO_CACHE).exists():

    df_cache = pd.read_csv(ARQUIVO_CACHE)

    ceps_processados = set(df_cache["cep"].astype(str))

    print("Cache encontrado:", len(df_cache))

else:

    df_cache = pd.DataFrame()

    ceps_processados = set()


# =========================
# FILTRAR CEPs RESTANTES
# =========================

ceps_restantes = [c for c in ceps_unicos if c not in ceps_processados]

print("CEPs restantes:", len(ceps_restantes))


# =========================
# PROCESSAMENTO
# =========================

novos = []

for i, cep in enumerate(ceps_restantes, 1):

    print(f"\nConsultando CEP {cep} ({i}/{len(ceps_restantes)})")

    dados = consultar_cep(cep)

    novos.append(dados)

    if i % BATCH_SIZE == 0:

        df_lote = pd.DataFrame(novos)

        df_cache = pd.concat([df_cache, df_lote], ignore_index=True)

        df_cache.to_csv(ARQUIVO_CACHE, index=False)

        print(f"\nLote salvo - {i} CEPs")

        novos = []

    time.sleep(SLEEP)


# salvar resto

if novos:

    df_lote = pd.DataFrame(novos)

    df_cache = pd.concat([df_cache, df_lote], ignore_index=True)

    df_cache.to_csv(ARQUIVO_CACHE, index=False)


print("\nProcessamento finalizado")
