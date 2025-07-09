#!/bin/bash

echo " Iniciando deploy para HOMOLOGAÇÃO..."

# Copia todos os arquivos do projeto atual para a pasta de homologação
cp -r * ~/homologacao/

# Executa o script SQL de migration no banco de homologação
echo "🛠️ Aplicando migration no banco de homologação..."
PGPASSWORD=senha psql -U postgres -d tarefa_homologacao -f ~/homologacao/migration.sql

# Ativa o ambiente virtual e executa o app na porta 5050
cd ~/homologacao
source venv/bin/activate
nohup python app.py --port=5050 > log_homologacao.out 2>&1 &

echo " Aplicação em HOMOLOGAÇÃO implantada na porta 5050."
