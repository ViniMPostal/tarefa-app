from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, send_file
from db import get_connection
from reportlab.pdfgen import canvas
from io import BytesIO
from auth import auth_bp
from email_utils import enviar_email

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def listar_tarefas():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    data_prevista = request.args.get('data_prevista')
    situacao = request.args.get('situacao')

    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT * FROM tarefa WHERE 1=1"
    params = []

    if data_prevista:
        query += " AND data_prevista = %s"
        params.append(data_prevista)

    if situacao and situacao != "Todos":
        query += " AND situacao = %s"
        params.append(situacao)

    cur.execute(query, tuple(params))
    tarefas = cur.fetchall()
    conn.close()

    return render_template('tarefas.html', tarefas=tarefas)

@app.route('/criar', methods=['GET', 'POST'])
def criar_tarefa():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        descricao = request.form['descricao']
        data_prevista = request.form['data_prevista']
        situacao = request.form['situacao']
        data_criacao = request.form['data_criacao']
        data_encerramento = request.form['data_encerramento']

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tarefa (descricao, data_criacao, data_prevista, data_encerramento, situacao)
            VALUES (%s, %s, %s, %s, %s)
        """, (descricao, data_criacao, data_prevista, data_encerramento or None, situacao))
        conn.commit()
        conn.close()

        enviar_email("viniboyppostal@gmail.com", "Nova Tarefa Criada", f"Tarefa '{descricao}' criada com sucesso!")

        return redirect(url_for('listar_tarefas'))
    return render_template('criar_tarefa.html')

@app.route('/exportar_pdf')
def exportar_pdf():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    data_prevista = request.args.get('data_prevista')
    situacao = request.args.get('situacao')

    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT * FROM tarefa WHERE 1=1"
    params = []

    if data_prevista:
        query += " AND data_prevista = %s"
        params.append(data_prevista)

    if situacao and situacao != "Todos":
        query += " AND situacao = %s"
        params.append(situacao)

    cur.execute(query, tuple(params))
    tarefas = cur.fetchall()
    conn.close()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(200, 800, "Relatório de Tarefas")

    y = 760
    for tarefa in tarefas:
        linha = f"{tarefa[0]} - {tarefa[1]} - {tarefa[2]} - {tarefa[3]} - {tarefa[4]} - {tarefa[5]}"
        pdf.drawString(50, y, linha)
        y -= 20
        if y < 50:
            pdf.showPage()
            y = 800

    pdf.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="tarefas.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    import sys

    # Porta padrão (desenvolvimento)
    porta = 5000
    ambiente = "desenvolvimento"

    # Verifica se foi passado argumento como --port=XXXX
    for arg in sys.argv:
        if arg.startswith("--port="):
            try:
                porta = int(arg.split("=")[1])
                if porta == 5050:
                    ambiente = "homologação"
                elif porta == 6060:
                    ambiente = "produção"
            except ValueError:
                print("⚠️ Porta inválida! Usando a porta padrão 5000.")

    print(f"✅ Iniciando em modo: {ambiente.upper()} na porta {porta}")
    app.run(host='0.0.0.0', port=porta)



