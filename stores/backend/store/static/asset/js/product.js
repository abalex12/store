document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.product-form');

    forms.forEach(form => {
        const decrementBtn = form.querySelector('.decrement');
        const incrementBtn = form.querySelector('.increment');
        const quantityInput = form.querySelector('.quantity-input');
        const submitContainer = form.querySelector('.submit-button-container');

        decrementBtn.addEventListener('click', () => updateQuantity(-1));
        incrementBtn.addEventListener('click', () => updateQuantity(1));

        function updateQuantity(change) {
            let newValue = parseInt(quantityInput.value) + change;
            newValue = Math.max(0, newValue);
            quantityInput.value = newValue;
            submitContainer.style.display = newValue > 0 ? 'block' : 'none';
        }

        quantityInput.addEventListener('input', function() {
            submitContainer.style.display = this.value > 0 ? 'block' : 'none';
        });
    });
});