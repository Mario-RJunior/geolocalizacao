from geolocalizador import *
from pprint import pprint

if __name__ == '__main__':
    bd = acessa_bd()
    df = gera_dataframe(bd)
    perg = str(input('Digite a localização (Bairro, Cidade - UF): '))
    serie = df['endereco_completo'].apply(converte_endereco)
    df['lat-long'] = serie
    dist = calcula_distancia_ordenada(perg, df)
    dist_rel = distancias_relativas(dist)
    pprint(dist_rel)
    # km_percorridos = calculo_distancia(dist_rel)
    # print(km_percorridos)
