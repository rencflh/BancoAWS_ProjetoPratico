from pymongo.errors import PyMongoError

class EstudanteCRUD:
    def __init__(self, database):
        # Recebe o banco inteiro para poder checar chaves em outras coleções
        self.db = database 
        self.colecao = database['estudante']

    # ==========================================
    # CRUD DO ESTUDANTE (DOCUMENTO PRINCIPAL)
    # ==========================================

    def criar(self, dados_estudante: dict):
        """ Create (C) - Estudante com validação de Chave Estrangeira (Usuário) """
        cpf_aluno = dados_estudante.get("cpf")

        # Verifica se o CPF existe na coleção de Usuários
        usuario_existe = self.db['usuario'].find_one({"cpf": cpf_aluno})
        
        if not usuario_existe:
            print(f"❌ ERRO: O CPF {cpf_aluno} não está cadastrado em Usuários. Inserção cancelada.")
            return None

        # Garante que a lista de vínculos nasça vazia se não for passada
        if "vinculos" not in dados_estudante:
            dados_estudante["vinculos"] = []

        try:
            resultado = self.colecao.insert_one(dados_estudante)
            print(f"✅ Estudante inserido com sucesso! Matrícula: {dados_estudante.get('matEstudante')}")
            return resultado.inserted_id
        except PyMongoError as e:
            print(f"❌ Erro ao inserir estudante: {e}")
            return None

    def criar_varios(self, lista_de_estudantes: list):
        """ Create Many (C) - Com filtro de Integridade Referencial em lote """
        estudantes_validos = []
        
        for est in lista_de_estudantes:
            cpf_aluno = est.get("cpf")
            if self.db['usuario'].find_one({"cpf": cpf_aluno}):
                # Garante que o array de vínculos nasça vazio se não existir
                if "vinculos" not in est:
                    est["vinculos"] = []
                estudantes_validos.append(est)
            else:
                print(f"⚠️ Estudante matrícula {est.get('matEstudante')} ignorado: CPF {cpf_aluno} não cadastrado.")
                
        if estudantes_validos:
            try:
                resultado = self.colecao.insert_many(estudantes_validos)
                print(f"✅ {len(resultado.inserted_ids)} estudantes inseridos em lote com sucesso!")
                return resultado.inserted_ids
            except PyMongoError as e:
                print(f"❌ Erro ao inserir lote: {e}")
        return []

    def ler_um(self, filtro: dict):
        """ Read (R) - Busca um estudante específico """
        try:
            return self.colecao.find_one(filtro)
        except PyMongoError as e:
            print(f"❌ Erro ao buscar estudante: {e}")
            return None

    def ler_varios(self, filtro: dict = {}):
        """ Read (R) - Busca vários estudantes (ou todos se filtro for vazio) """
        try:
            return list(self.colecao.find(filtro))
        except PyMongoError as e:
            print(f"❌ Erro ao buscar estudantes: {e}")
            return []

    def atualizar(self, filtro: dict, novos_dados: dict):
        """ Update (U) - Com proteção de integridade de Chaves (PK e FK) """
        
        # 1. PROTEÇÃO DE CHAVE PRIMÁRIA (PK): Impede a alteração da matrícula via update
        if "matEstudante" in novos_dados:
            print("⚠️ Aviso: A matrícula (Chave Primária) não pode ser alterada. Ignorando este campo.")
            del novos_dados["matEstudante"]

        # 2. PROTEÇÃO DE CHAVE ESTRANGEIRA (FK): Se tentar mudar o CPF, checa se o novo existe
        if "cpf" in novos_dados:
            novo_cpf = novos_dados["cpf"]
            usuario_existe = self.db['usuario'].find_one({"cpf": novo_cpf})
            if not usuario_existe:
                print(f"❌ ERRO: O novo CPF {novo_cpf} não existe em Usuários. Atualização cancelada.")
                return 0

        try:
            resultado = self.colecao.update_one(filtro, {"$set": novos_dados})
            if resultado.modified_count > 0:
                print("🔄 Dados do estudante atualizados com sucesso!")
            else:
                print("⚠️ Nenhum dado foi modificado (os dados já eram iguais).")
            return resultado.modified_count
        except PyMongoError as e:
            print(f"❌ Erro ao atualizar estudante: {e}")
            return 0

    def deletar(self, filtro: dict):
        """ Delete (D) - Deleta o estudante (e consequentemente todos os seus vínculos) """
        try:
            resultado = self.colecao.delete_one(filtro)
            if resultado.deleted_count > 0:
                print("🗑️ Estudante deletado com sucesso!")
            else:
                print("⚠️ Nenhum estudante encontrado para deletar.")
            return resultado.deleted_count
        except PyMongoError as e:
            print(f"❌ Erro ao deletar estudante: {e}")
            return 0


    # ==========================================
    # CRUD DO VÍNCULO (ARRAY EMBUTIDO)
    # ==========================================

    def adicionar_vinculo(self, mat_estudante: str, novo_vinculo: dict):
        """ Create (C) Vínculo - Usa $push com validação de Chave Estrangeira (Curso) """
        id_do_curso = novo_vinculo.get("curso")

        # Verifica se o curso existe na coleção Curso usando o identificador idCurso do SQL
        curso_existe = self.db['curso'].find_one({"idCurso": id_do_curso})
        
        if not curso_existe:
            print(f"❌ ERRO: O curso ID {id_do_curso} não existe. Vínculo cancelado.")
            return 0

        try:
            # Injeta o vínculo na lista do estudante específico
            resultado = self.colecao.update_one(
                {"matEstudante": mat_estudante}, 
                {"$push": {"vinculos": novo_vinculo}}
            )
            if resultado.modified_count > 0:
                print("➕ Vínculo acadêmico adicionado com sucesso!")
            return resultado.modified_count
        except PyMongoError as e:
            print(f"❌ Erro ao adicionar vínculo: {e}")
            return 0

    def atualizar_status_vinculo(self, mat_estudante: str, id_curso: int, novo_status: str):
        """ Update (U) Vínculo - Altera o status usando o operador posicional $ """
        filtro = {
            "matEstudante": mat_estudante,
            "vinculos.curso": id_curso 
        }
        dados_atualizacao = {
            "$set": {"vinculos.$.status": novo_status} 
        }
        
        try:
            resultado = self.colecao.update_one(filtro, dados_atualizacao)
            if resultado.modified_count > 0:
                print(f"🔄 Status do vínculo com curso {id_curso} atualizado para '{novo_status}'.")
            return resultado.modified_count
        except PyMongoError as e:
            print(f"❌ Erro ao atualizar status do vínculo: {e}")
            return 0

    def remover_vinculo(self, mat_estudante: str, id_curso: int):
        """ Delete (D) Vínculo - Remove um curso da lista usando $pull """
        filtro = {"matEstudante": mat_estudante}
        comando_remocao = {
            "$pull": {"vinculos": {"curso": id_curso}}
        }
        
        try:
            resultado = self.colecao.update_one(filtro, comando_remocao)
            if resultado.modified_count > 0:
                print(f"🗑️ Vínculo com o curso {id_curso} removido com sucesso!")
            return resultado.modified_count
        except PyMongoError as e:
            print(f"❌ Erro ao remover vínculo: {e}")
            return 0