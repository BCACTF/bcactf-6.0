import java.util.Scanner;

public class Main {
    
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            System.out.println("Welcome to my program.");
            System.out.println("Choose an option:");
            System.out.println("1) Add 1");
            System.out.println("2) Subtract 2");
            System.out.println("3) Multiply by 3");
            System.out.println("4) Divide by 4");
    
            System.out.print("> ");
            final int option = sc.nextInt();

            switch (option) {
                case 1 -> Part1.run(sc);
                case 2 -> Part2.run(sc);
                case 3 -> Part3.run(sc);
                case 4 -> Part4.run(sc);
            }

            System.out.println("Bye bye.");
        }
        
    }
}
