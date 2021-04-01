from geolocalizador import *

if __name__ == '__main__':
    perg_local = str(input('Digite o endereço de partida: '))
    
    try:
        
        perg_equipes = int(input('Quantas equipes disponíveis para visitas? '))

    except ValueError:

        print('Número de equipes inválido. Tente novamente.')

    else:

        perg_data = str(input('Insira a data da visita (dd/mm/aaaa): '))

        bd = acessa_bd(perg_data)
        df = gera_dataframe(bd)
        df = agrupa_visitas(perg_equipes, df)

        try:

            map_plot(df, perg_local)

        except AttributeError:

            print('Erro no endereço de origem. Tente novamente.')

        except KeyError:
            print('Erro na data. Tente novamente.')

        else:

            calcula_rota(df, perg_local)
