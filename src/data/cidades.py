from dataclasses import dataclass
from collections import defaultdict
import pandas as pd

@dataclass
class Cidade:
    nome: str
    estado: str
    latitude: float
    longitude: float

estado_dict: dict[str, list[Cidade]] = defaultdict(list)
nome_dict: dict[str, list[Cidade]] = defaultdict(list)

def load_cidades():
    if estado_dict and nome_dict:
        return nome_dict

    df = pd.read_csv("src/data/lat_long_cidades.csv", sep=';', encoding='utf-8')

    for _, row in df.iterrows():
        nome = row['municipio'].strip()
        estado = row['uf'].strip().upper()
        lat = float(row['latitude'])
        lon = float(row['longitude'])

        cidade = Cidade(nome, estado, lat, lon)
        estado_dict[estado].append(cidade)
        nome_dict[nome].append(cidade)

    return nome_dict

def get_lista_cidades_unicas():
    if not nome_dict:
        load_cidades()
    return list(nome_dict.keys())

def get_cidades_por_estado(uf: str) -> list[Cidade]:
    if not estado_dict:
        load_cidades()
    return estado_dict.get(uf.upper(), [])

def get_cidades_por_nome(nome: str) -> list[Cidade]:
    if not nome_dict:
        load_cidades()
    return nome_dict.get(nome.strip(), [])