import streamlit as st
from geolocalizador import Mapzer
from streamlit_folium import folium_static
from multiprocessing.pool import ThreadPool

st.title('Mapzer App')
st.sidebar.title('Menu')

origem = st.sidebar.selectbox('Endereço de origem', ['Selecione um endereço',
                                                     'Av. Cezar Hilal, 700, Vitória - ES'])
data = st.sidebar.date_input('Data')
equipes = st.sidebar.selectbox('Número de equipes', [1, 2, 3, 4, 5, 6, 7])

# UndefinedVariableError 
legenda_equipes = [f'Equipe {c}' if c != 0 else 'Todas as equipes' \
        for c in range(0, equipes + 1)]

num_equipes = st.sidebar.radio('Selecione uma trajetória', legenda_equipes)
n = legenda_equipes.index(num_equipes)

UndefinedVariableError = ''

if __name__ == '__main__':
    m = Mapzer(origem, data, equipes)

    try:
        bd = m.acessa_bd()

    except AttributeError:
        st.write('Conexão com banco de dados não realizada.')

    else:
        df = m.gera_dataframe()
        df = m.agrupa_visitas(df)

        try:
            mapa = m.map_plot(df, n)

        except KeyError:
            st.write('Não há visitas previstas nesta data.')

        except AttributeError:
            st.write('Selecione um endereço válido.')

        except NameError:
            st.write('Preencha as opções anteriores corretamente.')

        else:
            st.markdown(f'## Mapa')
            folium_static(mapa)                      

            if n != 0:
                lista_rotas = m.calcula_distancias(df, n)
                grupos_end = m.retorna_rotas(lista_rotas, n)

                st.markdown(f'## Trajetória')

                for g, e in grupos_end.items():
                    for end in e:
                        st.write(f'- {end}')

                dist_max = m.distancias_min_max(df, n)
                dist_min = m.distancias_min_max(df, n, False)

                st.markdown('## Distâncias')

                st.markdown(f'Distância máxima: {str(round(dist_max, 2)).replace(".", ",")} Km.')
                st.markdown(f'Distância mínima: {str(round(dist_min, 2)).replace(".", ",")} Km.')
                st.markdown(f'Economia de {str(round(dist_max - dist_min, 2)).replace(".", ",")} Km.')