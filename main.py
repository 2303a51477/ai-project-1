"""
main.py

Console application for Online Food Delivery Order Management System.
Uses Queue, Stack, and Dictionary data structures.
"""

from collections import deque
from order import Order

pending_queue = deque()
prepared_stack = []
delivered_orders = []
status_map = {}


def print_header():
    print("=" * 60)
    print("Online Food Delivery Order Management System")
    print("Queue, Stack, and Dictionary Simulation")
    print("=" * 60)
    print()


def print_menu():
    print("Menu Options:")
    print("1. Add New Order")
    print("2. Prepare Next Order")
    print("3. Deliver Next Order")
    print("4. Search Order by ID")
    print("5. Display All Orders")
    print("6. Exit")
    print()


def read_nonempty_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please enter a valid value.")


def read_positive_integer(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("Please enter a valid positive integer.")


def add_new_order():
    print("\n--- Add New Order ---")
    order_id = read_nonempty_text("Order ID: ")
    if order_id in status_map:
        print("Error: Order ID already exists. Use a different Order ID.\n")
        return

    customer_name = read_nonempty_text("Customer Name: ")
    food_item = read_nonempty_text("Food Item Name: ")
    quantity = read_positive_integer("Quantity: ")

    order = Order(order_id, customer_name, food_item, quantity)
    pending_queue.append(order)
    status_map[order_id] = "Pending"
    print("Order added successfully and placed in the pending queue.\n")


def prepare_next_order():
    print("\n--- Prepare Next Order ---")
    if not pending_queue:
        print("No pending orders are available to prepare.\n")
        return

    order = pending_queue.popleft()
    status_map[order.order_id] = "Prepared"
    prepared_stack.append(order)
    print(f"Order {order.order_id} has been prepared and moved to the prepared stack.\n")


def deliver_next_order():
    print("\n--- Deliver Next Order ---")
    if not prepared_stack:
        print("No prepared orders are available for delivery.\n")
        return

    order = prepared_stack.pop()
    status_map[order.order_id] = "Delivered"
    delivered_orders.append(order)
    print(f"Order {order.order_id} has been delivered successfully.\n")


def search_order_by_id():
    print("\n--- Search Order by ID ---")
    order_id = read_nonempty_text("Enter Order ID: ")
    status = status_map.get(order_id)

    if not status:
        print(f"Order {order_id} was not found.\n")
        return

    order = find_order_by_id(order_id)
    print(f"Status: {status}")
    if order:
        print(order)
    print()


def find_order_by_id(order_id):
    for order in pending_queue:
        if order.order_id == order_id:
            return order
    for order in prepared_stack:
        if order.order_id == order_id:
            return order
    for order in delivered_orders:
        if order.order_id == order_id:
            return order
    return None


def display_all_orders():
    print("\n--- Display All Orders ---")
    print("\nPending Orders (Queue FIFO):")
    if pending_queue:
        for order in pending_queue:
            print(f"  {order} | Status: Pending")
    else:
        print("  No pending orders.")

    print("\nPrepared Orders (Stack LIFO):")
    if prepared_stack:
        for order in reversed(prepared_stack):
            print(f"  {order} | Status: Prepared")
    else:
        print("  No prepared orders.")

    print("\nDelivered Orders:")
    if delivered_orders:
        for order in delivered_orders:
            print(f"  {order} | Status: Delivered")
    else:
        print("  No delivered orders.")
    print()


def main():
    print_header()
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_new_order()
        elif choice == "2":
            prepare_next_order()
        elif choice == "3":
            deliver_next_order()
        elif choice == "4":
            search_order_by_id()
        elif choice == "5":
            display_all_orders()
        elif choice == "6":
            print("\nGoodbye! Thank you for using the system.")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 6.\n")


if __name__ == "__main__":
    main()
