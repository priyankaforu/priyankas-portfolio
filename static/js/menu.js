document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const mobileMenuItems = document.querySelector('.mobile-menu-items');
    
    menuToggle.addEventListener('click', function(e) {
        e.preventDefault(); // Prevent default button behavior
        mobileMenuItems.classList.toggle('active');
    });
});
