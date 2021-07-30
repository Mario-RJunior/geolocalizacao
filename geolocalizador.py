import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance
from banco_dados import Bd
from sklearn.cluster import SpectralClustering
import folium
import numpy as np
from datetime import datetime


class Mapzer(Bd):

    def __init__(self, origem, data, quantidade):
        self.origem = origem
        self.data = data
        self.quantidade = quantidade
        self.dados = {}

    def acessa_bd(self):
        """
        Função que chama a função listar e filtra as informações do banco de dados pela data recebida.
        :return: Retorna um dicionário com os dados do banco de dados.
        """
        colunas = ['id', 'Nome', 'Rua', 'Numero_rua', 'Bairro', 'Cidade', 'Estado', 'Data']
        lista_dados = list(zip(colunas, Bd.listar(self, data=self.data)))

        for c in lista_dados:
            self.dados[c[0]] = c[1]

        return self.dados

    def gera_dataframe(self):
        """
        Função que gera um dataframe a partir das informações do banco de dados.
        :return: Dataframe completo com informações do banco de dados.
        """
        dataframe = pd.DataFrame(self.dados)
        dataframe['endereco_completo'] = \
            dataframe['Rua'].astype(str) + ', ' + dataframe['Numero_rua'].astype(str) + ', ' + \
            dataframe['Cidade'].astype(str) + ' - ' + dataframe['Estado'].astype(str)

        return dataframe

    def converte_endereco(self, endereco):
        """
        Função que recebe um endereço e o converte para coordenadas geográficas.
        :param endereco: Endereço a que se deseja calcular suas coordenadas geográficas.
        :return: Coordenada geográfica do endereço.
        """
        geolocator = Nominatim(user_agent="my_user_agent", timeout=20)
        pais = "BR"
        loc = geolocator.geocode(endereco + ',' + pais)

        return loc.latitude, loc.longitude

    def agrupa_visitas(self, dataframe):
        """
        Função que faz o agrupamento dos pacientes a partir da sua localização.
        :param dataframe: Dataframe que possue endereço dos clientes.
        :return: Dataframe com colunas extras para latitude, longitute e grupo a qual o paciente foi associado.
        """

        try:

            serie = dataframe['endereco_completo'].apply(self.converte_endereco)

            dataframe['latitude'] = serie.apply(lambda lat: lat[0])
            dataframe['longitude'] = serie.apply(lambda lon: lon[1])

            if len(dataframe) == 0:

                pass

            elif len(dataframe) in [1, 2, 3]:

                dataframe['equipes'] = 0

            else:

                x = dataframe.loc[:, ['latitude', 'longitude']].values

                clustering = SpectralClustering(n_clusters=self.quantidade,
                                                assign_labels="discretize",
                                                random_state=0,
                                                affinity='nearest_neighbors',
                                                n_neighbors=3).fit(x)

                previsoes = clustering.fit_predict(x)
                dataframe['equipes'] = previsoes
                dataframe['equipes'] = dataframe['equipes'].apply(lambda x: x + 1)

        except TypeError:

            print('Número de grupos maior do que o número de visitas. Tente novamente.')

        else:

            return dataframe

    def map_plot(self, dataframe, equipe):
        """
        Função para plotar o mapa com as localizações dos endereços.
        :param dataframe: Dataframe que possui as coordenadas geográficas dos endereços.
        :return: Retorna o respectivo mapa.
        """
        try:

            paleta_cores = (
                'blue', 'orange', 'darkred', 'pink', 'darkpurple', 'cadetblue',
                'lightred', 'darkgreen', 'purple', 'darkblue', 'black', 'red',
                'lightblue', 'beige', 'green', 'lightgray', 'lightgreen', 'gray',
                'white'
                )

            if equipe != 0:
                dataframe = dataframe.query(f'equipes == {equipe}')   

            lat = dataframe['latitude'].to_list()
            lon = dataframe['longitude'].to_list()
            equipes = dataframe['equipes'].to_list()
            coord_origem = self.converte_endereco(self.origem)

            coordenadas = list(zip(lat, lon, equipes))
            m = folium.Map(location=[-20.2999473, -40.3221028], zoom_start=12)

            for loc in coordenadas:
                folium.Marker(location=(loc[0], loc[1]),
                            icon=folium.Icon(color=paleta_cores[loc[2]], icon='user', prefix="fa"),
                            popup=f'Equipe {loc[2]}'
                            ).add_to(m)

            folium.Marker(location=(coord_origem[0], coord_origem[1]),
                        icon=folium.Icon(color='darkgreen', icon='medkit', prefix="fa"),
                        popup='Origem'
                        ).add_to(m)

        except TypeError:

            print('Erro ao gerar o mapa. Tente novamente.')

        else:

            return m
       
    def calcula_distancias(self, dataframe, equipe):
        lista_grupos = []
        df = dataframe.query(f'equipes == {equipe}')
        inicio = self.origem
        enderecos = df['endereco_completo'].to_list()
        dic = {}
        
        for end in enderecos:
            coord_inicio = self.converte_endereco(inicio)
            coord = self.converte_endereco(end)

            distancia = geopy.distance.distance(coord_inicio, coord).km
            dic[end] = distancia

        lista_grupos.append(dic)

        return lista_grupos

    def retorna_rotas(self, rotas, equipe):
        """
        Função que recebe um lista com as rotas e ordena os endereços de forma crescente das distâncias.
        :param rotas: Lista com os endereços e suas distâncias.
        :return: Lista com os endereços ordenados pela distância.
        """

        dic_rotas_ordenadas = {}
        rotas_temp = []

        for r in rotas:
            rota_ordenada = sorted(r.items(), key=lambda x: x[1])

            for ro in rota_ordenada:
                rotas_temp.append(ro[0])

            dic_rotas_ordenadas[f'Equipe {equipe}'] = rotas_temp.copy()
            rotas_temp.clear()

        return dic_rotas_ordenadas

    def distancias_min_max(self, dataframe, equipe, maximo=True):
        """
        Função que retorna distâncias máximas e mínimas de cada rota.
        :param dataframe: Dataframe atualizado.
        :param maximo: Indica se queremos retornar as distâncias máximas ou mínimas. Se True = máxima, se False = mínima.
        :return: Lista com os endereços com suas respectivas distâncas.
        """
        df = dataframe.query(f'equipes == {equipe}')
        lista_distancias = []
        dist_min_max = []

        inicio = self.origem
        enderecos = df['endereco_completo'].to_list()
        dic_temp = {}
        dic = {}
        min_dist = 0

        while len(enderecos) > 0:

            for end in enderecos:
                coord_inicio = self.converte_endereco(inicio)
                coord = self.converte_endereco(end)
                distancia = geopy.distance.distance(coord_inicio, coord).km

                dic_temp[end] = distancia

            if maximo:
                mais_perto = max(dic_temp, key=dic_temp.get)

            else:
                mais_perto = min(dic_temp, key=dic_temp.get)

            dic[mais_perto] = dic_temp[mais_perto]
            inicio = mais_perto

            min_dist += dic_temp[mais_perto]
            dic_temp.clear()
            enderecos.remove(mais_perto)

        lista_distancias.append(dic)

        for d in lista_distancias:
            soma = 0
            for _, v in d.items():
                soma += v
            dist_min_max.append(soma)

        return dist_min_max[0]

    def gera_log(self, erro):
        """
        Função quer cria / atualiza um arquivo de texto com os erros de execução.
        :param erro: Mensagem de erro gerada.
        """
        with open('log_erro.txt', 'a') as f:
            data = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

            f.write(data + ' - ')
            f.write(str(erro))
            f.write('\n')
