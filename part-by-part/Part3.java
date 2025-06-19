import java.util.Scanner;

public class Part3 {

    public static void run(final Scanner sc) {
        System.out.print("Enter an integer: ");
        final int num = sc.nextInt();

        System.out.printf("%d * 3 = %d\n", num, num * 3);
    }
}