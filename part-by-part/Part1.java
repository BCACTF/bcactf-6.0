import java.util.Scanner;

public class Part1 {

    public static void run(final Scanner sc) {
        System.out.print("Enter an integer: ");
        final int num = sc.nextInt();

        System.out.printf("%d + 1 = %d\n", num, num + 1);
    }
}