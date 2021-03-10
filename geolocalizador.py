import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance
from banco_dados import listar


def acessa_bd():
    dados = {'id': listar()[0],
             'Nome': listar()[1],
             'Rua': listar()[2],
             'Numero_rua': listar()[3],
             'Bairro': listar()[4],
             'Cidade': listar()[5],
             'Estado': listar()[6]
             }
    return dados


def gera_dataframe(dado):
    dataframe = pd.DataFrame(dado)
    dataframe['endereco_completo'] = \
        dataframe['Rua'].astype(str) + ', ' + dataframe['Numero_rua'].astype(str) + ', ' + \
        dataframe['Cidade'].astype(str) + ' - ' + dataframe['Estado'].astype(str)

    return dataframe


def converte_endereco(endereco):
    geolocator = Nominatim(user_agent="my_user_agent")
    pais = "BR"
    loc = geolocator.geocode(endereco + ',' + pais)

    return loc.latitude, loc.longitude


def ordena_distancia(e):
    return e['distancia']


def calcula_distancia_ordenada(endereco, dataframe):
    dic_distancias = {}
    lista_distancias = []

    coordenadas = converte_endereco(endereco)
    distancias = dataframe['lat-long'].map(lambda x: geopy.distance.distance(x, coordenadas).km)
    lista_zip = list(zip(dataframe['endereco_completo'].to_list(), distancias))

    for e in lista_zip:
        dic_distancias['endereço'] = e[0]
        dic_distancias['distancia'] = e[1]
        lista_distancias.append(dic_distancias.copy())

    lista_distancias.sort(key=ordena_distancia)

    return lista_distancias


def distancias_relativas(lista_dist):
    d = lista_dist[0]['distancia']

    for reg in lista_dist:
        km = reg['distancia'] - d
        reg['distancia relativa'] = abs(km)
        d = reg['distancia']

    return lista_dist


def calculo_distancia(lista_dist):
    km = 0

    for c in range(len(lista_dist)):
        if c == 0:
            km += lista_dist[c]['distancia']
        else:
            km += lista_dist[c]['distancia relativa']
    return km
