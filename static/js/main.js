// Universal JS functionality
document.addEventListener('DOMContentLoaded', function() {
    // Image preview for add_item.html
    const imageInput = document.getElementById('image');
    const imagePreview = document.getElementById('imagePreview');
    
    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        });
    }
    
    // Search and filter functionality for index.html
    const searchInput = document.getElementById('searchInput');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const itemCards = document.querySelectorAll('.item-card');
    let currentFilter = 'all';
    
    if (searchInput) {
        searchInput.addEventListener('input', performSearchFilter);
    }
    
    if (filterBtns.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                currentFilter = this.dataset.filter;
                filterBtns.forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                performSearchFilter();
            });
        });
    }
    
    function performSearchFilter() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        itemCards.forEach(card => {
            const title = card.dataset.title || '';
            const desc = card.dataset.desc || '';
            const location = card.dataset.location || '';
            const category = card.dataset.category || '';
            
            const matchesSearch = title.includes(searchTerm) || 
                                desc.includes(searchTerm) || 
                                location.includes(searchTerm);
            
            const matchesFilter = currentFilter === 'all' || category === currentFilter;
            
            if (matchesSearch && matchesFilter) {
                card.style.display = 'block';
                card.style.animation = 'slideDown 0.3s ease';
            } else {
                card.style.display = 'none';
            }
        });
    }
    
    // Auto-set today's date for date input
    const dateInput = document.getElementById('date');
    if (dateInput) {
        dateInput.value = new Date().toISOString().split('T')[0];
    }
    
    // Navbar mobile responsiveness (smooth scroll for longer content)
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.background = 'rgba(255, 255, 255, 0.98)';
                navbar.style.boxShadow = '0 4px 30px rgba(0,0,0,0.15)';
            } else {
                navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
            }
        });
    }
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#ff6b6b';
                    valid = false;
                } else {
                    field.style.borderColor = '#e1e5e9';
                }
            });
            
            if (!valid) {
                e.preventDefault();
                alert('Please fill all required fields!');
            }
        });
    });
    
    // Smooth animations for cards
    itemCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});
