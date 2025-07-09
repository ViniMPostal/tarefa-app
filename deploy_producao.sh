#!/bin/bash

echo " Iniciando deploy para PRODUÇÃO..."

# Caminho do projeto
cd ~/tarefa-app || exit

# Ativa o ambiente virtual
source venv/bin/activate

# Define o ambiente de produção
export FLASK_ENV=producao

# Executa o script SQL de migração (se existir)
if [ -f "migration.sql" ]; then
  echo " Executando migração do banco de dados (producao)..."
  psql -U postgres -d tarefa_producao -f migration.sql
else
  echo " Arquivo migration.sql não encontrado, pulando migração."
fi

# Finaliza processos na porta 6060, se houver
fuser -k 6060/tcp || true

# Inicia aplicação
nohup flask run --host=0.0.0.0 --port=6060 > ~/producao/log_producao.out 2>&1 &

echo " Aplicação em PRODUÇÃO implantada na porta 6060."
