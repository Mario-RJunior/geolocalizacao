import MySQLdb


def conectar():
    """
    Função para conectar ao servidor.
    """
    try:
        conn = MySQLdb.connect(db='pacientes', host='localhost', user='root', password='')
        return conn
    except MySQLdb.Error as e:
        print(f'Erro na conexão ao MySQL Server: {e}.')


def desconectar(conn):
    """
    Função para desconectar do servidor.
    """
    if conn:
        conn.close()


def listar():
    """
    Função para listar as informações dos pacientes.
    """

    sql = f'select * from visitas'

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(sql)
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
