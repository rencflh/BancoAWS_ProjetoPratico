import java.sql.*;

public class TesteJDBC {
	
   public Connection conexao = null;
	
   public TesteJDBC() {
      try{
         //Carregar driver JDBC do postgress
         Class.forName("org.postgresql.Driver"); 
         System.out.println("Carregou agora");
      } catch (ClassNotFoundException ex){ex.printStackTrace();}
   }

	public void setConnection() throws SQLException {
		String host = "engdados-atv2.ckerqud10erx.us-east-1.rds.amazonaws.com:5432";
		String db = "atividade_engdados";
		String url = "jdbc:postgresql://" + host + "/" + db;
		String user = "professor";
		String senha = "professor";

		conexao = DriverManager.getConnection(url, user, senha);
		System.out.println("Criou a conexão");
	}
   
   public void exemploConsultaStatment(Connection conexao) throws SQLException{
	   String sql = "Select * from universidade.usuario WHERE cpf = 11111111100";
	   Statement comando = conexao.createStatement();
	   System.out.println("Executar consulta: " + sql);
	   ResultSet resultado = comando.executeQuery(sql);
	   while(resultado.next()){
	      String cpf = resultado.getString("data_nascimento");
	      String cpf2 = resultado.getString(1);
	     System.out.println(cpf2);
	   }	
	   comando.close();
	}
   
   public void exemploConsultaPreparedStatment(Connection conexao) throws SQLException{
	   String sql = "Select * from universidade.professor where nome = ?";
	   PreparedStatement comando = conexao.prepareStatement(sql);
	   System.out.println("Executar consulta: " + sql);
	   comando.setString(1, "P100");
	   ResultSet resultado = comando.executeQuery();
	   while(resultado.next()){
	      String cpf = resultado.getString("cpf");
	      System.out.println(cpf);
	   }	
	}
   
   public void exemploConsultaStatmentMeta(Connection conexao) throws SQLException{
	   String sql = "SELECT * FROM universidade.professor WHERE departamento = 'DCOMP'";
	   Statement comando = conexao.createStatement();
	   System.out.println("Executar consulta: " + sql);
	   ResultSet resultado = comando.executeQuery(sql);
	   ResultSetMetaData rsm = resultado.getMetaData();
	   while(resultado.next()){
		   for(int i = 1; i<=rsm.getColumnCount(); i++){
			   String campo = resultado.getString(i);
			   System.out.print(campo + "\t");
		   }
		   System.out.println();
	   }
   }
   


   public static void main(String[] args) {
      TesteJDBC teste = new TesteJDBC();
      try{
    	  teste.setConnection();
    	  teste.exemploConsultaStatment(teste.conexao);
    	  //teste.exemploConsultaPreparedStatment(teste.conexao);
    	  teste.conexao.close();
    	  
      } catch(SQLException ex) {ex.printStackTrace();}
   }
}
