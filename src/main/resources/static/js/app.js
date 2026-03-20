// Pet Paradise - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('Pet Paradise store loaded');
    
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Cart functionality
    const cartButtons = document.querySelectorAll('.add-to-cart');
    if (cartButtons.length > 0) {
        cartButtons.forEach(button => {
            button.addEventListener('click', function() {
                const productName = this.getAttribute('data-product');
                const productPrice = this.getAttribute('data-price');
                
                addToCart(productName, productPrice);
            });
        });
    }
    
    // Contact form submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const name = formData.get('name') || 'User';
            
            // In a real app, this would be an AJAX call to the backend
            alert(`Thank you for your message, ${name}! We will get back to you within 24 hours.`);
            this.reset();
            
            // Show success message
            showNotification('Message sent successfully!', 'success');
        });
    }
    
    // Load pets from API
    loadPets();
    
    // Initialize cart count
    updateCartCount();
});

// Cart functions
let cartItems = [];

function addToCart(productName, price) {
    const item = {
        name: productName,
        price: parseFloat(price),
        quantity: 1,
        id: Date.now()
    };
    
    // Check if item already in cart
    const existingItem = cartItems.find(item => item.name === productName);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cartItems.push(item);
    }
    
    updateCartCount();
    showNotification(`${productName} added to cart!`, 'success');
    
    // Save to localStorage
    saveCart();
}

function updateCartCount() {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        const totalItems = cartItems.reduce((total, item) => total + item.quantity, 0);
        cartCountElement.textContent = totalItems;
    }
}

function saveCart() {
    localStorage.setItem('petParadiseCart', JSON.stringify(cartItems));
}

function loadCart() {
    const savedCart = localStorage.getItem('petParadiseCart');
    if (savedCart) {
        cartItems = JSON.parse(savedCart);
        updateCartCount();
    }
}

// API functions
async function loadPets() {
    try {
        const response = await fetch('/api/pets');
        const data = await response.json();
        
        // In a real implementation, this would populate the pets section
        console.log('Pets API response:', data);
        
        // Simulate pet data for demo
        const mockPets = [
            { id: 1, name: 'Golden Retriever', type: 'dog', price: 800, image: 'https://images.unsplash.com/photo-1552053831-71594a27632d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80' },
            { id: 2, name: 'Persian Cat', type: 'cat', price: 600, image: 'https://images.unsplash.com/photo-1513360371669-4adf3dd7dff8?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80' },
            { id: 3, name: 'African Grey Parrot', type: 'bird', price: 1200, image: 'https://images.unsplash.com/photo-1591946614720-90a587da4a36?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80' },
            { id: 4, name: 'Holland Lop Rabbit', type: 'rabbit', price: 150, image: 'https://images.unsplash.com/photo-1559253664-ca249d4608c6?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80' }
        ];
        
        // Could use this data to dynamically populate the page
        return mockPets;
    } catch (error) {
        console.error('Error loading pets:', error);
        return [];
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

// Search functionality
function searchPets(query) {
    console.log('Searching for:', query);
    // In a real app, this would filter or fetch from API
    showNotification(`Searching for "${query}"...`, 'info');
}

// Newsletter subscription
function subscribeNewsletter(email) {
    if (!email || !email.includes('@')) {
        showNotification('Please enter a valid email address', 'warning');
        return false;
    }
    
    // Simulate API call
    setTimeout(() => {
        showNotification(`Thank you for subscribing with ${email}!`, 'success');
    }, 500);
    
    return true;
}

// Load cart from localStorage on page load
document.addEventListener('DOMContentLoaded', loadCart);