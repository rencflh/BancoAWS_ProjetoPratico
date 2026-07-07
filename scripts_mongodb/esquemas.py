# VALIDAÇÃO DE TIPOS
# 1. ESQUEMA: USUÁRIO
# ========================================================
esquema_usuario = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["cpf", "nome", "login", "senha"],
        "properties": {
            "cpf": {"bsonType": "long", "description": "CPF - Chave Primária"},
            "nome": {"bsonType": "string", "maxLength": 100},
            "data_nascimento": {"bsonType": ["string", "date", "null"]},
            "email": {"bsonType": "array", "items": {"bsonType": "string"}},
            "telefone": {"bsonType": "array", "items": {"bsonType": "string"}},
            "login": {"bsonType": "string", "maxLength": 45},
            "senha": {"bsonType": "string", "maxLength": 32}
        }
    }
}

# ========================================================
# 2. ESQUEMA: CURSO
# ========================================================
esquema_curso = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["idCurso", "nome", "turno"],
        "properties": {
            "idCurso": {"bsonType": "int", "description": "ID do Curso - Chave Primária"},
            "nome": {"bsonType": "string", "maxLength": 100},
            "grau": {"bsonType": "string", "enum": ["Bacharelado", "Licenciatura Plena"]},
            "turno": {"bsonType": "string", "enum": ["Matutino", "Vespertino", "Noturno", "Turno Indefinido"]},
            "campus": {"bsonType": "string", "maxLength": 100},
            "nivel": {"bsonType": "string", "enum": ["Graduação", "Mestrado", "Doutorado", "Lato"]}
        }
    }
}

# ========================================================
# 3. ESQUEMA: ESTUDANTE (MODELO HÍBRIDO - EMBUTE VÍNCULO E CURSA)
# ========================================================
esquema_estudante = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["matEstudante", "anoIngresso"],
        "properties": {
            "matEstudante": {"bsonType": "string", "maxLength": 7, "description": "Chave Primária"},
            "cpf": {"bsonType": ["long", "null"]},
            "mc": {"bsonType": "double"},
            "anoIngresso": {"bsonType": "int"},
            
            # Tabela VINCULO embutida aqui (Relacionamento Estudante-Curso)
            "vinculos": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["curso", "status"],
                    "properties": {
                        "curso": {"bsonType": "int"},
                        "data_entrada": {"bsonType": ["string", "date", "null"]},
                        "status": {"bsonType": "string", "enum": ["Ativo", "Cancelada", "Formando", "Graduado"]},
                        "data_saida": {"bsonType": ["string", "date", "null"]}
                    }
                }
            },
            
            # Tabela CURSA embutida aqui (Histórico de Notas do Aluno nas Turmas)
            "historico_escolar": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["id_turma"],
                    "properties": {
                        "id_turma": {"bsonType": "int"},
                        "nota": {"bsonType": ["double", "int", "null"]}
                    }
                }
            }
        }
    }
}

# ========================================================
# 4. ESQUEMA: PROFESSOR
# ========================================================
esquema_professor = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["mat_professor", "cpf"],
        "properties": {
            "mat_professor": {"bsonType": "string", "maxLength": 7, "description": "Chave Primária"},
            "cpf": {"bsonType": ["long", "null"]},
            "departamento": {"bsonType": ["string", "null"], "maxLength": 5},
            "formacao": {"bsonType": "string", "enum": ["Graduação", "Especialização", "Mestrado", "Doutorado"]},
            "data_admissao": {"bsonType": ["string", "date", "null"]},
            "tipo_jornada_trabalho": {"bsonType": "string", "enum": ["20h", "40h", "DE"]},
            "salario": {"bsonType": ["double", "null"]}
        }
    }
}

# ========================================================
# 5. ESQUEMA: DEPARTAMENTO
# ========================================================
esquema_departamento = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["cod_depto", "nome"],
        "properties": {
            "cod_depto": {"bsonType": "string", "maxLength": 5, "description": "Chave Primária"},
            "nome": {"bsonType": "string", "maxLength": 50},
            "chefe": {"bsonType": ["string", "null"], "maxLength": 7},
            "orcamento": {
                "bsonType": ["double", "null"],
                "minimum": 0.01,
                "description": "Garante orçamento maior que zero"
            },
            "comissal": {"bsonType": ["double", "null"]}
        }
    }
}

# ========================================================
# 6. ESQUEMA: DISCIPLINA
# ========================================================
esquema_disciplina = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["cod_disc", "nome"],
        "properties": {
            "cod_disc": {"bsonType": "string", "maxLength": 8, "description": "Chave Primária"},
            "nome": {"bsonType": "string", "maxLength": 40},
            "pre_req": {"bsonType": ["string", "null"], "maxLength": 8},
            "creditos": {
                "bsonType": "int",
                "minimum": 1,
                "maximum": 11,
                "description": "Garante créditos entre 1 e 11"
            },
            "depto_responsavel": {"bsonType": ["string", "null"], "maxLength": 5}
        }
    }
}

# ========================================================
# 7. ESQUEMA: TURMA (MODELO HÍBRIDO)
# ========================================================
esquema_turma = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["id_turma", "cod_disc", "numero", "ano", "semestre"],
        "properties": {
            "id_turma": {"bsonType": "int", "description": "Chave Primária"},
            "cod_disc": {"bsonType": "string", "maxLength": 8},
            "numero": {"bsonType": "int"},
            "ano": {"bsonType": "int"},
            "semestre": {"bsonType": "int"},
            
            "professores_ministrantes": {
                "bsonType": "array",
                "items": {"bsonType": "string", "maxLength": 7}
            },
            
            "alocacoes_agenda": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["dia", "slot", "sala"],
                    "properties": {
                        "dia": {"bsonType": "string", "maxLength": 15},
                        "slot": {"bsonType": "int"},
                        "sala": {"bsonType": "string"}
                    }
                }
            }
        }
    }
}

# ========================================================
# 8. ESQUEMA: PROJETO
# ========================================================
esquema_projeto = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["id_projeto"],
        "properties": {
            "id_projeto": {"bsonType": "int", "description": "Chave Primária"},
            "descricao": {"bsonType": "string"}
        }
    }
}

# ========================================================
# 9. ESQUEMA: PLANO
# ========================================================
esquema_plano = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["id_projeto", "mat_professor", "mat_estudante", "ano"],
        "properties": {
            "id_projeto": {"bsonType": "int"},
            "mat_professor": {"bsonType": "string", "maxLength": 7},
            "mat_estudante": {"bsonType": "string", "maxLength": 7},
            "ano": {"bsonType": "int"}
        }
    }
}

# ========================================================
# 10. ESQUEMA: SEMESTRE
# ========================================================
esquema_semestre = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["ano", "semestre"],
        "properties": {
            "ano": {"bsonType": "int"},
            "semestre": {"bsonType": "int"},
            "data_inicio": {"bsonType": ["string", "date", "null"]},
            "data_fim": {"bsonType": ["string", "date", "null"]}
        }
    }
}