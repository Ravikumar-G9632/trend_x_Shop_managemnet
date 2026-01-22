// API Base URL
const API_BASE = '/api';

// Initialize app on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Trend_X Shop Management System Initialized');
    loadDashboard();
    loadProducts();
    loadCustomers();
    loadOrders();
    
    // Attach form event listeners
    document.getElementById('addProductForm').addEventListener('submit', handleAddProduct);
    document.getElementById('addCustomerForm').addEventListener('submit', handleAddCustomer);
    document.getElementById('addOrderForm').addEventListener('submit', handleAddOrder);
});

// Show specific section
function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));
    
    // Remove active class from all nav buttons
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(button => button.classList.remove('active'));
    
    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add('active');
    }
    
    // Add active class to clicked button
    event.target.classList.add('active');
    
    // Load data for specific sections
    if (sectionId === 'products') {
        loadProducts();
    } else if (sectionId === 'customers') {
        loadCustomers();
    } else if (sectionId === 'orders') {
        loadOrders();
    } else if (sectionId === 'dashboard') {
        loadDashboard();
    }
}

// Load Dashboard Stats
function loadDashboard() {
    fetch(`${API_BASE}/dashboard`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('productCount').textContent = data.total_products;
                document.getElementById('customerCount').textContent = data.total_customers;
                document.getElementById('orderCount').textContent = data.total_orders;
                document.getElementById('totalRevenue').textContent = '$' + data.total_revenue.toLocaleString();
                document.getElementById('inventoryValue').textContent = '$' + data.inventory_value.toLocaleString();
                document.getElementById('status').textContent = '🟢 Connected';
            } else {
                console.error('Error loading dashboard:', data.error);
                document.getElementById('status').textContent = '🔴 Error';
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            document.getElementById('status').textContent = '🔴 Error';
        });
}

// ==================== PRODUCTS ====================

// Load Products
function loadProducts() {
    fetch(`${API_BASE}/products`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayProducts(data.products);
            } else {
                console.error('Error loading products:', data.error);
            }
        })
        .catch(error => console.error('Fetch error:', error));
}

// Display Products
function displayProducts(products) {
    const productsList = document.getElementById('productsList');
    
    if (products.length === 0) {
        productsList.innerHTML = '<p class="empty-state">No products yet. Add one to get started!</p>';
        return;
    }
    
    productsList.innerHTML = products.map(product => `
        <div class="product-item">
            <div class="product-info">
                <h4>👕 ${escapeHtml(product.name)}</h4>
                <p><strong>Category:</strong> ${escapeHtml(product.category)}</p>
                <p><strong>Size:</strong> ${escapeHtml(product.size) || 'N/A'} | <strong>Color:</strong> ${escapeHtml(product.color) || 'N/A'}</p>
                <p><strong>Stock:</strong> ${product.quantity} units</p>
                <p class="product-price">💰 $${product.price.toFixed(2)}</p>
                <p style="font-size: 0.8rem; margin-top: 5px; color: #94a3b8;">
                    Added: ${new Date(product.created_at).toLocaleDateString()}
                </p>
            </div>
            <button class="btn btn-danger" onclick="deleteProduct('${product._id}')">Delete</button>
        </div>
    `).join('');
}

// Handle Add Product
function handleAddProduct(event) {
    event.preventDefault();
    
    const name = document.getElementById('productName').value.trim();
    const category = document.getElementById('productCategory').value;
    const price = document.getElementById('productPrice').value;
    const quantity = document.getElementById('productQuantity').value;
    const size = document.getElementById('productSize').value.trim();
    const color = document.getElementById('productColor').value.trim();
    const description = document.getElementById('productDescription').value.trim();
    
    if (!name || !category || !price || quantity === '') {
        alert('Please fill in all required fields');
        return;
    }
    
    fetch(`${API_BASE}/products`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, category, price, quantity, size, color, description })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Product added successfully!');
            document.getElementById('addProductForm').reset();
            loadProducts();
            loadDashboard();
        } else {
            alert('❌ Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Error adding product');
    });
}

// Delete Product
function deleteProduct(productId) {
    if (confirm('Are you sure you want to delete this product?')) {
        fetch(`${API_BASE}/products/${productId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('✅ Product deleted successfully!');
                loadProducts();
                loadDashboard();
            } else {
                alert('❌ Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('❌ Error deleting product');
        });
    }
}

// ==================== CUSTOMERS ====================

// Load Customers
function loadCustomers() {
    fetch(`${API_BASE}/customers`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayCustomers(data.customers);
            } else {
                console.error('Error loading customers:', data.error);
            }
        })
        .catch(error => console.error('Fetch error:', error));
}

// Display Customers
function displayCustomers(customers) {
    const customersList = document.getElementById('customersList');
    
    if (customers.length === 0) {
        customersList.innerHTML = '<p class="empty-state">No customers yet. Add one to get started!</p>';
        return;
    }
    
    customersList.innerHTML = customers.map(customer => `
        <div class="customer-item">
            <div class="customer-header">
                <span class="customer-name">👤 ${escapeHtml(customer.name)}</span>
            </div>
            <div class="customer-info">
                <p><strong>📞 Phone:</strong> ${escapeHtml(customer.phone)}</p>
                <p><strong>📧 Email:</strong> ${escapeHtml(customer.email) || 'N/A'}</p>
                <p><strong>📍 Address:</strong> ${escapeHtml(customer.address) || 'N/A'}</p>
                <p style="font-size: 0.8rem; margin-top: 8px; color: #94a3b8;">
                    Registered: ${new Date(customer.created_at).toLocaleDateString()}
                </p>
            </div>
        </div>
    `).join('');
}

// Handle Add Customer
function handleAddCustomer(event) {
    event.preventDefault();
    
    const name = document.getElementById('customerName').value.trim();
    const phone = document.getElementById('customerPhone').value.trim();
    const email = document.getElementById('customerEmail').value.trim();
    const address = document.getElementById('customerAddress').value.trim();
    
    if (!name || !phone) {
        alert('Please fill in all required fields');
        return;
    }
    
    fetch(`${API_BASE}/customers`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, phone, email, address })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Customer added successfully!');
            document.getElementById('addCustomerForm').reset();
            loadCustomers();
            loadDashboard();
        } else {
            alert('❌ Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Error adding customer');
    });
}

// ==================== ORDERS ====================

// Load Orders
function loadOrders() {
    fetch(`${API_BASE}/orders`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayOrders(data.orders);
            } else {
                console.error('Error loading orders:', data.error);
            }
        })
        .catch(error => console.error('Fetch error:', error));
}

// Display Orders
function displayOrders(orders) {
    const ordersList = document.getElementById('ordersList');
    
    if (orders.length === 0) {
        ordersList.innerHTML = '<p class="empty-state">No orders yet. Create one to get started!</p>';
        return;
    }
    
    ordersList.innerHTML = orders.map(order => `
        <div class="order-item">
            <div class="order-header">
                <span class="order-customer">👤 ${escapeHtml(order.customer_name)}</span>
                <span class="order-status ${order.status.toLowerCase()}">${order.status}</span>
            </div>
            <div class="order-details">
                <div class="order-detail">
                    <label>💰 Total Price:</label>
                    <value>$${order.total_price.toFixed(2)}</value>
                </div>
                <div class="order-detail">
                    <label>💳 Payment:</label>
                    <value>${order.payment_method}</value>
                </div>
                <div class="order-detail">
                    <label>📅 Date:</label>
                    <value>${formatDate(order.created_at)}</value>
                </div>
            </div>
            <div style="margin-top: 10px; background: #f8fafc; padding: 10px; border-radius: 6px;">
                <strong>📦 Items:</strong> ${escapeHtml(order.items.join(', '))}
            </div>
            <button class="btn btn-success" onclick="updateOrderStatus('${order._id}', 'Completed')" style="margin-top: 10px;">Mark as Completed</button>
        </div>
    `).join('');
}

// Handle Add Order
function handleAddOrder(event) {
    event.preventDefault();
    
    const customer_name = document.getElementById('orderCustomer').value.trim();
    const itemsText = document.getElementById('orderItems').value.trim();
    const total_price = document.getElementById('orderTotal').value;
    const payment_method = document.getElementById('paymentMethod').value;
    
    if (!customer_name || !itemsText || !total_price) {
        alert('Please fill in all required fields');
        return;
    }
    
    const items = itemsText.split('\n').filter(item => item.trim());
    
    fetch(`${API_BASE}/orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ customer_name, items, total_price, payment_method, status: 'Pending' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Order created successfully!');
            document.getElementById('addOrderForm').reset();
            loadOrders();
            loadDashboard();
        } else {
            alert('❌ Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Error creating order');
    });
}

// Update Order Status
function updateOrderStatus(orderId, status) {
    fetch(`${API_BASE}/orders/${orderId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('✅ Order status updated!');
            loadOrders();
            loadDashboard();
        } else {
            alert('❌ Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Error updating order');
    });
}

// Utility: Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Utility: Format Date
function formatDate(dateString) {
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Auto-refresh data every 30 seconds
setInterval(() => {
    const activeSection = document.querySelector('.section.active');
    if (activeSection) {
        const sectionId = activeSection.id;
        if (sectionId === 'dashboard') {
            loadDashboard();
        } else if (sectionId === 'products') {
            loadProducts();
        } else if (sectionId === 'customers') {
            loadCustomers();
        } else if (sectionId === 'orders') {
            loadOrders();
        }
    }
}, 30000);
