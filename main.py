from geolocalizador import *

if __name__ == '__main__':
    try:

        perg_local = str(input('Digite a localização (Bairro, Cidade - UF): '))
        perg_equipes = int(input('Quantas equipes disponíveis para visitas? '))
        perg_data = str(input('Insira a data da visita (dd/mm/aaaa): '))

        bd = acessa_bd(perg_data)
        df = gera_dataframe(bd)
        df = agrupa_visitas(perg_equipes, df)
        map_plot(df, perg_local)
        calcula_rota(df, perg_local)

    except ValueError:
        print('Valor incorreto. Preencher novamente.')
