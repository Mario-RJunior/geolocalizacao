import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance
from banco_dados import listar
from pprint import pprint
from sklearn.cluster import KMeans
import folium
import webbrowser


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
    geolocator = Nominatim(user_agent="my_user_agent", timeout=20)
    pais = "BR"
    loc = geolocator.geocode(endereco + ',' + pais)

    return loc.latitude, loc.longitude


def agrupa_visitas(num_equipes, dataframe):
    serie = dataframe['endereco_completo'].apply(converte_endereco)
    dataframe['latitude'] = serie.apply(lambda lat: lat[0])
    dataframe['longitude'] = serie.apply(lambda lon: lon[1])

    x = dataframe.loc[:, ['latitude', 'longitude']].values
    kmeans = KMeans(n_clusters=num_equipes, random_state=0)
    previsoes = kmeans.fit_predict(x)
    dataframe['equipes'] = previsoes

    return dataframe


def map_plot(dataframe):
    lat = dataframe['latitude'].to_list()
    lon = dataframe['longitude'].to_list()

    coordenadas = list(zip(lat, lon))

    m = folium.Map(location=[-20.2999473, -40.3221028], zoom_start=12)
    for loc in coordenadas:
        folium.Marker(location=loc,
                      icon=folium.Icon(color='red')
                      ).add_to(m)
    m.save('map.html')
    webbrowser.open('map.html', new=2)


def calcula_rota(dataframe, origem):
    enderecos = dataframe['endereco_completo'].to_list()
    inicio = origem
    dic = {}

    while len(enderecos) > 0:

        for end in enderecos:
            coord_inicio = converte_endereco(inicio)
            coord = converte_endereco(end)
            distancia = geopy.distance.distance(coord_inicio, coord).km

            dic[end] = distancia

        mais_perto = min(dic, key=dic.get)
        enderecos.remove(str(mais_perto))
        inicio = mais_perto
        pprint(dic)
        dic.clear()
        print(mais_perto)
        print('-=' * 50)
