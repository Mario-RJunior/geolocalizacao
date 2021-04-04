import streamlit as st
from geolocalizador import *
from streamlit_folium import folium_static

st.title('Mapster')
st.sidebar.title('Menu')

origem = st.sidebar.selectbox('Endereço de origem', ['Selecione um endereço',
                                                     'Av. Cezar Hilal, 700, Vitória - ES'])
data = st.sidebar.date_input('Data')
equipes = st.sidebar.selectbox('Número de equipes', [1, 2, 3, 4, 5, 6, 7])

if __name__ == '__main__':
    bd = acessa_bd(data)
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
