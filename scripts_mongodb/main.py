from pymongo import MongoClient
from pymongo.errors import OperationFailure

# Importa os esquemas de validação
import scripts_mongodb.esquemas as esquemas

# Importa as classes de CRUD
from scripts_mongodb.estudante_crud import EstudanteCRUD
from scripts_mongodb.curso_crud import CursoCRUD
from scripts_mongodb.usuario_crud import UsuarioCRUD

def conectar_banco():
    """ Estabelece a conexão com o MongoDB Atlas """
    string_conexao = "mongodb+srv://Maard_db_user:mongo001@cluster-ufs.5fzp98n.mongodb.net/universidade?appName=Cluster-UFS"
    
    try:
        client = MongoClient(string_conexao)
        db = client['universidade']
        client.admin.command('ping')
        return db
    except Exception as e:
        print(f"Falha ao conectar ao banco de dados: {e}")
        return None

def aplicar_validacoes_esquema(db):
    """ Aplica as regras estruturais (NOT NULL, ENUM, Tipos) nas coleções existentes """
    colecoes_esquemas = {
        "usuario": esquemas.esquema_usuario,
        "curso": esquemas.esquema_curso,
        "estudante": esquemas.esquema_estudante,
        "professor": esquemas.esquema_professor,
        "departamento": esquemas.esquema_departamento,
        "disciplina": esquemas.esquema_disciplina,
        "turma": esquemas.esquema_turma,
        "projeto": esquemas.esquema_projeto,
        "plano": esquemas.esquema_plano,
        "semestre": esquemas.esquema_semestre
    }

    print("\nAplicando regras de integridade e validação no banco de dados...")
    for nome_colecao, esquema in colecoes_esquemas.items():
        try:
            db.command(
                "collMod", 
                nome_colecao, 
                validator=esquema, 
                validationLevel="strict"
            )
            print(f"  Schema aplicado com sucesso na coleção: {nome_colecao}")
        except OperationFailure as e:
            print(f"  Erro ao aplicar schema em '{nome_colecao}': {e.details.get('errmsg', e)}")


# ========================================================
# SUBMENU: ESTUDANTES
# ========================================================
def menu_estudantes(manager: EstudanteCRUD):
    while True:
        print("\n" + "="*35)
        print("GERENCIAR ESTUDANTES E VÍNCULOS")
        print("="*35)
        print("1. Criar novo Estudante")
        print("2. Criar vários Estudantes (Lote)")
        print("3. Buscar Estudante por Matrícula")
        print("4. Atualizar Dados do Estudante")
        print("5. Deletar Estudante")
        print("6. [Vínculo] Adicionar Curso ao Aluno")
        print("7. [Vínculo] Alterar Status do Curso")
        print("8. [Vínculo] Remover Curso do Aluno")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            mat = input("Matrícula (ex: E999): ")
            cpf = int(input("CPF do Usuário (apenas números): "))
            mc = float(input("Média Curricular (MC): "))
            ano = int(input("Ano de Ingresso: "))
            
            manager.criar({
                "matEstudante": mat, "cpf": cpf, "mc": mc, 
                "anoIngresso": ano, "vinculos": [], "historico_escolar": []
            })

        elif opcao == '2':
            print("--- Cadastro em Lote (Simulação de 2 itens) ---")
            lista = []
            for i in range(2):
                print(f"\nEstudante #{i+1}:")
                mat = input("Matrícula: ")
                cpf = int(input("CPF: "))
                mc = float(input("MC: "))
                ano = int(input("Ano Ingresso: "))
                lista.append({"matEstudante": mat, "cpf": cpf, "mc": mc, "anoIngresso": ano})
            manager.criar_varios(lista)

        elif opcao == '3':
            mat = input("Digite a matrícula para busca: ")
            aluno = manager.ler_um({"matEstudante": mat})
            if aluno:
                print("\n" + "="*40)
                print(f"DOSSIÊ DO ALUNO: {aluno.get('matEstudante')}")
                print("="*40)
                print(f"CPF: {str(aluno.get('cpf')).zfill(11)} | MC: {aluno.get('mc')}")
                print(f"Ano de Ingresso: {aluno.get('anoIngresso')}")
                
                # Percorre e mostra os detalhes de cada vínculo encontrado
                print("\nVÍNCULOS ACADÊMICOS:")
                vinculos = aluno.get('vinculos', [])
                if not vinculos:
                    print("  - Nenhum vínculo registrado.")
                for v in vinculos:
                    print(f"  -> Curso ID: {v.get('curso')} | Status: {v.get('status')}")
                
                # Aproveita para mostrar também o histórico de notas embutido
                print("\nHISTÓRICO DE NOTAS (CURSA):")
                historico = aluno.get('historico_escolar', [])
                if not historico:
                    print("  - Nenhuma nota registrada.")
                for h in historico:
                    nota_formatada = h.get('nota') if h.get('nota') is not None else "Sem Nota"
                    print(f"  -> Turma ID: {h.get('id_turma')} | Nota: {nota_formatada}")
                print("="*40)
            else:
                print("Aluno não encontrado.")

        elif opcao == '4':
            mat = input("Matrícula do estudante que deseja alterar: ")
            print("Deixe em branco os campos que NÃO deseja alterar.")
            novo_mc = input("Nova Média Curricular (MC): ")
            novo_ano = input("Novo Ano de Ingresso: ")
            
            dados_novos = {}
            if novo_mc: dados_novos["mc"] = float(novo_mc)
            if novo_ano: dados_novos["anoIngresso"] = int(novo_ano)
            
            if dados_novos:
                manager.atualizar({"matEstudante": mat}, dados_novos)
            else:
                print("Nenhuma alteração informada.")

        elif opcao == '5':
            mat = input("Matrícula do Estudante para deletar: ")
            manager.deletar({"matEstudante": mat})

        elif opcao == '6':
            mat = input("Matrícula do Estudante: ")
            id_curso = int(input("ID do Curso para vincular: "))
            status = input("Status (Ativo, Cancelada, Formando, Graduado): ")
            manager.adicionar_vinculo(mat, {"curso": id_curso, "data_entrada": None, "status": status, "data_saida": None})

        elif opcao == '7':
            mat = input("Matrícula do Estudante: ")
            id_curso = int(input("ID do Curso: "))
            status = input("Novo Status (Ativo, Cancelada, Formando, Graduado): ")
            manager.atualizar_status_vinculo(mat, id_curso, status)

        elif opcao == '8':
            mat = input("Matrícula do Estudante: ")
            id_curso = int(input("ID do Curso para desvincular: "))
            manager.remover_vinculo(mat, id_curso)

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")


# ========================================================
# SUBMENU: USUÁRIOS
# ========================================================
def menu_usuarios(manager: UsuarioCRUD):
    while True:
        print("\n" + "="*35)
        print("GERENCIAR USUÁRIOS DO SISTEMA")
        print("="*35)
        print("1. Criar novo Usuário")
        print("2. Buscar Usuário por CPF")
        print("3. Atualizar Dados do Usuário")
        print("4. Deletar Usuário (Simula ON DELETE SET NULL)")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            cpf = int(input("CPF (Apenas números): "))
            nome = input("Nome Completo: ")
            login = input("Login de Acesso: ")
            senha = input("Senha: ")
            
            manager.criar({
                "cpf": cpf, "nome": nome, "login": login, "senha": senha,
                "data_nascimento": None, "email": [], "telefone": []
            })

        elif opcao == '2':
            cpf = int(input("Digite o CPF para busca: "))
            usr = manager.ler_um({"cpf": cpf})
            if usr:
                print(f"\nUsuário Encontrado: {usr.get('nome')} | Login: {usr.get('login')} | CPF: {usr.get('cpf')}")
            else:
                print("Usuário não encontrado.")

        elif opcao == '3':
            cpf = int(input("Digite o CPF do usuário a alterar: "))
            print("Deixe em branco os campos que NÃO deseja alterar.")
            nome = input("Novo Nome: ")
            login = input("Novo Login: ")
            
            dados_novos = {}
            if nome: dados_novos["nome"] = nome
            if login: dados_novos["login"] = login
            
            if dados_novos:
                manager.atualizar({"cpf": cpf}, dados_novos)
            else:
                print("Nenhuma alteração informada.")

        elif opcao == '4':
            cpf = int(input("Digite o CPF do usuário para remover: "))
            manager.deletar({"cpf": cpf})

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")


# ========================================================
# SUBMENU: CURSOS
# ========================================================
def menu_cursos(manager: CursoCRUD):
    while True:
        print("\n" + "="*35)
        print("GERENCIAR CURSOS DA UNIVERSIDADE")
        print("="*35)
        print("1. Criar novo Curso")
        print("2. Buscar Curso por ID")
        print("3. Atualizar Dados do Curso")
        print("4. Deletar Curso (Com trava de integridade)")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == '1':
            id_curso = int(input("ID do Curso (Inteiro único): "))
            nome = input("Nome do Curso: ")
            print("Turnos válidos: Matutino, Vespertino, Noturno, Turno Indefinido")
            turno = input("Turno: ")
            
            manager.criar({
                "idCurso": id_curso, "nome": nome, "turno": turno,
                "grau": "Bacharelado", "campus": "São Cristóvão", "nivel": "Graduação"
            })

        elif opcao == '2':
            id_curso = int(input("Digite o ID do Curso para busca: "))
            cur = manager.ler_um({"idCurso": id_curso})
            if cur:
                print(f"\nCurso Encontrado: {cur.get('nome')} | Turno: {cur.get('turno')} | ID: {cur.get('idCurso')}")
            else:
                print("Curso não encontrado.")

        elif opcao == '3':
            id_curso = int(input("ID do curso a alterar: "))
            print("Deixe em branco os campos que NÃO deseja alterar.")
            nome = input("Novo Nome do Curso: ")
            turno = input("Novo Turno: ")
            
            dados_novos = {}
            if nome: dados_novos["nome"] = nome
            if turno: dados_novos["turno"] = turno
            
            if dados_novos:
                manager.atualizar({"idCurso": id_curso}, dados_novos)
            else:
                print("Nenhuma alteração informada.")

        elif opcao == '4':
            id_curso = int(input("ID do curso para deletar: "))
            manager.deletar({"idCurso": id_curso})

        elif opcao == '0':
            break
        else:
            print("Opção inválida.")


# ========================================================
# FLUXO PRINCIPAL (MAIN)
# ========================================================
def main():
    print("Iniciando Sistema de Gestão Universitária (NoSQL)...")
    
    db = conectar_banco()
    if db is None:
        return

    # Passo 1: Blinda o banco de dados aplicando os schemas
    aplicar_validacoes_esquema(db)
    
    # Passo 2: Instancia os gerenciadores de CRUD
    estudante_manager = EstudanteCRUD(db)
    curso_manager = CursoCRUD(db)
    usuario_manager = UsuarioCRUD(db)

    # LOOP PRINCIPAL DO SISTEMA
    while True:
        print("\n" + "#"*35)
        print("SISTEMA UNIVERSITÁRIO NOSQL")
        print("#"*35)
        print("1. Gerenciar Estudantes e Vínculos")
        print("2. Gerenciar Usuários")
        print("3. Gerenciar Cursos")
        print("0. Sair do Sistema")
        
        escolha = input("\nDigite o número da operação desejada: ")

        if escolha == '1':
            menu_estudantes(estudante_manager)
        elif escolha == '2':
            menu_usuarios(usuario_manager)
        elif escolha == '3':
            menu_cursos(curso_manager)
        elif escolha == '0':
            print("\nDesconectando do banco... Sistema encerrado com sucesso. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()