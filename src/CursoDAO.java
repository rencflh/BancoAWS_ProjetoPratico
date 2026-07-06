import MODEL.Curso;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class CursoDAO {
    private Connection connection;

    public CursoDAO(Connection connection) {
        this.connection = connection;
    }

    // 1. CREATE
    public void inserir(Curso curso) throws SQLException {
        // idCurso oculto pois eh serial
        String sql = "INSERT INTO curso (nome, grau, turno, campus, nivel) " +
                "VALUES (?, ?::universidade.tipo_grau, ?::universidade.tipo_turno, ?, ?::universidade.tipo_nivel)";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, curso.getNome());
            stmt.setString(2, curso.getGrau());
            stmt.setString(3, curso.getTurno());
            stmt.setString(4, curso.getCampus());
            stmt.setString(5, curso.getNivel());

            stmt.executeUpdate();
            System.out.println("Curso inserido com sucesso!");
        }
    }

    // 2. READ (Buscar por ID do Curso)
    public Curso buscarPorId(int idCurso) throws SQLException {
        String sql = "SELECT * FROM curso WHERE idCurso = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, idCurso);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapearResultSetParaCurso(rs);
                }
            }
        }
        return null;
    }

    // 3. READ (Listar Todos)
    public List<Curso> listarTodos() throws SQLException {
        List<Curso> lista = new ArrayList<>();
        String sql = "SELECT * FROM curso";

        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            while (rs.next()) {
                lista.add(mapearResultSetParaCurso(rs));
            }
        }
        return lista;
    }

    // 4. UPDATE
    public void atualizar(Curso curso) throws SQLException {
        String sql = "UPDATE curso SET nome = ?, grau = ?::universidade.tipo_grau, " +
                "turno = ?::universidade.tipo_turno, campus = ?, nivel = ?::universidade.tipo_nivel " +
                "WHERE idCurso = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, curso.getNome());
            stmt.setString(2, curso.getGrau());
            stmt.setString(3, curso.getTurno());
            stmt.setString(4, curso.getCampus());
            stmt.setString(5, curso.getNivel());
            stmt.setInt(6, curso.getIdCurso()); // WHERE

            int linhas = stmt.executeUpdate();
            if(linhas > 0) System.out.println("Curso atualizado com sucesso!");
        }
    }

    // 5. DELETE
    public void deletar(int idCurso) throws SQLException {
        String sql = "DELETE FROM curso WHERE idCurso = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setInt(1, idCurso);
            int linhas = stmt.executeUpdate();
            if (linhas > 0) {
                System.out.println("Curso deletado com sucesso!");
            } else {
                System.out.println("Nenhum curso encontrado com esse ID.");
            }
        }
    }

    // método auxiliar
    private Curso mapearResultSetParaCurso(ResultSet rs) throws SQLException {
        Curso c = new Curso();
        c.setIdCurso(rs.getInt("idCurso"));
        c.setNome(rs.getString("nome"));
        c.setGrau(rs.getString("grau"));
        c.setTurno(rs.getString("turno"));
        c.setCampus(rs.getString("campus"));
        c.setNivel(rs.getString("nivel"));
        return c;
    }
}
