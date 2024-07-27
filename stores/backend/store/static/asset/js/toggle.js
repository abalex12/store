document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('toggleSidebar');
    const sidebar = document.querySelector('.sidebar');
    const body = document.body;
    const contentWrapper = document.querySelector('.content-wrapper');

    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        body.classList.toggle('sidebar-collapsed');
        
        // Toggle aria-expanded attribute
        const isExpanded = sidebar.classList.contains('collapsed') ? 'false' : 'true';
        sidebarToggle.setAttribute('aria-expanded', isExpanded);

        // Adjust content wrapper margin
        if (body.classList.contains('sidebar-collapsed')) {
            contentWrapper.style.marginLeft = '0';
        } else {
            contentWrapper.style.marginLeft = 'var(--sidebar-width)';
        }
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl)
    })
    toastList.forEach(toast => toast.show())
})