import MODEL.Usuario;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class UsuarioDAO {
    private Connection connection;

    public UsuarioDAO(Connection connection) {
        this.connection = connection;
    }

    // 1. CREATE
    public void inserir(Usuario usuario) throws SQLException {
        String sql = "INSERT INTO usuario (cpf, nome, data_nascimento, email, telefone, login, senha) VALUES (?, ?, ?, ?, ?, ?, ?)";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setLong(1, usuario.getCpf());
            stmt.setString(2, usuario.getNome());
            stmt.setDate(3, usuario.getDataNascimento());

            // tratamento para os arrays do PostgreSQL
            Array arrayEmails = usuario.getEmails() != null ? connection.createArrayOf("varchar", usuario.getEmails()) : null;
            Array arrayTelefones = usuario.getTelefones() != null ? connection.createArrayOf("varchar", usuario.getTelefones()) : null;

            stmt.setArray(4, arrayEmails);
            stmt.setArray(5, arrayTelefones);
            stmt.setString(6, usuario.getLogin());
            stmt.setString(7, usuario.getSenha());

            stmt.executeUpdate();
            System.out.println("Usuário inserido com sucesso!");
        }
    }

    // 2. READ (Buscar por CPF)
    public Usuario buscarPorCpf(long cpf) throws SQLException {
        String sql = "SELECT * FROM usuario WHERE cpf = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setLong(1, cpf);
            try (ResultSet rs = stmt.executeQuery()) {
                if (rs.next()) {
                    return mapearResultSetParaUsuario(rs);
                }
            }
        }
        return null;
    }

    // 3. READ
    public List<Usuario> listarTodos() throws SQLException {
        List<Usuario> lista = new ArrayList<>();
        String sql = "SELECT * FROM usuario";

        try (PreparedStatement stmt = connection.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            while (rs.next()) {
                lista.add(mapearResultSetParaUsuario(rs));
            }
        }
        return lista;
    }

    // 4. UPDATE
    public void atualizar(Usuario usuario) throws SQLException {
        String sql = "UPDATE usuario SET nome = ?, data_nascimento = ?, email = ?, telefone = ?, login = ?, senha = ? WHERE cpf = ?";

        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setString(1, usuario.getNome());
            stmt.setDate(2, usuario.getDataNascimento());

            Array arrayEmails = usuario.getEmails() != null ? connection.createArrayOf("varchar", usuario.getEmails()) : null;
            Array arrayTelefones = usuario.getTelefones() != null ? connection.createArrayOf("varchar", usuario.getTelefones()) : null;

            stmt.setArray(3, arrayEmails);
            stmt.setArray(4, arrayTelefones);
            stmt.setString(5, usuario.getLogin());
            stmt.setString(6, usuario.getSenha());
            stmt.setLong(7, usuario.getCpf()); // WHERE

            int linhas = stmt.executeUpdate();
            if(linhas > 0) System.out.println("Usuário atualizado com sucesso!");
        }
    }

    // 5. DELETE
    public void deletar(long cpf) throws SQLException {
        String sql = "DELETE FROM usuario WHERE cpf = ?";
        try (PreparedStatement stmt = connection.prepareStatement(sql)) {
            stmt.setLong(1, cpf);
            int linhas = stmt.executeUpdate();
            if (linhas > 0) {
                System.out.println("Usuário deletado com sucesso!");
            } else {
                System.out.println("Nenhum usuário encontrado com esse CPF.");
            }
        }
    }

    // método auxiliar
    private Usuario mapearResultSetParaUsuario(ResultSet rs) throws SQLException {
        Usuario u = new Usuario();
        u.setCpf(rs.getLong("cpf"));
        u.setNome(rs.getString("nome"));
        u.setDataNascimento(rs.getDate("data_nascimento"));

        // lendo os arrays do banco e convertendo de volta para String[]
        Array rsEmails = rs.getArray("email");
        if (rsEmails != null) u.setEmails((String[]) rsEmails.getArray());

        Array rsTelefones = rs.getArray("telefone");
        if (rsTelefones != null) u.setTelefones((String[]) rsTelefones.getArray());

        u.setLogin(rs.getString("login"));
        u.setSenha(rs.getString("senha"));

        return u;
    }
}
