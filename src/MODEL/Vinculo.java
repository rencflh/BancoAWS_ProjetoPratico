package MODEL;

import java.sql.Date;

public class Vinculo {
    private int idVinculo; // SERIAL
    private String matEstudante; // FK para Estudante
    private int idCurso; // FK para Curso
    private Date dataEntrada;
    private String status; // valores do ENUM do banco
    private Date dataSaida;

    public Vinculo() {}

    // Construtor sem o idVinculo
    public Vinculo(String matEstudante, int idCurso, Date dataEntrada, String status, Date dataSaida) {
        this.matEstudante = matEstudante;
        this.idCurso = idCurso;
        this.dataEntrada = dataEntrada;
        this.status = status;
        this.dataSaida = dataSaida;
    }

    // --- GETTERS E SETTERS ---
    public int getIdVinculo() { return idVinculo; }
    public void setIdVinculo(int idVinculo) { this.idVinculo = idVinculo; }

    public String getMatEstudante() { return matEstudante; }
    public void setMatEstudante(String matEstudante) { this.matEstudante = matEstudante; }

    public int getIdCurso() { return idCurso; }
    public void setIdCurso(int idCurso) { this.idCurso = idCurso; }

    public Date getDataEntrada() { return dataEntrada; }
    public void setDataEntrada(Date dataEntrada) { this.dataEntrada = dataEntrada; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Date getDataSaida() { return dataSaida; }
    public void setDataSaida(Date dataSaida) { this.dataSaida = dataSaida; }

    @Override
    public String toString() {
        return "Vinculo [ID=" + idVinculo + ", Matrícula=" + matEstudante +
                ", Curso ID=" + idCurso + ", Status=" + status + "]";
    }
}
