from geolocalizador import *

if __name__ == '__main__':
    perg_local = str(input('Digite o endereço de partida: '))

    perg_equipes = ''
    try:
        perg_equipes = int(input('Quantas equipes disponíveis para visitas? '))

    except ValueError:
        print('Erro ao especificar o número de equipes! Tente novamente.')

    perg_data = str(input('Insira a data da visita (dd/mm/aaaa): '))

    #bd = acessa_bd(perg_data)
    #df = gera_dataframe(bd)
    #df = agrupa_visitas(perg_equipes, df)
    #map_plot(df, perg_local)
    #calcula_rota(df, perg_local)
