/**
 * Main.java
 *
 * Online Food Delivery Order Management System
 * Console application demonstrating Queue, Stack, and HashMap usage.
 */

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Scanner;
import java.util.Stack;

public class Main {
    private static LinkedList<Order> pendingQueue = new LinkedList<>();
    private static Stack<Order> preparedStack = new Stack<>();
    private static HashMap<String, String> statusMap = new HashMap<>();
    private static ArrayList<Order> deliveredOrders = new ArrayList<>();
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        printHeader();
        boolean running = true;

        while (running) {
            printMenu();
            int choice = readIntegerInput("Enter your choice: ");

            switch (choice) {
                case 1:
                    addNewOrder();
                    break;
                case 2:
                    prepareNextOrder();
                    break;
                case 3:
                    deliverNextOrder();
                    break;
                case 4:
                    searchOrderById();
                    break;
                case 5:
                    displayAllOrders();
                    break;
                case 6:
                    running = false;
                    System.out.println("\nThank you for using the Online Food Delivery Order Management System.");
                    break;
                default:
                    System.out.println("Invalid selection. Please choose a number between 1 and 6.\n");
            }
        }

        scanner.close();
    }

    private static void printHeader() {
        System.out.println("===============================================");
        System.out.println("   Online Food Delivery Order Management System");
        System.out.println("   Queue, Stack, and HashMap Simulation");
        System.out.println("===============================================\n");
    }

    private static void printMenu() {
        System.out.println("Main Menu:");
        System.out.println("1. Add New Order");
        System.out.println("2. Prepare Next Order");
        System.out.println("3. Deliver Next Order");
        System.out.println("4. Search Order by ID");
        System.out.println("5. Display All Orders");
        System.out.println("6. Exit\n");
    }

    private static int readIntegerInput(String prompt) {
        while (true) {
            System.out.print(prompt);
            String input = scanner.nextLine().trim();

            try {
                return Integer.parseInt(input);
            } catch (NumberFormatException e) {
                System.out.println("Invalid entry. Please enter a valid number.");
            }
        }
    }

    private static String readStringInput(String prompt) {
        while (true) {
            System.out.print(prompt);
            String input = scanner.nextLine().trim();

            if (!input.isEmpty()) {
                return input;
            }

            System.out.println("This field cannot be empty. Please enter a valid value.");
        }
    }

    private static void addNewOrder() {
        System.out.println("\n--- Add New Order ---");
        String orderId = readStringInput("Order ID: ");

        if (statusMap.containsKey(orderId)) {
            System.out.println("Error: Order ID already exists. Please use a different ID.\n");
            return;
        }

        String customerName = readStringInput("Customer Name: ");
        String foodItem = readStringInput("Food Item Name: ");
        int quantity = readIntegerInput("Quantity: ");

        if (quantity <= 0) {
            System.out.println("Quantity must be at least 1. Order not added.\n");
            return;
        }

        Order newOrder = new Order(orderId, customerName, foodItem, quantity);
        pendingQueue.add(newOrder);
        statusMap.put(orderId, "Pending");

        System.out.println("Order added successfully and placed in the pending queue.\n");
    }

    private static void prepareNextOrder() {
        System.out.println("\n--- Prepare Next Order ---");

        if (pendingQueue.isEmpty()) {
            System.out.println("No pending orders are available to prepare.\n");
            return;
        }

        Order nextOrder = pendingQueue.removeFirst();
        statusMap.put(nextOrder.getOrderId(), "Prepared");
        preparedStack.push(nextOrder);

        System.out.println("Order " + nextOrder.getOrderId() + " has been prepared and moved to the delivery stack.\n");
    }

    private static void deliverNextOrder() {
        System.out.println("\n--- Deliver Next Order ---");

        if (preparedStack.isEmpty()) {
            System.out.println("No prepared orders are available for delivery.\n");
            return;
        }

        Order deliveredOrder = preparedStack.pop();
        statusMap.put(deliveredOrder.getOrderId(), "Delivered");
        deliveredOrders.add(deliveredOrder);

        System.out.println("Order " + deliveredOrder.getOrderId() + " has been delivered successfully.\n");
    }

    private static void searchOrderById() {
        System.out.println("\n--- Search Order by ID ---");
        String orderId = readStringInput("Enter Order ID: ");

        if (!statusMap.containsKey(orderId)) {
            System.out.println("Order not found. Please ensure the Order ID is correct.\n");
            return;
        }

        String status = statusMap.get(orderId);
        System.out.println("Status for Order " + orderId + ": " + status);
        System.out.println("Order details are shown below if available.\n");

        Order order = findOrderInAllStructures(orderId);

        if (order != null) {
            System.out.println(order.toString() + " | Current Status: " + status + "\n");
        } else {
            System.out.println("Order details are not available in the current lists.\n");
        }
    }

    private static Order findOrderInAllStructures(String orderId) {
        for (Order order : pendingQueue) {
            if (order.getOrderId().equals(orderId)) {
                return order;
            }
        }

        for (Order order : preparedStack) {
            if (order.getOrderId().equals(orderId)) {
                return order;
            }
        }

        for (Order order : deliveredOrders) {
            if (order.getOrderId().equals(orderId)) {
                return order;
            }
        }

        return null;
    }

    private static void displayAllOrders() {
        System.out.println("\n--- Display All Orders ---");

        System.out.println("Pending Orders (Queue FIFO):");
        if (pendingQueue.isEmpty()) {
            System.out.println("  No pending orders.");
        } else {
            for (Order order : pendingQueue) {
                System.out.println("  " + order.toString() + " | Status: Pending");
            }
        }

        System.out.println("\nPrepared Orders (Stack LIFO):");
        if (preparedStack.isEmpty()) {
            System.out.println("  No prepared orders.");
        } else {
            for (int i = preparedStack.size() - 1; i >= 0; i--) {
                Order order = preparedStack.get(i);
                System.out.println("  " + order.toString() + " | Status: Prepared");
            }
        }

        System.out.println("\nDelivered Orders:");
        if (deliveredOrders.isEmpty()) {
            System.out.println("  No delivered orders.");
        } else {
            for (Order order : deliveredOrders) {
                System.out.println("  " + order.toString() + " | Status: Delivered");
            }
        }

        System.out.println();
    }
}
