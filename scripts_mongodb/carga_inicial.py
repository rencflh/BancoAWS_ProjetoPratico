from pymongo import MongoClient

def popular_banco_completo():
    # 1. CONEXÃO COM O MONGODB ATLAS
    # Substitua pela sua string de conexão real

    string_conexao = "mongodb+srv://Maard_db_user:mongo001@cluster-ufs.5fzp98n.mongodb.net/universidade?appName=Cluster-UFS"

    client = MongoClient(string_conexao)
    db = client['universidade']
    
    print("Limpando banco de dados para evitar duplicidade...")
    colecoes = ['departamento', 'usuario', 'professor', 'curso', 'estudante', 'disciplina', 'turma', 'projeto', 'plano', 'semestre']
    for col in colecoes:
        db[col].delete_many({})

    # ========================================================
    # EXTRAÇÃO (DADOS BRUTOS TRADUZIDOS DO SQL)
    # ========================================================
    
    # --- DEPARTAMENTOS (Já com os chefes atualizados pelo UPDATE do SQL) ---
    departamentos = [
        {"cod_depto": "DCOMP", "nome": "Departamento de Computação", "chefe": "P100", "orcamento": 10000.0, "comissal": 1000.0},
        {"cod_depto": "DCOM2", "nome": "Departamento de Computação", "chefe": None, "orcamento": 5000.0, "comissal": 0.0},
        {"cod_depto": "DMA", "nome": "Departamento de Matemática", "chefe": "P600", "orcamento": 20000.0, "comissal": 1000.0},
        {"cod_depto": "DFI", "nome": "Departamento de Física", "chefe": "P1400", "orcamento": 50000.0, "comissal": 1000.0},
        {"cod_depto": "DECAT", "nome": "Departamento de Estatística e Ciências Atuarias", "chefe": "P1100", "orcamento": 10000.0, "comissal": 1000.0},
        {"cod_depto": "DEL", "nome": "Departamento de Engenharia Elétrica", "chefe": None, "orcamento": None, "comissal": 0.0}
    ]

    # --- USUÁRIOS (Professores + Estudantes) ---
    usuarios = [
        {"cpf": 11111111100, "nome": "Prof A", "data_nascimento": "1980-03-05", "email": ["profA@email.com"], "telefone": ["99998888","88889999"], "login": "profa", "senha": "senha1"},
        {"cpf": 11111111101, "nome": "Prof B", "data_nascimento": "1980-07-23", "email": ["profB@email.com", "pB@mail.com"], "telefone": [], "login": "profb", "senha": "senha2"},
        {"cpf": 11111111102, "nome": "Prof C", "data_nascimento": "1987-05-12", "email": ["profc@email.com"], "telefone": ["99998885","84389999"], "login": "profc", "senha": "senha3"},
        {"cpf": 11111111103, "nome": "Prof D", "data_nascimento": "1975-01-22", "email": [], "telefone": [], "login": "profd", "senha": "senha4"},
        {"cpf": 11111111104, "nome": "Prof E", "data_nascimento": "1980-04-25", "email": ["profE@email.com"], "telefone": ["99298888","88889999"], "login": "profe", "senha": "senha5"},
        {"cpf": 11111111105, "nome": "Prof F", "data_nascimento": "1960-03-05", "email": ["profF@email.com"], "telefone": ["89998888","98889999"], "login": "proff", "senha": "senha6"},
        {"cpf": 11111111106, "nome": "Prof G", "data_nascimento": "1981-03-05", "email": ["profG@email.com"], "telefone": ["99978888","86889999"], "login": "profg", "senha": "senha7"},
        {"cpf": 11111111107, "nome": "Prof H", "data_nascimento": "1972-08-03", "email": ["profh@email.com"], "telefone": ["90998888","88889999"], "login": "profh", "senha": "senha8"},
        {"cpf": 11111111108, "nome": "Prof A", "data_nascimento": "1986-04-01", "email": ["profA2@email.com"], "telefone": ["90998088","81889999"], "login": "profam", "senha": "senha9"},
        {"cpf": 11111111109, "nome": "Prof I", "data_nascimento": "1980-03-05", "email": ["profI@email.com"], "telefone": [], "login": "profi", "senha": "sennha10"},
        {"cpf": 11111111110, "nome": "Prof F", "data_nascimento": "1981-09-05", "email": ["profFF@email.com"], "telefone": ["99668888","88329999"], "login": "proffd", "senha": "senha12"},
        {"cpf": 11111111111, "nome": "Prof K", "data_nascimento": "1980-03-04", "email": ["profK@email.com"], "telefone": ["79998888","97889999"], "login": "profk", "senha": "senha11"},
        {"cpf": 11111111112, "nome": "Prof I", "data_nascimento": "1980-03-05", "email": ["profI@email.com"], "telefone": ["93998888","92889999"], "login": "profim", "senha": "senha13"},
        {"cpf": 11111111113, "nome": "Prof G", "data_nascimento": "1954-06-15", "email": ["profGA@email.com"], "telefone": ["97698888","88129999"], "login": "profgf", "senha": "senha14"},
        {"cpf": 11111111114, "nome": "Prof P", "data_nascimento": "1989-11-05", "email": ["profP@email.com"], "telefone": ["99128888","88339999"], "login": "profp", "senha": "senha15"},
        {"cpf": 22222222201, "nome": "Steve Jobs", "data_nascimento": "1990-03-05", "email": ["steve@email.com","steve@apple.com"], "telefone": [], "login": "steve", "senha": "s1"},
        {"cpf": 22222222202, "nome": "Paul Bell", "data_nascimento": "1999-09-15", "email": ["bell@email.com"], "telefone": [], "login": "paul", "senha": "s2"},
        {"cpf": 22222222203, "nome": "Alan Turing", "data_nascimento": "1912-07-23", "email": [], "telefone": [], "login": "alan", "senha": "s3"},
        {"cpf": 22222222204, "nome": "John Hopcroft", "data_nascimento": "1939-10-07", "email": ["hopcroft@lfc.com"], "telefone": [], "login": "john", "senha": "s4"},
        {"cpf": 22222222205, "nome": "Ada Lovelace", "data_nascimento": "1985-11-27", "email": [], "telefone": [], "login": "ada", "senha": "s5"},
        {"cpf": 22222222206, "nome": "Grace Hooper", "data_nascimento": "1996-12-10", "email": ["hooper@linguagens.com"], "telefone": [], "login": "grace", "senha": "s5"},
        {"cpf": 22222222207, "nome": "Charles Babbage", "data_nascimento": "1971-12-26", "email": [], "telefone": [], "login": "charles", "senha": "s6"},
        {"cpf": 22222222208, "nome": "Musa al-Khwarizmi", "data_nascimento": "1950-12-26", "email": [], "telefone": [], "login": "musa", "senha": "s7"},
        {"cpf": 22222222209, "nome": "Cesar Lattes", "data_nascimento": "1924-06-11", "email": ["cesar@cnpq.com", "lattes@curriculo.com"], "telefone": [], "login": "lattes", "senha": "s8"},
        {"cpf": 22222222210, "nome": "Donald Knuth", "data_nascimento": "1938-01-10", "email": ["knuth@algorithms.com"], "telefone": [], "login": "knuth", "senha": "s9"},
        {"cpf": 22222222211, "nome": "Abraham Silberschatz", "data_nascimento": "1956-01-10", "email": ["silberchatz@sgbd.com"], "telefone": [], "login": "abraham", "senha": "s10"},
        {"cpf": 22222222212, "nome": "Elmasri Navathe", "data_nascimento": "1944-03-24", "email": [], "telefone": [], "login": "elmasri", "senha": "s11"},
        {"cpf": 22222222213, "nome": "Ramakrishnam Raghu", "data_nascimento": "1965-08-22", "email": [], "telefone": [], "login": "raghu", "senha": "s12"}
    ]

    # --- PROFESSORES ---
    professores = [
        {"mat_professor": "P100", "cpf": 11111111100, "departamento": "DCOMP", "formacao": "Doutorado", "data_admissao": None, "tipo_jornada_trabalho": "20h", "salario": 2000.0},
        {"mat_professor": "P200", "cpf": 11111111101, "departamento": "DCOMP", "formacao": "Doutorado", "data_admissao": None, "tipo_jornada_trabalho": "20h", "salario": 2000.0},
        {"mat_professor": "P300", "cpf": 11111111102, "departamento": "DCOMP", "formacao": "Doutorado", "data_admissao": None, "tipo_jornada_trabalho": "40h", "salario": 4000.0},
        {"mat_professor": "P400", "cpf": 11111111103, "departamento": "DCOMP", "formacao": "Mestrado", "data_admissao": None, "tipo_jornada_trabalho": "20h", "salario": 2000.0},
        {"mat_professor": "P500", "cpf": 11111111104, "departamento": "DCOMP", "formacao": "Mestrado", "data_admissao": None, "tipo_jornada_trabalho": "40h", "salario": 4000.0},
        {"mat_professor": "P600", "cpf": 11111111105, "departamento": "DMA", "formacao": "Especialização", "data_admissao": None, "tipo_jornada_trabalho": "20h", "salario": 1500.0},
        {"mat_professor": "P700", "cpf": 11111111106, "departamento": "DFI", "formacao": "Mestrado", "data_admissao": None, "tipo_jornada_trabalho": "40h", "salario": 4000.0},
        {"mat_professor": "P800", "cpf": 11111111107, "departamento": "DCOMP", "formacao": "Mestrado", "data_admissao": None, "tipo_jornada_trabalho": "40h", "salario": 2000.0},
        {"mat_professor": "P900", "cpf": 11111111108, "departamento": "DCOMP", "formacao": "Mestrado", "data_admissao": None, "tipo_jornada_trabalho": "DE", "salario": 2000.0},
        {"mat_professor": "P1000", "cpf": 11111111109, "departamento": "DCOMP", "formacao": "Doutorado", "data_admissao": None, "tipo_jornada_trabalho": "DE", "salario": 6000.0},
        {"mat_professor": "P1100", "cpf": 11111111110, "departamento": "DECAT", "formacao": "Graduação", "data_admissao": None, "tipo_jornada_trabalho": "20h", "salario": 1000.0},
        {"mat_professor": "P1200", "cpf": 11111111111, "departamento": "DMA", "formacao": "Mestrado", "data_admissao": None, "tipo_jornada_trabalho": "20h", "salario": 2000.0},
        {"mat_professor": "P1300", "cpf": 11111111112, "departamento": "DMA", "formacao": "Doutorado", "data_admissao": None, "tipo_jornada_trabalho": "20h", "salario": 2500.0},
        {"mat_professor": "P1400", "cpf": 11111111113, "departamento": "DFI", "formacao": "Doutorado", "data_admissao": None, "tipo_jornada_trabalho": "40h", "salario": 4000.0},
        {"mat_professor": "P1500", "cpf": 11111111114, "departamento": "DCOM2", "formacao": "Doutorado", "data_admissao": None, "tipo_jornada_trabalho": "DE", "salario": 6000.0}
    ]

    # --- CURSOS ---
    cursos = [
        {"idCurso": 1, "nome": "Ciência da Computação", "grau": "Bacharelado", "turno": "Vespertino", "campus": "São Cristóvão", "nivel": "Graduação"},
        {"idCurso": 2, "nome": "Sistemas de Informação", "grau": "Bacharelado", "turno": "Noturno", "campus": "São Cristóvão", "nivel": "Graduação"},
        {"idCurso": 3, "nome": "Sistemas de Informação", "grau": "Bacharelado", "turno": "Matutino", "campus": "Itabaiana", "nivel": "Graduação"},
        {"idCurso": 4, "nome": "Engenharia de Computação", "grau": "Bacharelado", "turno": "Vespertino", "campus": "São Cristóvão", "nivel": "Graduação"},
        {"idCurso": 5, "nome": "Inteligência Artificial", "grau": "Bacharelado", "turno": "Vespertino", "campus": "São Cristóvão", "nivel": "Graduação"}
    ]

    # --- DISCIPLINAS ---
    disciplinas = [
        {"cod_disc": "COMP0196", "nome": "Fundamentos da Computação", "pre_req": None, "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0197", "nome": "Programação Imperativa", "pre_req": None, "creditos": 6, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0198", "nome": "Programação Orientada à Objetos", "pre_req": "COMP0197", "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0199", "nome": "Programação Declarativa", "pre_req": "COMP0197", "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0212", "nome": "Estrutura de Dados I", "pre_req": "COMP0197", "creditos": 6, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0213", "nome": "Estrutura de Dados II", "pre_req": "COMP0212", "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0222", "nome": "Inteligência Artificial", "pre_req": "COMP0199", "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0233", "nome": "Lógica para Computação", "pre_req": None, "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0279", "nome": "Desenvolvimento de Software I", "pre_req": "COMP0197", "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0280", "nome": "Desenvolvimento de Software II", "pre_req": "COMP0279", "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0281", "nome": "Desenvolvimento de Software III", "pre_req": "COMP0280", "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0298", "nome": "Redes de Computadores", "pre_req": None, "creditos": 4, "depto_responsavel": None},
        {"cod_disc": "COMP0311", "nome": "Banco de dados", "pre_req": "COMP0213", "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "COMP0326", "nome": "Sistemas Distribuídos", "pre_req": "COMP0298", "creditos": 4, "depto_responsavel": "DCOMP"},
        {"cod_disc": "MAT0064", "nome": "Cálculo I", "pre_req": None, "creditos": 6, "depto_responsavel": "DMA"},
        {"cod_disc": "MAT0065", "nome": "Cálculo II", "pre_req": None, "creditos": 6, "depto_responsavel": "DMA"},
        {"cod_disc": "MAT0096", "nome": "Cálculo Numérico", "pre_req": None, "creditos": 4, "depto_responsavel": "DMA"},
        {"cod_disc": "FISI0050", "nome": "Física A", "pre_req": None, "creditos": 4, "depto_responsavel": "DFI"},
        {"cod_disc": "FISI0051", "nome": "Física B", "pre_req": "FISI0050", "creditos": 4, "depto_responsavel": "DFI"}
    ]

    # --- SEMESTRES ---
    semestres = [
        {"ano": 2017, "semestre": 2, "data_inicio": None, "data_fim": None},
        {"ano": 2019, "semestre": 1, "data_inicio": None, "data_fim": None}
    ]

    # --- PROJETOS & PLANOS ---
    projetos = [
        {"id_projeto": 1, "descricao": "Projeto 1"}, {"id_projeto": 2, "descricao": "Projeto 2"},
        {"id_projeto": 3, "descricao": "Projeto 3"}, {"id_projeto": 4, "descricao": "Projeto 4"},
        {"id_projeto": 5, "descricao": "Projeto 5"}
    ]
    planos = [
        {"id_projeto": 1, "mat_professor": "P100", "mat_estudante": "E103", "ano": 2018},
        {"id_projeto": 2, "mat_professor": "P200", "mat_estudante": "E105", "ano": 2018},
        {"id_projeto": 3, "mat_professor": "P300", "mat_estudante": "E106", "ano": 2018},
        {"id_projeto": 4, "mat_professor": "P500", "mat_estudante": "E107", "ano": 2018},
        {"id_projeto": 5, "mat_professor": "P600", "mat_estudante": "E108", "ano": 2018},
        {"id_projeto": 1, "mat_professor": "P100", "mat_estudante": "E109", "ano": 2018}
    ]

    # ========================================================
    # TRANSFORM (A MÁGICA DO NOSQL: EMBUTINDO DADOS)
    # ========================================================
    
    # --- TURMAS + LECIONA (Professores embutidos na turma) ---
    turmas = [
        {"id_turma": 1, "cod_disc": "COMP0212", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P100"], "alocacoes_agenda": []},
        {"id_turma": 2, "cod_disc": "COMP0213", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P100"], "alocacoes_agenda": []},
        {"id_turma": 3, "cod_disc": "COMP0311", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P100"], "alocacoes_agenda": []},
        {"id_turma": 4, "cod_disc": "COMP0198", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P200"], "alocacoes_agenda": []},
        {"id_turma": 5, "cod_disc": "COMP0199", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P200"], "alocacoes_agenda": []},
        {"id_turma": 6, "cod_disc": "COMP0233", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P300"], "alocacoes_agenda": []},
        {"id_turma": 7, "cod_disc": "COMP0196", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P300"], "alocacoes_agenda": []},
        {"id_turma": 8, "cod_disc": "COMP0197", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P300"], "alocacoes_agenda": []},
        {"id_turma": 9, "cod_disc": "COMP0279", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P400"], "alocacoes_agenda": []},
        {"id_turma": 10, "cod_disc": "COMP0280", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P400"], "alocacoes_agenda": []},
        {"id_turma": 11, "cod_disc": "COMP0281", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P400"], "alocacoes_agenda": []},
        {"id_turma": 12, "cod_disc": "COMP0298", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P500"], "alocacoes_agenda": []},
        {"id_turma": 13, "cod_disc": "COMP0326", "numero": 2, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P500"], "alocacoes_agenda": []},
        {"id_turma": 14, "cod_disc": "MAT0096", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P600"], "alocacoes_agenda": []},
        {"id_turma": 15, "cod_disc": "MAT0064", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P600"], "alocacoes_agenda": []},
        {"id_turma": 16, "cod_disc": "MAT0096", "numero": 2, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P900"], "alocacoes_agenda": []},
        {"id_turma": 17, "cod_disc": "MAT0096", "numero": 3, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P1300"], "alocacoes_agenda": []},
        {"id_turma": 18, "cod_disc": "MAT0065", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P1200"], "alocacoes_agenda": []},
        {"id_turma": 19, "cod_disc": "FISI0050", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P700"], "alocacoes_agenda": []},
        {"id_turma": 20, "cod_disc": "COMP0199", "numero": 2, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P1500"], "alocacoes_agenda": []},
        {"id_turma": 21, "cod_disc": "COMP0233", "numero": 2, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P1500"], "alocacoes_agenda": []},
        {"id_turma": 22, "cod_disc": "COMP0222", "numero": 1, "ano": 2017, "semestre": 2, "professores_ministrantes": ["P100"], "alocacoes_agenda": []},
        {"id_turma": 23, "cod_disc": "MAT0065", "numero": 1, "ano": 2019, "semestre": 1, "professores_ministrantes": [], "alocacoes_agenda": []},
        {"id_turma": 24, "cod_disc": "FISI0050", "numero": 1, "ano": 2019, "semestre": 1, "professores_ministrantes": [], "alocacoes_agenda": []},
        {"id_turma": 25, "cod_disc": "COMP0199", "numero": 2, "ano": 2019, "semestre": 1, "professores_ministrantes": [], "alocacoes_agenda": []},
        {"id_turma": 26, "cod_disc": "COMP0233", "numero": 2, "ano": 2019, "semestre": 1, "professores_ministrantes": [], "alocacoes_agenda": []},
        {"id_turma": 27, "cod_disc": "COMP0222", "numero": 1, "ano": 2019, "semestre": 1, "professores_ministrantes": [], "alocacoes_agenda": []}
    ]

    # --- ESTUDANTES BASE ---
    estudantes = [
        {"matEstudante": "E101", "cpf": 22222222201, "mc": 7.0, "anoIngresso": 2021, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E102", "cpf": 22222222202, "mc": 8.3, "anoIngresso": 2021, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E103", "cpf": 22222222203, "mc": 6.7, "anoIngresso": 2021, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E104", "cpf": 22222222204, "mc": 0.0, "anoIngresso": 2021, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E105", "cpf": 22222222205, "mc": 9.0, "anoIngresso": 2022, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E106", "cpf": 22222222206, "mc": 7.7, "anoIngresso": 2022, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E107", "cpf": 22222222207, "mc": 5.5, "anoIngresso": 2022, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E108", "cpf": 22222222208, "mc": 6.5, "anoIngresso": 2023, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E109", "cpf": 22222222209, "mc": 6.0, "anoIngresso": 2023, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E110", "cpf": 22222222210, "mc": 2.1, "anoIngresso": 2023, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E111", "cpf": 22222222211, "mc": 3.3, "anoIngresso": 2023, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E112", "cpf": 22222222212, "mc": 4.5, "anoIngresso": 2024, "vinculos": [], "historico_escolar": []},
        {"matEstudante": "E113", "cpf": 22222222213, "mc": 8.1, "anoIngresso": 2024, "vinculos": [], "historico_escolar": []}
    ]

    # --- FUNDINDO OS VÍNCULOS NOS ESTUDANTES ---
    vinculos_brutos = [
        ("E101", 3), ("E102", 2), ("E103", 1), ("E104", 4), ("E105", 1),
        ("E106", 1), ("E107", 1), ("E108", 5), ("E109", 1), ("E110", 5),
        ("E111", 4), ("E112", 2), ("E113", 2)
    ]
    
    # O Python mapeia o aluno pelo ID e injeta o dicionário dentro da lista "vinculos" dele
    estudantes_map = {e['matEstudante']: e for e in estudantes}
    for mat, curso in vinculos_brutos:
        estudantes_map[mat]['vinculos'].append({"curso": curso, "data_entrada": None, "status": "Ativo", "data_saida": None})

    # --- FUNDINDO AS NOTAS (CURSA) NOS ESTUDANTES ---
    cursa_bruto = [
        ("E112", 7, 4.1), ("E102", 7, 10.0), ("E104", 7, 7.0), ("E109", 7, 8.0),
        ("E112", 8, 5.5), ("E102", 8, 10.0), ("E107", 8, 9.0), ("E108", 8, 8.5), ("E109", 8, 10.0),
        ("E104", 5, 8.7), ("E109", 5, None), ("E110", 20, 5.5), ("E111", 20, 10.0),
        ("E101", 2, 10.0), ("E107", 2, 10.0), ("E106", 2, 10.0), ("E104", 2, 10.0), ("E105", 2, 10.0),
        ("E101", 22, None), ("E111", 22, None), ("E106", 22, 9.5), ("E108", 22, 9.5), ("E109", 22, 9.5), ("E110", 22, 8.1),
        ("E112", 6, None), ("E102", 6, None), ("E104", 6, None), ("E106", 6, None), ("E107", 6, None),
        ("E108", 21, None), ("E109", 21, None), ("E111", 21, None),
        ("E106", 9, None), ("E110", 9, None), ("E111", 9, None), ("E108", 9, None),
        ("E108", 11, None), ("E107", 11, None), ("E110", 11, None),
        ("E101", 12, 9.5), ("E111", 12, 7.6), ("E110", 12, 7.7),
        ("E106", 3, 9.0), ("E110", 3, None), ("E101", 3, 7.0), ("E102", 3, 2.5), ("E107", 3, 3.2),
        ("E101", 13, 8.0), ("E111", 13, 8.0), ("E109", 13, 4.0),
        ("E101", 15, 4.0), ("E111", 15, 3.5), ("E107", 15, 2.0), ("E102", 15, 8.0), ("E112", 15, 6.0),
        ("E106", 18, 6.0), ("E111", 18, 7.5), ("E109", 18, 6.0), ("E110", 18, 9.0),
        ("E102", 14, 7.5), ("E104", 14, 6.0), ("E106", 16, 10.0), ("E107", 16, 0.0), ("E108", 16, 9.0), ("E110", 17, 8.5),
        ("E101", 23, 8.0), ("E105", 23, 8.0), ("E109", 23, 4.0),
        ("E101", 24, 4.0), ("E110", 24, 3.5), ("E107", 24, 2.0), ("E102", 24, 8.0), ("E111", 24, 6.0),
        ("E106", 25, 6.0), ("E111", 25, 7.5), ("E109", 25, 6.0), ("E112", 25, 9.0)
    ]
    for mat, id_turma, nota in cursa_bruto:
        estudantes_map[mat]['historico_escolar'].append({"id_turma": id_turma, "nota": nota})

    # ========================================================
    # LOAD (CARGA DOS DADOS NO MONGODB)
    # ========================================================
    print("Inserindo dados mapeados...")
    
    if departamentos: db['departamento'].insert_many(departamentos)
    if usuarios: db['usuario'].insert_many(usuarios)
    if professores: db['professor'].insert_many(professores)
    if cursos: db['curso'].insert_many(cursos)
    if disciplinas: db['disciplina'].insert_many(disciplinas)
    if semestres: db['semestre'].insert_many(semestres)
    if projetos: db['projeto'].insert_many(projetos)
    if planos: db['plano'].insert_many(planos)
    if turmas: db['turma'].insert_many(turmas)
    if estudantes: db['estudante'].insert_many(list(estudantes_map.values()))

    print("BASE DE DADOS POVOADA E TRADUZIDA COM SUCESSO!")
    client.close()

if __name__ == "__main__":
    popular_banco_completo()