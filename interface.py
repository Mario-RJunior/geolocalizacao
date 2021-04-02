import streamlit as st

st.title('Mapster')
st.sidebar.title('Menu')

st.sidebar.text_input('Endereço de origem')
st.sidebar.date_input('Data')
st.sidebar.selectbox('Número de equipes', [1, 2, 3, 4, 5, 6, 7])

