import streamlit as st
from geolocalizador import *

st.title('Mapster')
st.sidebar.title('Menu')

origem = st.sidebar.text_input('Endereço de origem')
data = st.sidebar.date_input('Data')
equipes = st.sidebar.selectbox('Número de equipes', [1, 2, 3, 4, 5, 6, 7])

if __name__ == '__main__':
    bd = acessa_bd(data)
    df = gera_dataframe(bd)
    df = agrupa_visitas(equipes, df)
    st.write(df)
