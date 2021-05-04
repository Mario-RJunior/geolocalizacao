import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance
from banco_dados import listar
from sklearn.cluster import SpectralClustering
import folium
import numpy as np


# TODO: Implementar uma função para calcular distância para maior e menor rota.


def acessa_bd(data):
    """
    Função que chama a função listar e filtra as informações do banco de dados pela data recebida.
    :param data: Data para fazer o filtro no banco de dados.
    :return: Retorna um dicionário com os dados do banco de dados.
    """
    colunas = ['id', 'Nome', 'Rua', 'Numero_rua', 'Bairro', 'Cidade', 'Estado', 'Data']
    lista_dados = list(zip(colunas, listar(data)))
    dados = {}

    for c in lista_dados:
        dados[c[0]] = c[1]

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


def agrupa_visitas(dataframe, num_equipes):
    try:

        serie = dataframe['endereco_completo'].apply(converte_endereco)

        dataframe['latitude'] = serie.apply(lambda lat: lat[0])
        dataframe['longitude'] = serie.apply(lambda lon: lon[1])

        if len(dataframe) == 0:

            pass

        elif len(dataframe) == 1:

            dataframe['equipes'] = 0

        else:

            x = dataframe.loc[:, ['latitude', 'longitude']].values

            clustering = SpectralClustering(n_clusters=num_equipes,
                                            assign_labels="discretize",
                                            random_state=0,
                                            affinity='nearest_neighbors',
                                            n_neighbors=3).fit(x)

            previsoes = clustering.fit_predict(x)
            dataframe['equipes'] = previsoes

    except TypeError:

        print('Número de grupos maior do que o número de visitas. Tente novamente.')

    else:

        return dataframe


def map_plot(dataframe, origem):
    try:

        paleta_cores = ('blue', 'orange', 'darkred', 'pink', 'darkpurple', 'cadetblue',
                        'lightred', 'darkgreen', 'purple', 'darkblue', 'black', 'red',
                        'lightblue', 'beige', 'green', 'lightgray', 'lightgreen', 'gray',
                        'white')

        lat = dataframe['latitude'].to_list()
        lon = dataframe['longitude'].to_list()
        equipes = dataframe['equipes'].to_list()
        coord_origem = converte_endereco(origem)

        coordenadas = list(zip(lat, lon, equipes))

        m = folium.Map(location=[-20.2999473, -40.3221028], zoom_start=12)

        for loc in coordenadas:
            folium.Marker(location=(loc[0], loc[1]),
                          icon=folium.Icon(color=paleta_cores[loc[2]], icon='user', prefix="fa"),
                          popup=f'Equipe {loc[2] + 1}'
                          ).add_to(m)

        folium.Marker(location=(coord_origem[0], coord_origem[1]),
                      icon=folium.Icon(color='darkgreen', icon='medkit', prefix="fa"),
                      popup='Origem'
                      ).add_to(m)

    except TypeError:

        print('Erro ao gerar o mapa. Tente novamente.')

    else:

        return m


def calcula_distancias(dataframe, origem):
    grupos = np.sort(dataframe['equipes'].unique())
    lista_grupos = []

    for g in grupos:

        inicio = origem
        df = dataframe.query(f'equipes == {g}')
        enderecos = df['endereco_completo'].to_list()
        dic = {}

        for end in enderecos:
            coord_inicio = converte_endereco(inicio)
            coord = converte_endereco(end)
            distancia = geopy.distance.distance(coord_inicio, coord).km

            dic[end] = distancia
        lista_grupos.append(dic)

    return lista_grupos


def retorna_rotas(rotas):
    dic_rotas_ordenadas = {}
    rotas_temp = []
    cont = 0

    for r in rotas:
        cont += 1
        rota_ordenada = sorted(r.items(), key=lambda x: x[1])

        for ro in rota_ordenada:
            rotas_temp.append(ro[0])

        dic_rotas_ordenadas[f'Equipe {cont}'] = rotas_temp.copy()
        rotas_temp.clear()

    return dic_rotas_ordenadas


def distancias_max_min(dataframe, origem):
    grupos = np.sort(dataframe['equipes'].unique())
    lista_distancias = []

    for g in grupos:

        inicio = origem
        df = dataframe.query(f'equipes == {g}')
        enderecos = df['endereco_completo'].to_list()
        dic = {}
        dic2 = {}
        min_dist = 0

        while len(enderecos) > 0:

            for end in enderecos:
                coord_inicio = converte_endereco(inicio)
                coord = converte_endereco(end)
                distancia = geopy.distance.distance(coord_inicio, coord).km

                dic[end] = distancia

            mais_perto = min(dic, key=dic.get)
            dic2[mais_perto] = dic[mais_perto]
            inicio = mais_perto

            min_dist += dic[mais_perto]
            dic.clear()
            enderecos.remove(mais_perto)

        lista_distancias.append(dic2)

    return lista_distancias
