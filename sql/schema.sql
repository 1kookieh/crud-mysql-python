-- Criação do banco e da tabela de exemplo
CREATE DATABASE IF NOT EXISTS crud_app
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE crud_app;

CREATE TABLE IF NOT EXISTS registros (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    nome       VARCHAR(100) NOT NULL,
    email      VARCHAR(120) NOT NULL,
    telefone   VARCHAR(30) NULL,
    criado_em  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_registros_email UNIQUE (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
