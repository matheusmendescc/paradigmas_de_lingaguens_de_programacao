import java.util.Scanner;

public class CalculoSalario {
    public static void main(String[] args) {
        // Instanciando um objeto chamado "Scanner" da classe abstrata Scanner...
        Scanner scanner = new Scanner(System.in);

        //Bloco de entrada de dados com o nome e o salário do funcionário
        System.out.print("Nome: ");
        String nome = scanner.next();

        System.out.println("Salário: ");
        Double sal = scanner.nextDouble();

        // Estrutura de decisão
        if (sal <= 1250){
            sal += (sal*0.15);
        } else {
            sal += (sal*0.1);
        }

        System.out.print("O salário de " + nome + " é de: R$ " + sal);

        // Comando para finalizar o objeto scanner
        scanner.close();
    }
}