import MySQLdb


# Fazendo a conexão com o banco de dados
def conectar():
    """
    Função para conectar ao servidor
    """
    try:
        conn = MySQLdb.connect(db='pacientes', host='localhost', user='root', password='')
        return conn
    except MySQLdb.Error as e:
        print(f'Erro na conexão ao MySQL Server: {e}.')


# Encerrando a conexão com o banco de dados
def desconectar(conn):
    """
    Função para desconectar do servidor.
    """
    if conn:
        conn.close()


# Listando as informações do banco de dados
def listar():
    """
    Função para listar os produtos
    """

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('select * from visitas')
    pacientes = cursor.fetchall()  # Vai pegar o resultado do comando anterior e transformar em uma lista!

    ids = []
    nomes = []
    ruas = []
    numeros = []
    bairros = []
    cidades = []
    estados = []
    datas = []

    if len(pacientes) > 0:

        for paciente in pacientes:
            ids.append(paciente[0])
            nomes.append(paciente[1])
            ruas.append(paciente[2])
            numeros.append(paciente[3])
            bairros.append(paciente[4])
            cidades.append(paciente[5])
            estados.append(paciente[6])
            datas.append(paciente[7])

    else:
        print('Registro não encontrado!')
    desconectar(conn)

    return ids, nomes, ruas, numeros, bairros, cidades, estados, datas
