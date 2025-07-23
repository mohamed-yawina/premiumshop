// ==============================================
// FONCTIONS DU PANIER - À UTILISER SUR TOUT LE SITE
// ==============================================

/**
 * Ajoute un produit au panier
 * @param {string} productId - ID du produit
 * @param {string} productName - Nom du produit
 * @param {number} quantity - Quantité à ajouter
 * @param {number} price - Prix unitaire
 * @param {string} [image=''] - URL de l'image (optionnel)
 */
function addToCart(productId, productName, quantity, price, image = '') {
    // Récupérer le panier existant ou en créer un nouveau
    let cart = JSON.parse(localStorage.getItem('panier')) || {};
    
    // Vérifier si le produit existe déjà
    if (cart[productId]) {
        cart[productId].quantity += parseInt(quantity);
    } else {
        cart[productId] = {
            name: productName,
            price: price,
            quantity: parseInt(quantity),
            image: image
        };
    }
    
    // Sauvegarder dans le localStorage
    localStorage.setItem('panier', JSON.stringify(cart));
    
    // Mettre à jour l'affichage
    updateCartDisplay();
    
    // Afficher une notification
    showToast("Produit ajouté au panier", "success");
}

/**
 * Met à jour l'affichage du panier dans toute l'application
 */
function updateCartDisplay() {
    const cart = JSON.parse(localStorage.getItem('panier')) || {};
    const totalItems = Object.values(cart).reduce((sum, item) => sum + item.quantity, 0);
    
    // Mettre à jour le compteur dans le header
    $('.cart-count').text(totalItems);
    
    // Mettre à jour le popover si ouvert
    if ($('#panier').next('.popover').length) {
        refreshCartPopover();
    }
}

/**
 * Rafraîchit le contenu du popover du panier
 */
function refreshCartPopover() {
    $('#panier').popover('dispose').popover({
        html: true,
        content: generateCartHTML(),
        placement: 'bottom',
        trigger: 'focus'
    });
}

/**
 * Génère le HTML pour le popover du panier
 * @returns {string} HTML du panier
 */
function generateCartHTML() {
    const cart = JSON.parse(localStorage.getItem('panier')) || {};
    const items = Object.values(cart);
    const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);
    const totalPrice = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    let html = `
        <div class="cart-popover" style="min-width:280px">
            <div class="cart-header border-bottom pb-2 px-3">
                <h6 class="mb-0 fw-bold">Votre Panier (${totalItems})</h6>
            </div>
            <div class="cart-body p-3">`;
    
    if (items.length === 0) {
        html += '<p class="text-muted my-2">Votre panier est vide</p>';
    } else {
        html += '<ul class="list-unstyled mb-3">';
        
        items.forEach(item => {
            html += `
                <li class="py-2 border-bottom d-flex justify-content-between align-items-center">
                    <div class="d-flex align-items-center">
                        ${item.image ? `<img src="${item.image}" alt="${item.name}" class="me-2" style="width:30px;height:30px;object-fit:cover">` : ''}
                        <span class="text-truncate" style="max-width:150px">${item.name}</span>
                    </div>
                    <div>
                        <span class="badge bg-primary rounded-pill me-2">${item.quantity}</span>
                        <small class="text-muted">${(item.price * item.quantity).toFixed(2)} MAD</small>
                    </div>
                </li>`;
        });
        
        html += `</ul>
            <div class="d-flex justify-content-between align-items-center mb-3">
                <strong>Total:</strong>
                <span class="fw-bold">${totalPrice.toFixed(2)} MAD</span>
            </div>
            <div class="d-grid gap-2">
                <a href="/checkout/" class="btn btn-primary btn-sm py-2">
                    <i class="fas fa-credit-card me-2"></i>Commander
                </a>
                <button class="btn btn-outline-danger btn-sm py-1 empty-cart">
                    <i class="fas fa-trash-alt me-1"></i>Vider le panier
                </button>
            </div>`;
    }
    
    html += `</div></div>`;
    return html;
    
}

/**
 * Vide complètement le panier
 */
function emptyCart() {
    localStorage.removeItem('panier');
    updateCartDisplay();
    showToast("Panier vidé", "info");
}

/**
 * Affiche une notification toast
 * @param {string} message - Message à afficher
 * @param {string} [type='success'] - Type de notification (success, error, warning, info)
 */
function showToast(message, type = 'success') {
    // Supprimer les toasts existants
    $('.toast').remove();
    
    // Icônes selon le type
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-times-circle',
        warning: 'fa-exclamation-circle',
        info: 'fa-info-circle'
    };
    
    // Créer le toast
    const toast = $(`
        <div class="toast show align-items-center text-white bg-${type} border-0"
            style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="fas ${icons[type] || 'fa-info-circle'} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `);
    
    $('body').append(toast);
    setTimeout(() => toast.remove(), 3000);
}

// ==============================================
// INITIALISATION - À EXÉCUTER SUR CHAQUE PAGE
// ==============================================

$(document).ready(function() {
    // Initialiser l'affichage du panier
    updateCartDisplay();
    
    // Configurer le popover du panier
    $('#panier').popover({
        html: true,
        content: generateCartHTML(),
        placement: 'bottom',
        trigger: 'focus'
    });
    
    // Gérer le clic sur "Vider le panier"
    $(document).on('click', '.empty-cart', function(e) {
        e.preventDefault();
        emptyCart();
        refreshCartPopover();
    });
});