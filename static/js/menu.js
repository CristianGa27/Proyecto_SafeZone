// Funcionalidad del menú hamburger para SafeZone
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    let isMenuOpen = false;
    
    // Función para alternar el menú
    function toggleMenu() {
        isMenuOpen = !isMenuOpen;
        
        if (menuToggle) {
            menuToggle.classList.toggle('active', isMenuOpen);
        }
        
        if (window.innerWidth <= 1024) {
            // Tablet y móvil: mostrar/ocultar sidebar con overlay
            if (sidebar) {
                sidebar.classList.toggle('active', isMenuOpen);
            }
            if (sidebarOverlay) {
                sidebarOverlay.classList.toggle('active', isMenuOpen);
            }
        } else {
            // Desktop: colapsar/expandir sidebar
            if (sidebar) {
                sidebar.classList.toggle('collapsed', isMenuOpen);
            }
            if (mainContent) {
                mainContent.classList.toggle('expanded', isMenuOpen);
            }
        }
        
        // Prevenir scroll del body cuando el menú está abierto en móvil
        if (window.innerWidth <= 768) {
            document.body.style.overflow = isMenuOpen ? 'hidden' : '';
        }
    }
    
    // Función para cerrar el menú
    function closeMenu() {
        if (isMenuOpen) {
            toggleMenu();
        }
    }
    
    // Event listeners
    if (menuToggle) {
        menuToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            toggleMenu();
        });
    }
    
    // Cerrar menú al hacer click en overlay
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function(e) {
            e.preventDefault();
            closeMenu();
        });
    }
    
    // Cerrar menú al hacer click en enlaces en dispositivos móviles
    if (sidebar) {
        const navLinks = sidebar.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 1024) {
                    setTimeout(closeMenu, 150); // Pequeño delay para mejor UX
                }
            });
        });
    }
    
    // Cerrar menú con tecla Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isMenuOpen) {
            closeMenu();
        }
    });
    
    // Manejar cambios de tamaño de ventana
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            const wasOpen = isMenuOpen;
            
            // Limpiar todas las clases
            if (sidebar) {
                sidebar.classList.remove('active', 'collapsed');
            }
            if (sidebarOverlay) {
                sidebarOverlay.classList.remove('active');
            }
            if (mainContent) {
                mainContent.classList.remove('expanded');
            }
            if (menuToggle) {
                menuToggle.classList.remove('active');
            }
            
            // Restaurar overflow del body
            document.body.style.overflow = '';
            
            // Reinicializar estado
            isMenuOpen = false;
            
            // Si el menú estaba abierto, reabrirlo con la nueva lógica
            if (wasOpen) {
                setTimeout(toggleMenu, 100);
            }
        }, 250);
    });
    
    // Inicialización
    function initializeMenu() {
        isMenuOpen = false;
        
        // Limpiar todas las clases al inicio
        if (sidebar) {
            sidebar.classList.remove('active', 'collapsed');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.remove('active');
        }
        if (mainContent) {
            mainContent.classList.remove('expanded');
        }
        if (menuToggle) {
            menuToggle.classList.remove('active');
        }
        
        document.body.style.overflow = '';
    }
    
    // Inicializar al cargar
    initializeMenu();
    
    // Mejorar la accesibilidad
    if (menuToggle) {
        menuToggle.setAttribute('aria-label', 'Alternar menú de navegación');
        menuToggle.setAttribute('aria-expanded', 'false');
        
        // Actualizar aria-expanded cuando cambie el estado
        const originalToggle = toggleMenu;
        toggleMenu = function() {
            originalToggle();
            menuToggle.setAttribute('aria-expanded', isMenuOpen.toString());
        };
    }
});