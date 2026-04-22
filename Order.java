/**
 * Order.java
 *
 * Represents a single food delivery order with core order details.
 */
public class Order {
    private String orderId;
    private String customerName;
    private String foodItem;
    private int quantity;

    public Order(String orderId, String customerName, String foodItem, int quantity) {
        this.orderId = orderId;
        this.customerName = customerName;
        this.foodItem = foodItem;
        this.quantity = quantity;
    }

    public String getOrderId() {
        return orderId;
    }

    public String getCustomerName() {
        return customerName;
    }

    public String getFoodItem() {
        return foodItem;
    }

    public int getQuantity() {
        return quantity;
    }

    @Override
    public String toString() {
        return String.format("Order ID: %s | Customer: %s | Food: %s | Qty: %d",
                orderId, customerName, foodItem, quantity);
    }
}
