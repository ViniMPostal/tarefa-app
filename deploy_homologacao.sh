#!/bin/bash

echo " Iniciando deploy para HOMOLOGAÇÃO..."

# Caminho do projeto
cd ~/tarefa-app || exit

# Ativa o ambiente virtual
source venv/bin/activate

# Define o ambiente de homologação
export FLASK_ENV=homologacao

# Executa o script SQL de migração (se existir)
if [ -f "migration.sql" ]; then
  echo " Executando migração do banco de dados (homologacao)..."
  psql -U postgres -d tarefa_homologacao -f migration.sql
else
  echo " Arquivo migration.sql não encontrado, pulando migração."
fi

# Finaliza processos na porta 5050, se houver
fuser -k 5050/tcp || true

# Inicia aplicação
nohup flask run --host=0.0.0.0 --port=5050 > ~/homologacao/log_homologacao.out 2>&1 &

echo " Aplicação em HOMOLOGAÇÃO implantada na porta 5050."
