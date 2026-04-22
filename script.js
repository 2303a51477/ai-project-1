const pendingList = document.getElementById('pendingList');
const preparedList = document.getElementById('preparedList');
const deliveredList = document.getElementById('deliveredList');
const pendingCount = document.getElementById('pendingCount');
const preparedCount = document.getElementById('preparedCount');
const deliveredCount = document.getElementById('deliveredCount');
const searchResult = document.getElementById('searchResult');
const toast = document.getElementById('toast');

const orderForm = document.getElementById('orderForm');
const prepareBtn = document.getElementById('prepareBtn');
const deliverBtn = document.getElementById('deliverBtn');
const resetBtn = document.getElementById('resetBtn');
const searchBtn = document.getElementById('searchBtn');
const searchInput = document.getElementById('searchInput');

const pendingQueue = [];
const deliveryStack = [];
const deliveredOrders = [];
const statusMap = new Map();

function createOrderCard(order, status) {
    const card = document.createElement('div');
    card.className = 'item-card';

    const title = document.createElement('div');
    title.className = 'item-title';
    title.textContent = `${order.orderId} — ${order.foodItem}`;

    const meta = document.createElement('div');
    meta.className = 'item-meta';
    meta.innerHTML = `
    <span><strong>Customer:</strong> ${order.customerName}</span>
    <span><strong>Qty:</strong> ${order.quantity}</span>
    <span><strong>Bill:</strong> ₹${parseFloat(order.billingAmount).toFixed(2)}</span>
    <span><strong>Status:</strong> ${status}</span>
  `;

    card.append(title, meta);
    return card;
}

function updateCounters() {
    pendingCount.textContent = pendingQueue.length;
    preparedCount.textContent = deliveryStack.length;
    deliveredCount.textContent = deliveredOrders.length;
}

function renderPreparedOrders() {
    renderList(preparedList, [...deliveryStack].slice().reverse(), 'prepared');
}

function renderDeliveredOrders() {
    renderList(deliveredList, deliveredOrders, 'delivered');
}

function renderList(container, items, status) {
    container.innerHTML = '';
    if (!items.length) {
        container.classList.add('empty-state');
        container.textContent = status === 'pending'
            ? 'No pending orders yet.'
            : status === 'prepared'
                ? 'No orders ready for delivery.'
                : 'No delivered orders yet.';
        return;
    }

    container.classList.remove('empty-state');
    items.forEach((order) => {
        const card = createOrderCard(order, status === 'delivered' ? 'Delivered' : status === 'prepared' ? 'Prepared' : 'Pending');
        container.appendChild(card);
    });
}

function showToast(message) {
    toast.textContent = message;
    toast.classList.add('show');
    toast.classList.remove('hidden');
    setTimeout(() => {
        toast.classList.remove('show');
        toast.classList.add('hidden');
    }, 1800);
}

function resetSystem() {
    pendingQueue.length = 0;
    deliveryStack.length = 0;
    deliveredOrders.length = 0;
    statusMap.clear();
    orderForm.reset();
    searchInput.value = '';
    searchResult.textContent = 'Search for an order to see its status.';
    searchResult.classList.add('empty-state');
    renderList(pendingList, pendingQueue, 'pending');
    renderPreparedOrders();
    renderDeliveredOrders();
    updateCounters();
    showToast('System reset complete. All orders cleared.');
}

orderForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const orderId = document.getElementById('orderId').value.trim();
    const customerName = document.getElementById('customerName').value.trim();
    const foodItem = document.getElementById('foodItem').value.trim();
    const quantity = Number(document.getElementById('quantity').value);
    const billingAmount = Number(document.getElementById('billingAmount').value);

    if (!orderId || !customerName || !foodItem || quantity <= 0 || billingAmount <= 0) {
        showToast('Please complete all order fields including billing amount.');
        return;
    }

    if (statusMap.has(orderId)) {
        showToast('Order ID already exists. Use a unique ID.');
        return;
    }

    const order = { orderId, customerName, foodItem, quantity, billingAmount };
    pendingQueue.push(order);
    statusMap.set(orderId, 'Pending');

    renderList(pendingList, pendingQueue, 'pending');
    updateCounters();
    orderForm.reset();
    showToast(`Order ${orderId} added to pending queue.`);
});

prepareBtn.addEventListener('click', () => {
    if (!pendingQueue.length) {
        showToast('No pending orders to prepare.');
        return;
    }

    const nextOrder = pendingQueue.shift();
    statusMap.set(nextOrder.orderId, 'Prepared');
    deliveryStack.push(nextOrder);

    renderList(pendingList, pendingQueue, 'pending');
    renderPreparedOrders();
    updateCounters();
    showToast(`Order ${nextOrder.orderId} is prepared and ready for delivery.`);
});

deliverBtn.addEventListener('click', () => {
    if (!deliveryStack.length) {
        showToast('No prepared orders available for delivery.');
        return;
    }

    const deliveredOrder = deliveryStack.pop();
    statusMap.set(deliveredOrder.orderId, 'Delivered');
    deliveredOrders.unshift(deliveredOrder);

    renderPreparedOrders();
    renderDeliveredOrders();
    updateCounters();
    showToast(`Order ${deliveredOrder.orderId} delivered successfully.`);
});

searchBtn.addEventListener('click', () => {
    const query = searchInput.value.trim();
    if (!query) {
        searchResult.textContent = 'Enter a valid Order ID to search.';
        return;
    }

    const status = statusMap.get(query);
    const message = status
        ? `Order ${query} is currently: ${status}.`
        : `Order ${query} was not found.`;

    searchResult.textContent = message;
    searchResult.classList.remove('empty-state');
});

resetBtn.addEventListener('click', resetSystem);

window.addEventListener('load', () => {
    renderList(pendingList, pendingQueue, 'pending');
    renderPreparedOrders();
    renderDeliveredOrders();
    updateCounters();
});
