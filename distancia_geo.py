import pandas as pd
import numpy as np

def haversine_km(df, lat1, lon1, lat2, lon2):
    """
    Calcula distância em KM entre dois pontos (lat/lon)
    usando Haversine (vetorizado)
    """

    # Converter para radianos
    lat1_rad = np.radians(df[lat1])
    lon1_rad = np.radians(df[lon1])
    lat2_rad = np.radians(df[lat2])
    lon2_rad = np.radians(df[lon2])

    # Diferenças
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    # Raio da Terra (km)
    R = 6371

    return R * c



df = pd.DataFrame({ # preencha o dataframe com as cordenadas que deseja calcular
    'lat_origem': [-23.515538871507328], 
    'lon_origem': [-46.687931571678064],
    'lat_destino': [-23.665422576676516], 
    'lon_destino': [-46.65907023761084]
})

df['dist_km'] = haversine_km(
    df,
    'lat_origem', 'lon_origem',
    'lat_destino', 'lon_destino'
)
# Resultado comparada entre os pontos em linha reta com 98% de precisão
# Para validar, use o "Medir Até Aqui" do google maps
print(df)
