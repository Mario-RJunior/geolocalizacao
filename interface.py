import streamlit as st
from geolocalizador import *
from streamlit_folium import folium_static

st.title('Mapzer App')
st.sidebar.title('Menu')

origem = st.sidebar.selectbox('Endereço de origem', ['Selecione um endereço',
                                                     'Av. Cezar Hilal, 700, Vitória - ES'])
data = st.sidebar.date_input('Data')
equipes = st.sidebar.selectbox('Número de equipes', [1, 2, 3, 4, 5, 6, 7])

if __name__ == '__main__':
    try:
        bd = acessa_bd(data)

    except AttributeError:
        st.write('Conexão com banco de dados não realizada.')

    else:
        df = gera_dataframe(bd)
        df = agrupa_visitas(df, equipes)

        try:
            m = map_plot(df, origem)

        except KeyError:
            st.write('Não há visitas previstas nesta data.')

        except AttributeError:
            st.write('Selecione um endereço válido.')

        else:
            folium_static(m)
            lista_rotas = calcula_distancias(df, origem)
            grupos_end = retorna_rotas(lista_rotas)

            for r, e in grupos_end.items():
                texto = ''
                st.markdown(f'### {r}')

                for i in range(len(e)):
                    texto += f'{e[i]} '

                    if i != len(e) - 1:
                        texto += '-> '

                st.markdown(f'- {texto.strip()}.')
