import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance
from banco_dados import listar
from sklearn.cluster import SpectralClustering
import folium
import numpy as np
# import webbrowser
# from math import ceil


def acessa_bd(data):
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

            # qtd_visitas_cluster = ceil(dataframe.shape[0] / num_equipes)
            x = dataframe.loc[:, ['latitude', 'longitude']].values

            clustering = SpectralClustering(n_clusters=num_equipes,
                                            assign_labels="discretize",
                                            random_state=0,
                                            affinity='nearest_neighbors',
                                            n_neighbors=3).fit(x)

            previsoes = clustering.fit_predict(x)
            dataframe['equipes'] = previsoes

        return dataframe

    except TypeError:

        print('Número de grupos maior do que o número de visitas. Tente novamente.')


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
                          icon=folium.Icon(color=paleta_cores[loc[2]], icon='user', prefix="fa")
                          ).add_to(m)

        folium.Marker(location=(coord_origem[0], coord_origem[1]),
                      icon=folium.Icon(color='darkgreen', icon='medkit', prefix="fa")
                      ).add_to(m)

        # m.save('map.html')
        # webbrowser.open('map.html', new=2)
        return m

    except TypeError:

        print('Erro ao gerar o mapa. Tente novamente.')


def calcula_distancias(dataframe, origem):
    grupos = np.sort(dataframe['equipes'].unique())
    lista_grupos = []

    for g in grupos:

        incio = origem
        df = dataframe.query(f'equipes == {g}')
        enderecos = df['endereco_completo'].to_list()
        dic = {}

        for end in enderecos:
            coord_inicio = converte_endereco(incio)
            coord = converte_endereco(end)
            distancia = geopy.distance.distance(coord_inicio, coord).km

            dic[end] = distancia
        lista_grupos.append(dic)

    return lista_grupos


def retorna_rotas(rotas):
    dic_rotas_ordenadas = {}
    rotas_temp = []
    nome_col = []
    cont = 0

    for r in rotas:
        cont += 1
        rota_ordenada = sorted(r.items(), key=lambda x: x[1])

        for ro in rota_ordenada:
            rotas_temp.append(ro[0])

        dic_rotas_ordenadas[f'Equipe {cont}'] = rotas_temp.copy()
        rotas_temp.clear()

    df = pd.DataFrame.from_dict(dic_rotas_ordenadas, orient='index')
    df.fillna('-', inplace=True)

    for i in range(len(df.columns)):
        nome_col.append('')

    df.columns = nome_col

    return df
