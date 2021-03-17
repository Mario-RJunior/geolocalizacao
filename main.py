from geolocalizador import *

if __name__ == '__main__':
    bd = acessa_bd()
    df = gera_dataframe(bd)
    perg_local = str(input('Digite a localização (Bairro, Cidade - UF): '))
    perg_equipes = int(input('Quantas equipes disponíveis para visitas? '))
    df = agrupa_visitas(perg_equipes, df)
    print(df)
    #calcula_rota(df, perg_local)
