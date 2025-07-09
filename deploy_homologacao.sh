#!/bin/bash

echo " Iniciando deploy para HOMOLOGAÇÃO..."

# Caminhos
APP_DIR="$HOME/tarefa-app"
HOMOLOG_DIR="$HOME/homologacao"

# Remove o antigo diretório de homologação
rm -rf "$HOMOLOG_DIR"

# Copia o projeto atualizado
cp -r "$APP_DIR" "$HOMOLOG_DIR"

# Acessa o diretório
cd "$HOMOLOG_DIR"

# Ativa o ambiente virtual
source venv/bin/activate

# Define a variável de ambiente com o banco de homologação
export DATABASE_URL="dbname=tarefa_homologacao user=vinicius host=localhost"

# Executa a aplicação na porta 5050
nohup python app.py --port=5050 > log_homologacao.out 2>&1 &
echo " Aplicação em HOMOLOGAÇÃO implantada na porta 5050."
