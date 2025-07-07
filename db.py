import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname='tarefa_db',
        user='vinicius',
        password='senha',
        host='localhost'
    )
