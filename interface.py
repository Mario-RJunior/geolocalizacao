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
            mapa = m.map_plot(df, legenda_equipes.index(num_equipes))

        except KeyError:
            st.write('Não há visitas previstas nesta data.')

        except AttributeError:
            st.write('Selecione um endereço válido.')

        except NameError:
            st.write('Preencha as opções anteriores corretamente.')

        else:
            st.markdown(f'## Mapa')
            folium_static(mapa)          

            # lista_rotas = m.calcula_distancias(df)
            # grupos_end = m.retorna_rotas(lista_rotas)
            # dist_max = m.distancias_min_max(df)
            # dist_min = m.distancias_min_max(df, maximo=False)

            # st.markdown(f'## Trajetórias')

            # cont = 0
            # for r, e in grupos_end.items():
            #     texto = ''
            #     st.markdown(f'### {r}')

            # for i in range(len(e)):
            #     texto += f'{e[i]} '

            #     if i != len(e) - 1:
            #         texto += '-> '

            # st.markdown(f'- {texto.strip()}.')

            # st.markdown(f'Distânca máxima: {str(round(dist_max[cont], 2)).replace(".", ",")} Km.')
            # st.markdown(f'Distânca mínima: {str(round(dist_min[cont], 2)).replace(".", ",")} Km.')
            # st.markdown(f'Economia de {str(round(dist_max[cont] - dist_min[cont], 2)).replace(".", ",")} Km.')

            # cont += 1
