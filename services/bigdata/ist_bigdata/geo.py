"""Visualização geográfica dos casos com Folium."""

import folium

from ist_bigdata import config
from ist_bigdata.graficos import caminho_saida


def mapa_casos_por_localidade(df, nome_arquivo="mapa_casos_localidade.html"):
    """Um marcador por cidade, com raio proporcional à raiz do número de casos."""
    casos = df.groupBy("localidade").count().toPandas()

    coordenadas = casos["localidade"].map(lambda x: config.COORDENADAS_CIDADES.get(x, [None, None]))
    casos["latitude"] = coordenadas.map(lambda c: c[0])
    casos["longitude"] = coordenadas.map(lambda c: c[1])
    casos = casos.dropna(subset=["latitude", "longitude"])

    mapa = folium.Map(location=config.CENTRO_MAPA, zoom_start=4)
    for _, row in casos.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=max(5, row["count"] ** 0.5),
            popup=f"{row['localidade']}: {row['count']} casos",
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.6,
        ).add_to(mapa)

    mapa.save(str(caminho_saida(nome_arquivo)))
    return mapa
