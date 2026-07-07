from pymongo.errors import PyMongoError

class CursoCRUD:
    def __init__(self, database):
        # Recebe o banco de dados para poder inspecionar outras coleções se necessário
        self.db = database
        self.colecao = database['curso']

    def criar(self, dados_curso: dict):
        """ Create (C) - Insere um novo curso individualmente """
        try:
            resultado = self.colecao.insert_one(dados_curso)
            print(f"Curso inserido com sucesso! ID do Curso: {dados_curso.get('idCurso')}")
            return resultado.inserted_id
        except PyMongoError as e:
            print(f"Erro ao inserir curso: {e}")
            return None

    def criar_varios(self, lista_de_cursos: list):
        """ Create Many (C) - Insere vários cursos em lote (útil para carga inicial) """
        try:
            resultado = self.colecao.insert_many(lista_de_cursos)
            print(f"{len(resultado.inserted_ids)} cursos inseridos em lote com sucesso!")
            return resultado.inserted_ids
        except PyMongoError as e:
            print(f"Erro ao inserir lote de cursos: {e}")
            return []

    def ler_um(self, filtro: dict):
        """ Read (R) - Busca um curso específico com base em um filtro """
        try:
            return self.colecao.find_one(filtro)
        except PyMongoError as e:
            print(f"Erro ao buscar curso: {e}")
            return None

    def ler_varios(self, filtro: dict = {}):
        """ Read (R) - Retorna uma lista de cursos com base no filtro """
        try:
            return list(self.colecao.find(filtro))
        except PyMongoError as e:
            print(f"Erro ao buscar cursos: {e}")
            return []

    def atualizar(self, filtro: dict, novos_dados: dict):
        """ Update (U) - Atualiza os dados do curso com proteção de Chave Primária """
        
        # PROTEÇÃO DE CHAVE PRIMÁRIA (PK): Impede a modificação do ID lógico do curso
        if "idCurso" in novos_dados:
            print("Aviso: O idCurso (Chave Primária) não pode ser alterado. Ignorando este campo.")
            del novos_dados["idCurso"]

        try:
            resultado = self.colecao.update_one(filtro, {"$set": novos_dados})
            if resultado.modified_count > 0:
                print("Dados do curso atualizados com sucesso!")
            else:
                print("Nenhum dado foi modificado (os dados já eram idênticos).")
            return resultado.modified_count
        except PyMongoError as e:
            print(f"Erro ao atualizar curso: {e}")
            return 0

    def deletar(self, filtro: dict):
        """ Delete (D) - Remove um curso garantindo a Integridade Referencial """
        
        # 1. Localiza o curso para capturar o idCurso real
        curso = self.ler_um(filtro)
        if not curso:
            print("Nenhum curso encontrado para remover.")
            return 0

        id_curso = curso.get("idCurso")

        # 2. VERIFICAÇÃO DE INTEGRIDADE REFERENCIAL:
        # Verifica se existe algum documento na coleção 'estudante' que possua esse id_curso 
        # dentro da lista embutida de vínculos.
        estudante_vinculado = self.db['estudante'].find_one({"vinculos.curso": id_curso})
        
        if  estudante_vinculado:
            print(f"ERRO DE INTEGRIDADE: O curso ID {id_curso} ({curso.get('nome')}) não pode ser excluído "
                  f"porque existem estudantes ativos vinculados a ele (Ex: Matrícula {estudante_vinculado.get('matEstudante')}).")
            return 0

        # 3. Se nenhum estudante estiver usando o curso, a deleção é segura
        try:
            resultado = self.colecao.delete_one({"idCurso": id_curso})
            if resultado.deleted_count > 0:
                print("Curso removido com sucesso!")
            return resultado.deleted_count
        except PyMongoError as e:
            print(f"Erro ao deletar curso: {e}")
            return 0