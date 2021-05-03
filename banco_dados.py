import psycopg2


def conectar():
    """
    Função para conectar ao servidor.
    """
    try:
        conn = psycopg2.connect(
            database='pacientes',
            host='localhost',
            user='teste_db',
            password='postgres')

        return conn

    except psycopg2.Error as e:
        print(f'Erro na conexão ao MySQL Server: {e}.')


def desconectar(conn):
    """
    Função para desconectar do servidor.
    :param conn: Conexão que se deseja encerrar.
    """
    if conn:
        conn.close()


def listar(data):
    """
    Função para listar as informações dos pacientes.
    :param data: Data em que se deseja filtrar os registros do banco de dados.
    :return: Tupla com as listas de todas as colunas da tabela do banco de dados.
    """

    sql = f"SELECT * FROM visitas WHERE data_visita = '{data}';"

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
