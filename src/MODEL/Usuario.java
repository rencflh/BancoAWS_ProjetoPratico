package MODEL;

import java.sql.Date;
import java.util.Arrays;

public class Usuario {
    private long cpf;
    private String nome;
    private Date dataNascimento;
    private String[] emails;     // array por conta do VARCHAR[] do banco
    private String[] telefones;  // array por conta do VARCHAR[] do banco
    private String login;
    private String senha;

    // construtor vazio
    public Usuario() {}

    // construtor com todos os campos
    public Usuario(long cpf, String nome, Date dataNascimento, String[] emails, String[] telefones, String login, String senha) {
        this.cpf = cpf;
        this.nome = nome;
        this.dataNascimento = dataNascimento;
        this.emails = emails;
        this.telefones = telefones;
        this.login = login;
        this.senha = senha;
    }

    // --- GETTERS E SETTERS ---
    public long getCpf() { return cpf; }
    public void setCpf(long cpf) { this.cpf = cpf; }

    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }

    public Date getDataNascimento() { return dataNascimento; }
    public void setDataNascimento(Date dataNascimento) { this.dataNascimento = dataNascimento; }

    public String[] getEmails() { return emails; }
    public void setEmails(String[] emails) { this.emails = emails; }

    public String[] getTelefones() { return telefones; }
    public void setTelefones(String[] telefones) { this.telefones = telefones; }

    public String getLogin() { return login; }
    public void setLogin(String login) { this.login = login; }

    public String getSenha() { return senha; }
    public void setSenha(String senha) { this.senha = senha; }


    @Override
    public String toString() {
        return "Usuario [CPF=" + cpf + ", Nome=" + nome +
                ", Emails=" + Arrays.toString(emails) +
                ", Telefones=" + Arrays.toString(telefones) + "]";
    }
}
