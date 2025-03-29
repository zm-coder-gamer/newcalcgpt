package org.example;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Display a welcome message
        System.out.println("Welcome to the Simple Calculator!");

        // Input the first number
        System.out.print("Enter the first number: ");
        double num1 = scanner.nextDouble();

        // Input the second number
        System.out.print("Enter the second number: ");
        double num2 = scanner.nextDouble();

        // Choose the operation
        System.out.println("Choose an operation:");
        System.out.println("1. Addition (+)");
        System.out.println("2. Subtraction (-)");
        System.out.print("Enter your choice (1 or 2): ");
        int choice = scanner.nextInt();

        // Perform the operation
        switch (choice) {
            case 1: // Addition
                double sum = num1 + num2;
                System.out.println("Result: " + num1 + " + " + num2 + " = " + sum);
                break;

            case 2: // Subtraction
                double difference = num1 - num2;
                System.out.println("Result: " + num1 + " - " + num2 + " = " + difference);
                break;

            default: // Invalid choice
                System.out.println("Invalid choice! Please choose 1 for Addition or 2 for Subtraction.");
        }

        // Close the scanner
        scanner.close();
        System.out.println("Thank you for using the Simple Calculator!");
    }
}
