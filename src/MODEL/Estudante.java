package MODEL;

public class Estudante {
    private String matEstudante;
    private long cpf;
    private double mc;
    private int anoIngresso;

    // construtor vazio
    public Estudante() {}

    // construtor completo
    public Estudante(String matEstudante, long cpf, double mc, int anoIngresso) {
        this.matEstudante = matEstudante;
        this.cpf = cpf;
        this.mc = mc;
        this.anoIngresso = anoIngresso;
    }

    // --- GETTERS E SETTERS ---
    public String getMatEstudante() { return matEstudante; }
    public void setMatEstudante(String matEstudante) { this.matEstudante = matEstudante; }

    public long getCpf() { return cpf; }
    public void setCpf(long cpf) { this.cpf = cpf; }

    public double getMc() { return mc; }
    public void setMc(double mc) { this.mc = mc; }

    public int getAnoIngresso() { return anoIngresso; }
    public void setAnoIngresso(int anoIngresso) { this.anoIngresso = anoIngresso; }

    @Override
    public String toString() {
        return "Estudante [Matrícula=" + matEstudante + ", CPF=" + cpf +
                ", MC=" + mc + ", Ano Ingresso=" + anoIngresso + "]";
    }
}
