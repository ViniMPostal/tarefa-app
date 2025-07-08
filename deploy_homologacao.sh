#!/bin/bash

echo "Iniciando deploy para ambiente de homologação..."

# Parâmetros
VM_USER="univates"
VM_HOST="177.44.248.80"
APP_DIR="homologacao"
LOCAL_DIR="."
PORTA=5050

# Envia os arquivos para a VM via rsync (ignora .git e venv)
rsync -avz --exclude '.git' --exclude 'venv' --exclude '__pycache__' $LOCAL_DIR $VM_USER@$VM_HOST:~/$APP_DIR

# Executa remotamente os comandos necessários
ssh $VM_USER@$VM_HOST << EOF
cd ~/$APP_DIR
source venv/bin/activate
fuser -k ${PORTA}/tcp || true
nohup python app.py --port=${PORTA} > flask.log 2>&1 &
EOF

echo "Deploy para homologação concluído!"
