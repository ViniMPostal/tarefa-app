#!/bin/bash

echo " Iniciando deploy para PRODUÇÃO..."

# Copia os arquivos da homologação para produção
cp -r ~/homologacao/* ~/producao/

# Executa a migration no banco de produção
echo " Aplicando migration no banco de produção..."
PGPASSWORD=senha psql -U postgres -d tarefa_producao -f ~/producao/migration.sql

# Ativa o ambiente virtual e executa o app na porta 6060
cd ~/producao
source venv/bin/activate
nohup python app.py --port=6060 > log_producao.out 2>&1 &

echo " Aplicação em PRODUÇÃO implantada na porta 6060."
