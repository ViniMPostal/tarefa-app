import psycopg2
import os

def get_connection():
    ambiente = os.getenv("AMBIENTE", "desenvolvimento")

    if ambiente == "homologacao":
        dbname = "tarefa_homologacao"
    elif ambiente == "producao":
        dbname = "tarefa_producao"
    else:
        dbname = "tarefa_db"  # local (dev)

    return psycopg2.connect(
        dbname=dbname,
        user='vinicius',
        password='senha',
        host='localhost'
    )
