import java.sql.*;

public class DbConnection {

    // método de conexão
    public Connection conexaoComDB(String bdNome, String usuario, String senha) {
        Connection conexao = null;
        try {
            Class.forName("org.postgresql.Driver");
            // conexão feita considerando o schema universidade para facilitar
            conexao = DriverManager.getConnection("jdbc:postgresql://engdados-atv2.ckerqud10erx.us-east-1.rds.amazonaws.com:5432/" + bdNome + "?currentSchema=universidade", usuario, senha);
            if (conexao != null) {
                System.out.println("Conexão estabelecida com sucesso!");
            }
        } catch(Exception e) {
            System.out.println("Erro na conexão: " + e.getMessage());
        }
        return conexao;
    }

}