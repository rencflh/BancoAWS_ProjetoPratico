# Sistema de Gestão Universitária - Engenharia de Dados

Projeto prático final desenvolvido para a disciplina de Engenharia de Dados (2026.1) sob orientação do Prof. André Britto de Carvalho. O sistema simula a gestão acadêmica completa de uma universidade, transitando pela modelagem transacional (OLTP) em modelo relacional, mapeamento para o modelo NoSQL, e culminando na construção de um Data Warehouse populado por pipelines de ETL (Integração de Dados).

## Arquitetura e Tecnologias

O projeto consolida as três fases exigidas utilizando múltiplas tecnologias integradas em um ambiente de nuvem:

* **Banco de Dados Relacional (Fase 1):** PostgreSQL
* **Banco de Dados NoSQL (Fase 2):** MongoDB
* **Banco de Dados Analítico / DW (Fase 3):** PostgreSQL hospedado no AWS RDS
* **Linguagens:** Java (JDBC) e Python (PyMongo)
* **ETL e Integração:** Apache Hop
* **Infraestrutura:** Instâncias EC2 e RDS na AWS Academy

---

## Requisitos e Funcionalidades Implementadas

### Parte 1: CRUD Relacional (Java + PostgreSQL)
Implementação de um sistema interativo via CLI que efetua as operações de manipulação de dados (CRUD) nas tabelas usuário, estudante, vínculo e curso. O banco foi hospedado na AWS.
- **Padrão DAO (Data Access Object):** Isolamento entre a camada de negócio e o SQL.
- **Segurança (PreparedStatement):** Proteção contra SQL Injection.

### Parte 2: Mapeamento e CRUD NoSQL (Python + MongoDB)
Migração lógica das tabelas do modelo relacional para o modelo orientado a documentos no MongoDB.
- **Modelo Híbrido (Embedding):** Visando performance de leitura, os dados das antigas tabelas `vinculo` e `cursa` foram embutidos como arrays dentro do documento principal do `Estudante`.
- **Garantia de Restrições:** Atendimento estrito aos requisitos de proteção de dados:
- **Not Null e Domínio:** Garantidos nativamente via JSON Schema Validation no banco de dados.
- **Integridade Referencial (FK) e PK:** Garantidas via aplicação (Python), validando a existência de documentos pai antes das inserções e simulando *On Delete Set Null*.
- **Segurança de Credenciais:** Uso de `python-dotenv` para isolar IPs e senhas.

### Parte 3: Integração de Dados (ETL e Esquema Estrela)
Construção de um Data Warehouse no AWS RDS populado através de rotinas de ETL construídas no Apache Hop, integrando bases heterogêneas.
- **Modelagem Multidimensional (Esquema Estrela):** Focada nas turmas de graduação, com dimensões para professores, disciplinas, departamentos, semestres e campus.
- **Cálculo de Métricas:** A tabela de fatos consolida e armazena o número de discentes matriculados, média das notas, número de aprovados e número de reprovados.
- **Fontes de Dados do Pipeline:**
  1. O banco PostgreSQL relacional desenvolvido na Parte 1.
  2. Arquivos `.csv` reais do portal de dados abertos da UFS (`dados.ufs.br`), filtrando turmas de 2019 até 2025.
- **Segurança RDS:** Criação de usuário e papéis específicos com as permissões exatas necessárias para o povoamento do banco de dados pelo pipeline.

---

## Como Executar o Projeto

### Pré-requisitos
* **Java JDK 11+** (Para a Parte 1)
* **Python 3.10+** (Para a Parte 2)
* **Apache Hop** (Para a Parte 3)
* Bancos de dados **PostgreSQL** e **MongoDB** rodando ativamente em instâncias (EC2/RDS) da AWS.

### Executando a Parte 1: CRUD Relacional (Java)
1. **Configuração do Banco:** Certifique-se de que o PostgreSQL está rodando na sua instância AWS EC2 e o script `.sql` de criação das tabelas da universidade foi executado.
2. **Driver JDBC:** Baixe o driver `postgresql.jar` e garanta que ele está adicionado ao *Classpath* do seu projeto (na sua IDE ou gerenciador de dependências).
3. **Configuração de Credenciais:** No código fonte Java (na classe responsável pela conexão), atualize a string de conexão com o IP, usuário e senha do seu servidor PostgreSQL na AWS.
4. **Execução:** Compile o projeto e execute a classe principal `MainMenu.java` para iniciar o menu interativo no terminal.

### Executando a Parte 2: CRUD NoSQL (Python)
1. **Dependências:** Abra o terminal na raiz do projeto e instale as bibliotecas necessárias para a conexão e segurança:
   ```bash
   pip install pymongo python-dotenv
   ```
2. **Variáveis de Ambiente:** Na raiz do projeto, crie um arquivo chamado .env e adicione a sua string de conexão (substitua pelo IP atualizado da sua máquina AWS):
   ```bash
   MONGO_URI=mongodb://seu_usuario:sua_senha@IP_DA_AWS:27017/universidade?authSource=admin
   ```
3. **Carga Inicial:** Execute o script abaixo para criar as coleções com as regras de validação (JSON Schema) e popular o banco convertendo os dados transacionais para o modelo de documentos:
   ```bash
   python scripts_mongodb/carga_inicial.py
   ```
4. **Execução do Sistema:** Após a mensagem de sucesso da carga inicial, inicie o CLI de gerenciamento NoSQL executando:
   ```bash
   python scripts_mongodb/main.py
   ```
### Executando a Parte 3: Integração de Dados (Apache Hop)
1. As tabelas do AWS RDS estarão inicialmente vazias, conforme exigido para a avaliação.
2. Abra a interface do **Apache Hop**.
3. Acesse os pipelines (`.hpl`) desenvolvidos e localizados na pasta `dados/` deste repositório.
4. Execute os pipelines de carga de forma modular (ex: `pipeline_campus.hpl`, `pipeline_componentes.hpl`, `pipeline_fato_turma.hpl`, etc.). Os dados transacionais da Fase 1 e os arquivos CSV abertos da UFS (também contidos na pasta `dados/`) serão lidos, transformados e carregados no Esquema Estrela, preenchendo as dimensões e os fatos.

---

## Equipe de Desenvolvimento
* Leonardo Souza Silva
* Mateus Alves de Almeida Rodrigues Dantas
* Renato Vasconcelos Campos Filho

---
