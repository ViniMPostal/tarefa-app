import unittest
from app import app
from flask import session

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_page_loads(self):
        response = self.app.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_login_incorreto(self):
        response = self.app.post('/auth/login', data=dict(email='errado@email.com', senha='123'), follow_redirects=True)
        self.assertIn(b'E-mail ou senha incorretos', response.data)

    def test_login_vazio(self):
        response = self.app.post('/auth/login', data=dict(email='', senha=''), follow_redirects=True)
        self.assertIn(b'E-mail ou senha incorretos', response.data)
    def test_logout_limpa_sessao(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/auth/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_protecao_rotas_sem_login(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Login', response.data)


class TarefasTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1

    def test_listar_tarefas(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tarefas Cadastradas', response.data)

    def test_criar_tarefa_get(self):
        response = self.app.get('/criar')
        self.assertEqual(response.status_code, 200)

    def test_criar_tarefa_post_invalida(self):
        response = self.app.post('/criar', data={
            'descricao': '',
            'data_criacao': '2025-07-01',
            'data_prevista': '2025-07-10',
            'data_encerramento': '',
            'situacao': 'Pendente'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Deve retornar a página novamente

    def test_criar_tarefa_post_valida(self):
        response = self.app.post('/criar', data={
            'descricao': 'Teste',
            'data_criacao': '2025-07-01',
            'data_prevista': '2025-07-10',
            'data_encerramento': '',
            'situacao': 'Pendente'
        }, follow_redirects=True)
        self.assertIn(b'Tarefas Cadastradas', response.data)

    def test_criar_redirect_se_nao_logado(self):
        with app.test_client() as c:
            response = c.get('/criar', follow_redirects=True)
            self.assertIn(b'Login', response.data)


class FilterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1

    def test_filtro_por_data_prevista(self):
        response = self.app.get('/?data_prevista=2025-07-03')
        self.assertEqual(response.status_code, 200)

    def test_filtro_por_situacao(self):
        response = self.app.get('/?situacao=Conclu%C3%ADdo')
        self.assertEqual(response.status_code, 200)

    def test_filtros_combinados(self):
        response = self.app.get('/?data_prevista=2025-07-03&situacao=Pendente')
        self.assertEqual(response.status_code, 200)

    def test_filtro_sem_resultado(self):
        response = self.app.get('/?data_prevista=1900-01-01&situacao=Conclu%C3%ADdo')
        self.assertIn(b'<table>', response.data)

    def test_botao_filtro_existe(self):
        response = self.app.get('/')
        self.assertIn(b'Filtrar', response.data)


class PdfTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_pdf_sem_login_redireciona(self):
        response = self.app.get('/exportar_pdf', follow_redirects=True)
        self.assertIn(b'Login', response.data)

    def test_pdf_gerado_com_login(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/exportar_pdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

    def test_pdf_filtrado(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/exportar_pdf?data_prevista=2025-07-03')
        self.assertEqual(response.status_code, 200)

    def test_pdf_nome_arquivo(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/exportar_pdf')
        self.assertIn('attachment; filename=tarefas.pdf', response.headers['Content-Disposition'])

    def test_pdf_conteudo_binario(self):
        with self.app.session_transaction() as sess:
            sess['user_id'] = 1
        response = self.app.get('/exportar_pdf')
        self.assertTrue(response.data.startswith(b'%PDF'))

if __name__ == '__main__':
    unittest.main()
