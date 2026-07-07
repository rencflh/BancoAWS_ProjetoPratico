from pymongo.errors import PyMongoError

class UsuarioCRUD:
    def __init__(self, database):
        # Recebe o banco de dados completo para gerenciar os vínculos relacionais
        self.db = database
        self.colecao = database['usuario']

    def criar(self, dados_usuario: dict):
        """ Create (C) - Insere um usuário garantindo a unicidade do CPF e do Login """
        cpf = dados_usuario.get("cpf")
        login = dados_usuario.get("login")

        # 1. VALIDAÇÃO DE CHAVE PRIMÁRIA (PK): Garante que o CPF não seja duplicado
        if self.colecao.find_one({"cpf": cpf}):
            print(f"ERRO: Já existe um usuário cadastrado com o CPF {cpf}.")
            return None

        # 2. VALIDAÇÃO DE RESTRIÇÃO UNIQUE: Garante que o login seja único
        if login and self.colecao.find_one({"login": login}):
            print(f"ERRO: O login '{login}' já está em uso por outro usuário.")
            return None

        try:
            resultado = self.colecao.insert_one(dados_usuario)
            print(f"Usuário '{dados_usuario.get('nome')}' inserido com sucesso!")
            return resultado.inserted_id
        except PyMongoError as e:
            print(f"Erro ao inserir usuário: {e}")
            return None

    def criar_varios(self, lista_de_usuarios: list):
        """ Create Many (C) - Insere vários usuários filtrando duplicatas """
        usuarios_validos = []
        
        for usu in lista_de_usuarios:
            cpf = usu.get("cpf")
            login = usu.get("login")
            
            if self.colecao.find_one({"cpf": cpf}) or (login and self.colecao.find_one({"login": login})):
                print(f"Usuário CPF {cpf} / Login '{login}' ignorado: CPF ou Login já cadastrados.")
            else:
                usuarios_validos.append(usu)

        if usuarios_validos:
            try:
                resultado = self.colecao.insert_many(usuarios_validos)
                print(f"{len(resultado.inserted_ids)} usuários inseridos em lote com sucesso!")
                return resultado.inserted_ids
            except PyMongoError as e:
                print(f"Erro ao inserir lote de usuários: {e}")
        return []

    def ler_um(self, filtro: dict):
        """ Read (R) - Busca um usuário específico """
        try:
            return self.colecao.find_one(filtro)
        except PyMongoError as e:
            print(f"Erro ao buscar usuário: {e}")
            return None

    def ler_varios(self, filtro: dict = {}):
        """ Read (R) - Busca múltiplos usuários """
        try:
            return list(self.colecao.find(filtro))
        except PyMongoError as e:
            print(f"Erro ao buscar usuários: {e}")
            return []

    def atualizar(self, filtro: dict, novos_dados: dict):
        """ Update (U) - Atualiza dados do usuário protegendo CPF e Login único """
        
        # 1. PROTEÇÃO DE CHAVE PRIMÁRIA (PK): O CPF não pode ser alterado via update direto
        if "cpf" in novos_dados:
            print("Aviso: O CPF (Chave Primária) não pode ser alterado diretamente. Ignorando este campo.")
            del novos_dados["cpf"]

        # 2. PROTEÇÃO DE RESTRIÇÃO UNIQUE: Se alterar o login, checa se o novo está disponível
        if "login" in novos_dados:
            novo_login = novos_dados["login"]
            usuario_com_login = self.colecao.find_one({"login": novo_login})
            if usuario_com_login and usuario_com_login.get("cpf") != filtro.get("cpf"):
                print(f"ERRO: O login '{novo_login}' já está em uso por outro usuário. Atualização cancelada.")
                return 0

        try:
            resultado = self.colecao.update_one(filtro, {"$set": novos_dados})
            if resultado.modified_count > 0:
                print("Dados do usuário atualizados com sucesso!")
            else:
                print("Nenhum dado foi modificado (os dados já eram idênticos).")
            return resultado.modified_count
        except PyMongoError as e:
            print(f"Erro ao atualizar usuário: {e}")
            return 0

    def deletar(self, filtro: dict):
        """ Delete (D) - Remove o usuário e simula a restrição ON DELETE SET NULL """
        
        # 1. Localiza o usuário para descobrir o CPF real dele
        usuario = self.ler_um(filtro)
        if not usuario:
            print("Nenhum usuário encontrado para remover.")
            return 0

        cpf_usuario = usuario.get("cpf")

        try:
            # 2. SIMULAÇÃO DO 'ON DELETE SET NULL' DO SQL:
            # Procuramos na coleção de estudantes se existe alguém usando este CPF.
            # Se sim, desvinculamos o CPF definindo-o como None, preservando o histórico do aluno.
            db_estudante = self.db['estudante']
            estudante_relacionado = db_estudante.find_one({"cpf": cpf_usuario})
            
            if estudante_relacionado:
                db_estudante.update_one({"cpf": cpf_usuario}, {"$set": {"cpf": None}})
                print(f"Integridade Referencial: O estudante de matrícula {estudante_relacionado.get('matEstudante')} "
                      f"teve seu CPF desvinculado (Set Null) devido à remoção do usuário.")

            # Repetimos a mesma lógica preventiva para a tabela de professores cadastrada na carga inicial
            db_professor = self.db['professor']
            if db_professor.find_one({"cpf": cpf_usuario}):
                db_professor.update_one({"cpf": cpf_usuario}, {"$set": {"cpf": None}})
                print("Integridade Referencial: Professor correspondente teve seu CPF definido como nulo.")

            # 3. Agora que os dados dependentes estão protegidos, removemos o usuário com segurança
            resultado = self.colecao.delete_one({"cpf": cpf_usuario})
            if resultado.deleted_count > 0:
                print("Usuário removido do sistema com sucesso!")
            return resultado.deleted_count

        except PyMongoError as e:
            print(f"Erro ao deletar usuário: {e}")
            return 0