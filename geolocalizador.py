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
