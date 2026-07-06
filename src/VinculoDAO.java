import MODEL.Vinculo;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class VinculoDAO {
    private Connection connection;

    public VinculoDAO(Connection connection) {
        this.connection = connection;
    }

    // 1. CREATE
    public void inserir(Vinculo vinculo) throws SQLException {
        // idVinculo SERIAL omitido
        String sql = "INSERT INTO vinculo (mat_estudante, curso, data_entrada, status, data_saida) " +
                "VALUES (?, ?, ?, ?::universidade.status_estudante, ?)";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, vinculo.getMatEstudante());
            stmt.setInt(2, vinculo.getIdCurso());
            stmt.setDate(3, vinculo.getDataEntrada());
            stmt.setString(4, vinculo.getStatus());
            stmt.setDate(5, vinculo.getDataSaida());

            stmt.executeUpdate();
            System.out.println("Vínculo inserido com sucesso!");
        }
    }

    // 2. READ (Por ID)
    public Vinculo buscarPorId(int idVinculo) throws SQLException {
        String sql = "SELECT * FROM vinculo WHERE idVinculo = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, idVinculo);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapearResultSetParaVinculo(rs);
                }
            }
        }
        return null;
    }

    // 3. READ (Listar Todos)
    public List<Vinculo> listarTodos() throws SQLException {
        List<Vinculo> lista = new ArrayList<>();
        String sql = "SELECT * FROM vinculo";

        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            while (rs.next()) {
                lista.add(mapearResultSetParaVinculo(rs));
            }
        }
        return lista;
    }

    // 4. UPDATE
    public void atualizar(Vinculo vinculo) throws SQLException {
        String sql = "UPDATE vinculo SET mat_estudante = ?, curso = ?, data_entrada = ?, " +
                "status = ?::universidade.status_estudante, data_saida = ? WHERE idVinculo = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, vinculo.getMatEstudante());
            stmt.setInt(2, vinculo.getIdCurso());
            stmt.setDate(3, vinculo.getDataEntrada());
            stmt.setString(4, vinculo.getStatus());
            stmt.setDate(5, vinculo.getDataSaida());
            stmt.setInt(6, vinculo.getIdVinculo()); // WHERE

            int linhas = stmt.executeUpdate();
            if (linhas > 0) System.out.println("Vínculo atualizado com sucesso!");
        }
    }

    // 5. DELETE
    public void deletar(int idVinculo) throws SQLException {
        String sql = "DELETE FROM vinculo WHERE idVinculo = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, idVinculo);
            int linhas = stmt.executeUpdate();
            if (linhas > 0) {
                System.out.println("Vínculo deletado com sucesso!");
            } else {
                System.out.println("Nenhum vínculo encontrado com esse ID.");
            }
        }
    }

    // método auxiliar
    private Vinculo mapearResultSetParaVinculo(ResultSet rs) throws SQLException {
        Vinculo v = new Vinculo();
        v.setIdVinculo(rs.getInt("idVinculo"));
        v.setMatEstudante(rs.getString("mat_estudante"));
        v.setIdCurso(rs.getInt("curso"));
        v.setDataEntrada(rs.getDate("data_entrada"));
        v.setStatus(rs.getString("status"));
        v.setDataSaida(rs.getDate("data_saida"));
        return v;
    }
}
