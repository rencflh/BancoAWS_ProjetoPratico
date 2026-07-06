import MODEL.Estudante;
import MODEL.Usuario;

import java.sql.Connection;
import java.sql.Date;
import java.sql.SQLException;

public class Main {
    public static void main(String[] args) {
        // instancia a sua classe de conexão
        DbConnection db = new DbConnection();

        Connection conn = db.conexaoComDB("atividade_engdados", "professor", "professor");

        if (conn != null) {
            try {
                // 2. instancia os data access objects passando a conexão ativa
                UsuarioDAO usuarioDAO = new UsuarioDAO(conn);
                EstudanteDAO estudanteDAO = new EstudanteDAO(conn);

                // PARTE 1: TESTE DO CRUD DE USUÁRIO
                System.out.println("\n--- INICIANDO TESTES DE USUÁRIO ---");

                // configurando arrays
                String[] emailsRenato = {"renato@email.com"};
                String[] telefonesRenato = {"999999999"};

                // instancia o objeto Usuario com o CPF 22222222203
                Usuario teste = new Usuario(
                        99988877700L,
                        "Renato Teste Filho",
                        Date.valueOf("2005-09-05"),
                        emailsRenato,
                        telefonesRenato,
                        "renato123",
                        "r123"
                );

                // CREATE - inserir o usuário no banco
                usuarioDAO.inserir(teste);

                // READ - buscar e printar no console para comprovar
                Usuario usuarioBuscado = usuarioDAO.buscarPorCpf(99988877700L);
                System.out.println("Usuário Encontrado via SELECT: " + usuarioBuscado.getNome());


                // PARTE 2: TESTE DO CRUD DE ESTUDANTE
                System.out.println("\n--- INICIANDO TESTES DE ESTUDANTE ---");

                // instancia o Estudante usando O MESMO CPF do usuário
                Estudante estudanteTeste = new Estudante(
                        "E207",
                        99988877700L, // Chave Estrangeira!
                        6.7,
                        2021
                );

                // CREATE - Inserir o estudante
                estudanteDAO.inserir(estudanteTeste);

                // READ - Buscar estudante para comprovar
                Estudante estBuscado = estudanteDAO.buscarPorMatricula("E207");
                System.out.println("Estudante Encontrado via SELECT: Matrícula " + estBuscado.getMatEstudante() + " | MC: " + estBuscado.getMc());

                // UPDATE - Alterando o MC do estudante e atualizando no banco
                estudanteTeste.setMc(8.5);
                estudanteDAO.atualizar(estudanteTeste);
                System.out.println("MC atualizado no objeto e mandado para o banco.");


            } catch (SQLException e) {
                System.err.println("Erro no banco de dados: " + e.getMessage());
                e.printStackTrace();
            } finally {
                // 3. fechando a conexão
                try {
                    conn.close();
                    System.out.println("\nConexão com a AWS encerrada.");
                } catch (SQLException e) {
                    System.err.println("Erro ao fechar conexão.");
                }
            }
        } else {
            System.out.println("Não foi possível estabelecer conexão com o banco. Abortando testes.");
        }
    }
}