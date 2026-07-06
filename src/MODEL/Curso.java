package MODEL;

public class Curso {
    private int idCurso; // gerado automaticamente pelo banco (SERIAL)
    private String nome;
    private String grau;
    private String turno;
    private String campus;
    private String nivel;

    // Construtor vazio
    public Curso() {}

    // Construtor SEM idCurso
    public Curso(String nome, String grau, String turno, String campus, String nivel) {
        this.nome = nome;
        this.grau = grau;
        this.turno = turno;
        this.campus = campus;
        this.nivel = nivel;
    }

    // --- GETTERS E SETTERS ---
    public int getIdCurso() { return idCurso; }
    public void setIdCurso(int idCurso) { this.idCurso = idCurso; }

    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }

    public String getGrau() { return grau; }
    public void setGrau(String grau) { this.grau = grau; }

    public String getTurno() { return turno; }
    public void setTurno(String turno) { this.turno = turno; }

    public String getCampus() { return campus; }
    public void setCampus(String campus) { this.campus = campus; }

    public String getNivel() { return nivel; }
    public void setNivel(String nivel) { this.nivel = nivel; }

    @Override
    public String toString() {
        return "Curso [ID=" + idCurso + ", Nome=" + nome + ", Turno=" + turno +
                ", Campus=" + campus + ", Nível=" + nivel + "]";
    }
}
