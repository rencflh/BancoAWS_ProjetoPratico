from pymongo import MongoClient

# A sua Connection String com o usuário e a senha corretos
uri = "mongodb+srv://Maard_db_user:mongo001@cluster-ufs.5fzp98n.mongodb.net/?appName=Cluster-UFS"

def testar_conexao():
    print("Tentando conectar com a AWS...")
    try:
        # Tenta estabelecer a conexão
        client = MongoClient(uri)
        
        # Envia um comando de "ping" para o servidor
        client.admin.command('ping')
        
        print("✅ SUCESSO! Você está conectado ao MongoDB Atlas na AWS.")
        return client
    except Exception as e:
        print("❌ ERRO AO CONECTAR:")
        print(e)
        return None

# Executa a função quando rodar o arquivo
if __name__ == "__main__":
    testar_conexao()