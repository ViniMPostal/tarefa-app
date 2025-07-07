DROP TABLE IF EXISTS tarefa;

CREATE TABLE tarefa (
    id SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL,
    data_criacao DATE NOT NULL,
    data_prevista DATE NOT NULL,
    data_encerramento DATE,
    situacao VARCHAR(20) NOT NULL
);

INSERT INTO tarefa (descricao, data_criacao, data_prevista, data_encerramento, situacao) VALUES
('Comprar mantimentos', '2025-07-01', '2025-07-03', NULL, 'Pendente'),
('Finalizar relatório', '2025-07-01', '2025-07-05', NULL, 'Em andamento'),
('Estudar Python', '2025-07-01', '2025-07-10', NULL, 'Pendente'),
('Reunião com equipe', '2025-07-02', '2025-07-02', '2025-07-02', 'Concluído'),
('Enviar e-mail para cliente', '2025-07-01', '2025-07-02', NULL, 'Pendente'),
('Revisar projeto', '2025-07-01', '2025-07-04', NULL, 'Pendente'),
('Backup do servidor', '2025-07-01', '2025-07-06', NULL, 'Pendente'),
('Treinamento interno', '2025-07-01', '2025-07-08', NULL, 'Pendente'),
('Atualizar site', '2025-07-01', '2025-07-07', NULL, 'Em andamento'),
('Enviar documentação', '2025-07-01', '2025-07-03', NULL, 'Pendente');
