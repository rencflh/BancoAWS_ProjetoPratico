import MODEL.Estudante;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class EstudanteDAO {
    private Connection connection;

    public EstudanteDAO(Connection connection) {
        this.connection = connection;
    }

    // 1. CREATE
    public void inserir(Estudante estudante) throws SQLException {
        // o cpf informado aqui JÁ DEVE existir na tabela Usuario
        String sql = "INSERT INTO estudante (mat_estudante, cpf, mc, ano_ingresso) VALUES (?, ?, ?, ?)";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, estudante.getMatEstudante());
            stmt.setLong(2, estudante.getCpf());
            stmt.setDouble(3, estudante.getMc());
            stmt.setInt(4, estudante.getAnoIngresso());

            stmt.executeUpdate();
            System.out.println("Estudante inserido com sucesso!");
        }
    }

    // 2. READ (Buscar por Matrícula)
    public Estudante buscarPorMatricula(String matricula) throws SQLException {
        String sql = "SELECT * FROM estudante WHERE mat_estudante = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, matricula);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapearResultSetParaEstudante(rs);
                }
            }
        }
        return null; // retorna null se não encontrar a matrícula
    }

    // 3. READ
    public List<Estudante> listarTodos() throws SQLException {
        List<Estudante> lista = new ArrayList<>();
        String sql = "SELECT * FROM estudante";

        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            while (rs.next()) {
                lista.add(mapearResultSetParaEstudante(rs));
            }
        }
        return lista;
    }

    // 4. UPDATE
    public void atualizar(Estudante estudante) throws SQLException {
        // atualizamos o CPF, MC e ano_ingresso baseados na matrícula, que não muda
        String sql = "UPDATE estudante SET cpf = ?, mc = ?, ano_ingresso = ? WHERE mat_estudante = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setLong(1, estudante.getCpf());
            stmt.setDouble(2, estudante.getMc());
            stmt.setInt(3, estudante.getAnoIngresso());
            stmt.setString(4, estudante.getMatEstudante()); // WHERE

            int linhas = stmt.executeUpdate();
            if(linhas > 0) {
                System.out.println("Estudante atualizado com sucesso!");
            } else {
                System.out.println("Matrícula não encontrada para atualização.");
            }
        }
    }

    // 5. DELETE
    public void deletar(String matricula) throws SQLException {
        String sql = "DELETE FROM estudante WHERE mat_estudante = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, matricula);
            int linhas = stmt.executeUpdate();
            if (linhas > 0) {
                System.out.println("Estudante deletado com sucesso!");
            } else {
                System.out.println("Nenhum estudante encontrado com essa matrícula.");
            }
        }
    }

    // método auxiliar
    private Estudante mapearResultSetParaEstudante(ResultSet rs) throws SQLException {
        Estudante e = new Estudante();
        e.setMatEstudante(rs.getString("mat_estudante"));
        e.setCpf(rs.getLong("cpf"));
        e.setMc(rs.getDouble("mc"));
        e.setAnoIngresso(rs.getInt("ano_ingresso"));
        return e;
    }
}
