from pymongo import MongoClient
import os
from dotenv import load_dotenv

# puxa a string de conexão usando o os.getenv
# mudar o ip no codigo .env
load_dotenv()
uri = os.getenv("MONGO_URI")

def testar_conexao():
    print("Tentando conectar com a AWS...")
    try:
        # possível falha no arquivo .env
        if not uri:
            raise ValueError("A variável MONGO_URI não foi encontrada. Verifique o arquivo .env.")
        # Tenta estabelecer a conexão
        client = MongoClient(uri)
        
        # Envia um comando de "ping" para o servidor
        client.admin.command('ping')
        
        print("SUCESSO! Você está conectado ao MongoDB Atlas na AWS.")
        return client
    except Exception as e:
        print("ERRO AO CONECTAR:")
        print(e)
        return None

# Executa a função quando rodar o arquivo
if __name__ == "__main__":
    testar_conexao()