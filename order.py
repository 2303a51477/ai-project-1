"""
order.py

Defines the Order class used by the Online Food Delivery Order Management System.
"""

class Order:
    def __init__(self, order_id: str, customer_name: str, food_item: str, quantity: int):
        self.order_id = order_id
        self.customer_name = customer_name
        self.food_item = food_item
        self.quantity = quantity

    def __str__(self):
        return (
            f"Order ID: {self.order_id} | Customer: {self.customer_name} | "
            f"Food: {self.food_item} | Quantity: {self.quantity}"
        )
