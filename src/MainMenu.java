import MODEL.Curso;
import MODEL.Estudante;
import MODEL.Usuario;
import MODEL.Vinculo;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import java.util.Scanner;

public class MainMenu {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        DbConnection db = new DbConnection();

        System.out.println("Conectando ao banco de dados na AWS...");
        Connection conn = db.conexaoComDB("atividade_engdados", "professor", "professor");

        if (conn == null) {
            System.out.println("Falha ao conectar na AWS. Encerrando o sistema.");
            return;
        }

        try {
            // instancia os DAOs uma única vez
            UsuarioDAO usuarioDAO = new UsuarioDAO(conn);
            EstudanteDAO estudanteDAO = new EstudanteDAO(conn);
            CursoDAO cursoDAO = new CursoDAO(conn);
            VinculoDAO vinculoDAO = new VinculoDAO(conn);

            int opcao = -1;

            // loop do menu principal
            while (opcao != 0) {
                System.out.println("\n=======================================");
                System.out.println("    SISTEMA UNIVERSIDADE - AWS CRUD    ");
                System.out.println("=======================================");
                System.out.println("1. Gerenciar Usuários");
                System.out.println("2. Gerenciar Estudantes");
                System.out.println("3. Gerenciar Cursos");
                System.out.println("4. Gerenciar Vínculos");
                System.out.println("0. Sair");
                System.out.print("Escolha uma opção: ");

                opcao = scanner.nextInt();
                scanner.nextLine(); // limpa o buffer do teclado
                switch (opcao) { // chama os submenus passando o Scanner e o DAO
                    case 1:
                        menuUsuario(scanner, usuarioDAO);
                        break;
                    case 2:
                        menuEstudante(scanner, estudanteDAO);
                        break;
                    case 3:

                        menuCurso(scanner, cursoDAO);
                        break;
                    case 4:
                        menuVinculo(scanner, vinculoDAO);
                        break;
                    case 0:
                        System.out.println("Encerrando o sistema...");
                        break;
                    default:
                        System.out.println("Opção inválida! Tente novamente.");
                }
            }

        } catch (Exception e) {
            System.err.println("Ocorreu um erro no sistema: " + e.getMessage());
        } finally {
            // fecha a conexão
            scanner.close();
            try {
                if (conn != null && !conn.isClosed()) {
                    conn.close();
                    System.out.println("Conexão com a AWS encerrada com sucesso.");
                }
            } catch (SQLException e) {
                System.err.println("Erro ao fechar a conexão.");
            }
        }
    }

    // SUBMENU DE CURSOS
    private static void menuCurso(Scanner scanner, CursoDAO cursoDAO) throws SQLException {
        int opcao = -1;

        while (opcao != 0) {
            System.out.println("\n--- GERENCIAR CURSOS ---");
            System.out.println("1. Inserir Novo Curso");
            System.out.println("2. Listar Todos os Cursos");
            System.out.println("3. Buscar Curso por ID");
            System.out.println("4. Deletar Curso");
            System.out.println("5. Atualizar Registro");
            System.out.println("0. Voltar ao Menu Principal");
            System.out.print("Escolha: ");

            opcao = scanner.nextInt();
            scanner.nextLine(); // limpa o buffer

            switch (opcao) {
                case 1:
                    System.out.println("\n-- INSERIR CURSO --");
                    System.out.print("Nome: ");
                    String nome = scanner.nextLine();
                    System.out.print("Grau (Bacharelado/Licenciatura Plena): ");
                    String grau = scanner.nextLine();
                    System.out.print("Turno (Matutino/Vespertino/Noturno/Turno Indefinido): ");
                    String turno = scanner.nextLine();
                    System.out.print("Campus: ");
                    String campus = scanner.nextLine();
                    System.out.print("Nível (Graduação/Mestrado/Doutorado/Lato): ");
                    String nivel = scanner.nextLine();

                    Curso novoCurso = new Curso(nome, grau, turno, campus, nivel);
                    cursoDAO.inserir(novoCurso);
                    break;

                case 2:
                    System.out.println("\n-- LISTA DE CURSOS --");
                    List<Curso> cursos = cursoDAO.listarTodos();
                    if (cursos.isEmpty()) {
                        System.out.println("Nenhum curso cadastrado.");
                    } else {
                        for (Curso c : cursos) {
                            System.out.println(c.toString());
                        }
                    }
                    break;

                case 3:
                    System.out.println("\n-- BUSCAR CURSO --");
                    System.out.print("Digite o ID do Curso: ");
                    int idBusca = scanner.nextInt();
                    Curso cursoEncontrado = cursoDAO.buscarPorId(idBusca);
                    if (cursoEncontrado != null) {
                        System.out.println("Encontrado: " + cursoEncontrado.toString());
                    } else {
                        System.out.println("Curso não encontrado.");
                    }
                    break;

                case 4:
                    System.out.println("\n-- DELETAR CURSO --");
                    System.out.print("Digite o ID do Curso a ser deletado: ");
                    int idDel = scanner.nextInt();
                    cursoDAO.deletar(idDel);
                    break;

                case 0:
                    System.out.println("Voltando...");
                    break;

                default:
                    System.out.println("Opção inválida!");
            }
        }
    }

    // SUBMENU DE USUÁRIOS
    private static void menuUsuario(Scanner scanner, UsuarioDAO usuarioDAO) throws SQLException {
        int opcao = -1;

        while (opcao != 0) {
            System.out.println("\n--- GERENCIAR USUÁRIOS ---");
            System.out.println("1. Inserir Novo Usuário");
            System.out.println("2. Listar Todos os Usuários");
            System.out.println("3. Buscar Usuário por CPF");
            System.out.println("4. Deletar Usuário");
            System.out.println("5. Atualizar Registro");
            System.out.println("0. Voltar ao Menu Principal");
            System.out.print("Escolha: ");

            opcao = scanner.nextInt();
            scanner.nextLine(); // limpa o buffer

            switch (opcao) {
                case 1:
                    System.out.println("\n-- INSERIR USUÁRIO --");
                    System.out.print("CPF (somente números): ");
                    long cpf = scanner.nextLong();
                    scanner.nextLine(); // limpa o buffer

                    System.out.print("Nome: ");
                    String nome = scanner.nextLine();

                    System.out.print("Data de Nascimento (YYYY-MM-DD): ");
                    java.sql.Date dataNasc = java.sql.Date.valueOf(scanner.nextLine());

                    System.out.print("Emails (separados por vírgula, ou deixe em branco): ");
                    String emailInput = scanner.nextLine();
                    String[] emails = emailInput.isEmpty() ? null : emailInput.split(",");

                    System.out.print("Telefones (separados por vírgula, ou deixe em branco): ");
                    String telInput = scanner.nextLine();
                    String[] telefones = telInput.isEmpty() ? null : telInput.split(",");

                    System.out.print("Login: ");
                    String login = scanner.nextLine();

                    System.out.print("Senha: ");
                    String senha = scanner.nextLine();

                    Usuario novoUsuario = new Usuario(cpf, nome, dataNasc, emails, telefones, login, senha);
                    usuarioDAO.inserir(novoUsuario);
                    break;

                case 2:
                    System.out.println("\n-- LISTA DE USUÁRIOS --");
                    List<Usuario> usuarios = usuarioDAO.listarTodos();
                    if (usuarios.isEmpty()) {
                        System.out.println("Nenhum usuário cadastrado.");
                    } else {
                        for (Usuario u : usuarios) {
                            System.out.println(u.toString());
                        }
                    }
                    break;

                case 3:
                    System.out.println("\n-- BUSCAR USUÁRIO --");
                    System.out.print("Digite o CPF (somente números): ");
                    long cpfBusca = scanner.nextLong();
                    Usuario usuarioEncontrado = usuarioDAO.buscarPorCpf(cpfBusca);
                    if (usuarioEncontrado != null) {
                        System.out.println("Encontrado: " + usuarioEncontrado.toString());
                    } else {
                        System.out.println("Usuário não encontrado.");
                    }
                    break;

                case 4:
                    System.out.println("\n-- DELETAR USUÁRIO --");
                    System.out.print("Digite o CPF do Usuário a ser deletado: ");
                    long cpfDel = scanner.nextLong();
                    usuarioDAO.deletar(cpfDel);
                    break;

                case 0:
                    System.out.println("Voltando...");
                    break;

                default:
                    System.out.println("Opção inválida!");
            }
        }
    }

    // SUBMENU DE ESTUDANTES
    private static void menuEstudante(Scanner scanner, EstudanteDAO estudanteDAO) throws SQLException {
        int opcao = -1;

        while (opcao != 0) {
            System.out.println("\n--- GERENCIAR ESTUDANTES ---");
            System.out.println("1. Inserir Novo Estudante");
            System.out.println("2. Listar Todos os Estudantes");
            System.out.println("3. Buscar Estudante por Matrícula");
            System.out.println("4. Deletar Estudante");
            System.out.println("5. Atualizar Registro");
            System.out.println("0. Voltar ao Menu Principal");
            System.out.print("Escolha: ");

            opcao = scanner.nextInt();
            scanner.nextLine(); // limpa o buffer

            switch (opcao) {
                case 1:
                    System.out.println("\n-- INSERIR ESTUDANTE --");
                    System.out.print("Matrícula (Ex: E206): ");
                    String matricula = scanner.nextLine();

                    System.out.print("CPF do Usuário vinculado (somente números): ");
                    long cpf = scanner.nextLong();

                    System.out.print("MC (Média de Conclusão - use vírgula para decimais dependendo do idioma do SO): ");
                    double mc = scanner.nextDouble();

                    System.out.print("Ano de Ingresso (Ex: 2026): ");
                    int anoIngresso = scanner.nextInt();
                    scanner.nextLine(); // limpa o buffer

                    Estudante novoEstudante = new Estudante(matricula, cpf, mc, anoIngresso);
                    estudanteDAO.inserir(novoEstudante);
                    break;

                case 2:
                    System.out.println("\n-- LISTA DE ESTUDANTES --");
                    List<Estudante> estudantes = estudanteDAO.listarTodos();
                    if (estudantes.isEmpty()) {
                        System.out.println("Nenhum estudante cadastrado.");
                    } else {
                        for (Estudante e : estudantes) {
                            System.out.println(e.toString());
                        }
                    }
                    break;

                case 3:
                    System.out.println("\n-- BUSCAR ESTUDANTE --");
                    System.out.print("Digite a Matrícula: ");
                    String matBusca = scanner.nextLine();
                    Estudante estEncontrado = estudanteDAO.buscarPorMatricula(matBusca);
                    if (estEncontrado != null) {
                        System.out.println("Encontrado: " + estEncontrado.toString());
                    } else {
                        System.out.println("Estudante não encontrado.");
                    }
                    break;

                case 4:
                    System.out.println("\n-- DELETAR ESTUDANTE --");
                    System.out.print("Digite a Matrícula a ser deletada: ");
                    String matDel = scanner.nextLine();
                    estudanteDAO.deletar(matDel);
                    break;

                case 0:
                    System.out.println("Voltando...");
                    break;

                default:
                    System.out.println("Opção inválida!");
            }
        }
    }

    // SUBMENU DE VÍNCULOS
    private static void menuVinculo(Scanner scanner, VinculoDAO vinculoDAO) throws SQLException {
        int opcao = -1;

        while (opcao != 0) {
            System.out.println("\n--- GERENCIAR VÍNCULOS ---");
            System.out.println("1. Inserir Novo Vínculo");
            System.out.println("2. Listar Todos os Vínculos");
            System.out.println("3. Buscar Vínculo por ID");
            System.out.println("4. Deletar Vínculo");
            System.out.println("5. Atualizar Registro");
            System.out.println("0. Voltar ao Menu Principal");
            System.out.print("Escolha: ");

            opcao = scanner.nextInt();
            scanner.nextLine(); // limpa o buffer

            switch (opcao) {
                case 1:
                    System.out.println("\n-- INSERIR VÍNCULO --");
                    System.out.print("Matrícula do Estudante: ");
                    String matricula = scanner.nextLine();

                    System.out.print("ID do Curso: ");
                    int idCurso = scanner.nextInt();
                    scanner.nextLine(); // limpa o buffer

                    System.out.print("Data de Entrada (YYYY-MM-DD): ");
                    java.sql.Date dataEntrada = java.sql.Date.valueOf(scanner.nextLine());

                    System.out.print("Status (Ativo/Cancelada/Formando/Graduado): ");
                    String status = scanner.nextLine();

                    System.out.print("Data de Saída (YYYY-MM-DD ou deixe em branco se não houver): ");
                    String dataSaidaInput = scanner.nextLine();
                    java.sql.Date dataSaida = dataSaidaInput.isEmpty() ? null : java.sql.Date.valueOf(dataSaidaInput);

                    Vinculo novoVinculo = new Vinculo(matricula, idCurso, dataEntrada, status, dataSaida);
                    vinculoDAO.inserir(novoVinculo);
                    break;

                case 2:
                    System.out.println("\n-- LISTA DE VÍNCULOS --");
                    List<Vinculo> vinculos = vinculoDAO.listarTodos();
                    if (vinculos.isEmpty()) {
                        System.out.println("Nenhum vínculo cadastrado.");
                    } else {
                        for (Vinculo v : vinculos) {
                            System.out.println(v.toString());
                        }
                    }
                    break;

                case 3:
                    System.out.println("\n-- BUSCAR VÍNCULO --");
                    System.out.print("Digite o ID do Vínculo: ");
                    int idBusca = scanner.nextInt();
                    Vinculo vinculoEncontrado = vinculoDAO.buscarPorId(idBusca);
                    if (vinculoEncontrado != null) {
                        System.out.println("Encontrado: " + vinculoEncontrado.toString());
                    } else {
                        System.out.println("Vínculo não encontrado.");
                    }
                    break;

                case 4:
                    System.out.println("\n-- DELETAR VÍNCULO --");
                    System.out.print("Digite o ID do Vínculo a ser deletado: ");
                    int idDel = scanner.nextInt();
                    vinculoDAO.deletar(idDel);
                    break;

                case 0:
                    System.out.println("Voltando...");
                    break;

                default:
                    System.out.println("Opção inválida!");
            }
        }
    }
}