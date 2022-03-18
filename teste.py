from geolocalizador import Mapzer

origem = 'Av. Cezar Hilal, 700, Vitória - ES'
data = '2021/03/20'
equipes = 3

m = Mapzer(origem, data, equipes)

bd = m.acessa_bd()
df = m.gera_dataframe()
df = m.agrupa_visitas(df)

print(df)

enderecos = ['Rua Hermes Bastos, 40, Vitória - ES',
             'Avenida Américo Buaiz, 200, Vitória - ES',
             'Avenida Vitória, 1690, Vitória - ES',
             'Avenida Fernando Ferrari, 514, Vitória - ES',
             'Avenida Dante Michelini, 1845, Vitória - ES',
             'Av. Luciano das Neves, 2418, Vila Velha - ES',
             'Av. Doutor Olivio Lira, 353, Vila Velha - ES',
             'Av. Nossa Senhora da Penha, 356, Vitória - ES',
             'R. Maestro Antônio Cícero, 111, Serra - ES',
             'Av. Coronel José Martins de Figueiredo, 359,  Vitória - ES',
             'Av. Mario Gurgel, 5353, Cariacica - ES',
             'R. Rio Branco, Cariacica - ES, 29147-709'
]

for e in enderecos:
    x = m.converte_endereco(e)
    print(x[0], x[1])

"""x = m.converte_endereco('Rua Meridional, 200 - Alto Lage, Cariacica - ES')
print(x[0], x[1])"""