#!/bin/bash

echo "Iniciando deploy para o ambiente de homologação..."

# Caminho na VM onde o projeto está localizado
APP_DIR=~/tarefa-app
HOMOLOG_DIR=~/homologacao

# Remove versão antiga
rm -rf "$HOMOLOG_DIR"

# Copia nova versão para homologação
cp -r "$APP_DIR" "$HOMOLOG_DIR"

# Ativa ambiente virtual e inicia aplicação
cd "$HOMOLOG_DIR"
source venv/bin/activate

# Mata qualquer processo anterior rodando na porta 5050
fuser -k 5050/tcp || true

# Sobe a aplicação
nohup python app.py --port=5050 > log_homologacao.txt 2>&1 &

echo "Deploy concluído com sucesso no ambiente de homologação!"
