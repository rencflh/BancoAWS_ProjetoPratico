-- Criação do Schema para o Data Warehouse
CREATE SCHEMA IF NOT EXISTS dw;

-- Criação das Tabelas de Dimensão

-- 1. Dimensão Departamento
CREATE TABLE IF NOT EXISTS dw.dim_departamento (
    sk_departamento SERIAL PRIMARY KEY,
    codigo VARCHAR(100), -- Código ou sigla original
    nome VARCHAR(255) NOT NULL
);

-- 2. Dimensão Semestre
CREATE TABLE IF NOT EXISTS dw.dim_semestre (
    sk_semestre SERIAL PRIMARY KEY,
    ano INT NOT NULL,
    periodo INT NOT NULL,
    UNIQUE(ano, periodo)
);

-- 3. Dimensão Professor
CREATE TABLE IF NOT EXISTS dw.dim_professor (
    sk_professor SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    tipo_jornada_trabalho VARCHAR(100),
    formacao VARCHAR(100),
    sk_departamento_lotacao INT,
    FOREIGN KEY (sk_departamento_lotacao) REFERENCES dw.dim_departamento(sk_departamento)
);

-- 4. Dimensão Disciplina (Componente Curricular)
CREATE TABLE IF NOT EXISTS dw.dim_disciplina (
    sk_disciplina SERIAL PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    cr_total INT,
    sk_departamento_responsavel INT,
    FOREIGN KEY (sk_departamento_responsavel) REFERENCES dw.dim_departamento(sk_departamento)
);

-- 5. Dimensão Campus
CREATE TABLE IF NOT EXISTS dw.dim_campus (
    sk_campus SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    UNIQUE(nome)
);

-- Criação da Tabela Fato
CREATE TABLE IF NOT EXISTS dw.fato_turma (
    sk_fato SERIAL PRIMARY KEY,
    codigo_turma VARCHAR(50), 
    sk_professor INT NOT NULL,
    sk_disciplina INT NOT NULL,
    sk_departamento INT NOT NULL,
    sk_semestre INT NOT NULL,
    sk_campus INT NOT NULL,
    
    -- Métricas
    num_discentes_matriculados INT DEFAULT 0,
    media_notas NUMERIC(5,2),
    num_aprovados INT DEFAULT 0,
    num_reprovados INT DEFAULT 0,
    
    FOREIGN KEY (sk_professor) REFERENCES dw.dim_professor(sk_professor),
    FOREIGN KEY (sk_disciplina) REFERENCES dw.dim_disciplina(sk_disciplina),
    FOREIGN KEY (sk_departamento) REFERENCES dw.dim_departamento(sk_departamento),
    FOREIGN KEY (sk_semestre) REFERENCES dw.dim_semestre(sk_semestre),
    FOREIGN KEY (sk_campus) REFERENCES dw.dim_campus(sk_campus)
);

-- Criação do Usuário de Integração (ETL) e Concessão de Permissões
-- OBS: A senha deve ser alterada conforme padrão de segurança da AWS RDS
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'etl_user') THEN
      CREATE ROLE etl_user LOGIN PASSWORD 'SenhaForte123!';
   END IF;
END
$do$;

GRANT USAGE ON SCHEMA dw TO etl_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA dw TO etl_user;
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA dw TO etl_user;

-- Para garantir permissões sobre futuras tabelas
ALTER DEFAULT PRIVILEGES IN SCHEMA dw GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO etl_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA dw GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO etl_user;
