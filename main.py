from geolocalizador import *

if __name__ == '__main__':
    bd = acessa_bd()
    df = gera_dataframe(bd)
    perg_local = str(input('Digite a localização (Bairro, Cidade - UF): '))
    perg_equipes = int(input('Quantas equipes disponíveis para visitas? '))
    perg_data = str(input('Insira a data da visita (dd/mm/aaaa): '))
    df = formata_data(df, perg_data)
    df = agrupa_visitas(perg_equipes, df)
    map_plot(df)
    #calcula_rota(df, perg_local)
