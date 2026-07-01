// Inicializar mapa con mejor configuración
const map = L.map('map', {
    center: [6.3389, -75.5627], // Bello, Antioquia
    zoom: 13,
    zoomControl: true,
    scrollWheelZoom: true,
    doubleClickZoom: true,
    boxZoom: true,
    keyboard: true,
    dragging: true,
    touchZoom: true
});

// Agregar capa de mapa con mejor estilo
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    minZoom: 10,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    errorTileUrl: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
}).addTo(map);

// Agregar controles de zoom personalizados
map.zoomControl.setPosition('bottomright');

const markersLayer = L.layerGroup().addTo(map);
let allReports = [];

// Elementos del modal
const modal = document.getElementById('reportModal');
const closeModal = document.getElementById('closeModal');

const modalTitle = document.getElementById('modalTitle');
const modalDate = document.getElementById('modalDate');
const modalSeverity = document.getElementById('modalSeverity');
const modalZone = document.getElementById('modalZone');
const modalTipo = document.getElementById('modalTipo');
const modalDescription = document.getElementById('modalDescription');
const modalInfo = document.getElementById('modalInfo');
const modalInfoContainer = document.getElementById('modalInfoContainer');
const modalImage1 = document.getElementById('modalImage1');
const modalImage2 = document.getElementById('modalImage2');
const modalImage3 = document.getElementById('modalImage3');
const modalImageContainer = document.getElementById('modalImageContainer');
const modalLocation = document.getElementById('modalLocation');
const modalEstado = document.getElementById('modalEstado');

// Colores según gravedad
const severityColors = {
    "leve": "#22c55e",
    "moderado": "#eab308", 
    "severo": "#f97316",
    "critico": "#ef4444"
};

// Iconos mejorados con sombras
const severityIcons = {
    "leve": "🟢",
    "moderado": "🟡", 
    "severo": "🟠",
    "critico": "🔴"
};

// Textos descriptivos
const severityTexts = {
    "leve": "Leve",
    "moderado": "Moderado", 
    "severo": "Severo",
    "critico": "Crítico"
};

const estadoTexts = {
    "pendiente": "⏳ Pendiente",
    "aprobado": "✅ Aprobado", 
    "rechazado": "❌ Rechazado"
};

// Variables globales para filtros
let currentEstadoFilter = 'todos';
let currentGravedadFilter = 'all';

/**
 * Carga los reportes desde la API según el estado filtrado.
 * @param {string} [estadoFiltro='todos'] - El estado de los reportes a cargar ('todos', 'pendiente', 'aprobado', etc.).
 */
async function loadReports(estadoFiltro = 'todos') {
    try {
        showLoadingIndicator(true);
        
        const url = estadoFiltro === 'todos' ? '/api/reportes' : `/api/reportes?estado=${estadoFiltro}`;
        const res = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        });
        
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        const reports = await res.json();
        
        if (reports.error) {
            console.error('Error del servidor:', reports.error);
            showErrorMessage('Error del servidor: ' + reports.error);
            return;
        }
        
        if (!Array.isArray(reports)) {
            console.error('Respuesta inválida del servidor:', reports);
            showErrorMessage('Respuesta inválida del servidor');
            return;
        }
        
        allReports = reports;
        currentEstadoFilter = estadoFiltro;
        
        // Verificar coordenadas válidas
        const validReports = allReports.filter(r => {
            const lat = parseCoordinate(r.lat);
            const lng = parseCoordinate(r.lng);
            return lat !== null && lng !== null;
        });
        
        updateMap(currentGravedadFilter);
        updateStatistics();
        
        if (validReports.length === 0) {
            showInfoMessage('No hay reportes con coordenadas válidas para mostrar en el mapa.');
        }
        
    } catch (err) {
        console.error('❌ Error cargando reportes:', err);
        showErrorMessage('Error al cargar los reportes. Por favor, recarga la página.');
    } finally {
        showLoadingIndicator(false);
    }
}

/**
 * Muestra u oculta el indicador de carga en pantalla.
 * @param {boolean} show - Verdadero para mostrar el indicador, falso para ocultarlo.
 */
function showLoadingIndicator(show) {
    const existing = document.getElementById('loading-indicator');
    if (existing) {
        existing.remove();
    }
    
    if (show) {
        const loader = document.createElement('div');
        loader.id = 'loading-indicator';
        loader.innerHTML = `
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(31, 41, 55, 0.95);
                color: white;
                padding: 20px;
                border-radius: 12px;
                z-index: 10000;
                text-align: center;
                backdrop-filter: blur(10px);
            ">
                <div style="
                    width: 40px;
                    height: 40px;
                    border: 4px solid rgba(108, 92, 231, 0.3);
                    border-top: 4px solid #6c5ce7;
                    border-radius: 50%;
                    animation: spin 1s linear infinite;
                    margin: 0 auto 10px;
                "></div>
                Cargando reportes...
            </div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            </style>
        `;
        document.body.appendChild(loader);
    }
}

/**
 * Muestra un mensaje de error tipo toast.
 * @param {string} message - El mensaje de error a mostrar.
 */
function showErrorMessage(message) {
    showMessage(message, 'error');
}

/**
 * Muestra un mensaje de información tipo toast.
 * @param {string} message - El mensaje informativo a mostrar.
 */
function showInfoMessage(message) {
    showMessage(message, 'info');
}

/**
 * Función base para crear y mostrar mensajes tipo toast animados.
 * @param {string} message - El texto del mensaje.
 * @param {string} [type='info'] - El tipo de mensaje ('error', 'info', 'success').
 */
function showMessage(message, type = 'info') {
    const existing = document.querySelectorAll('.toast-message');
    existing.forEach(el => el.remove());
    
    const colors = {
        error: { bg: '#ef4444', border: '#dc2626' },
        info: { bg: '#3b82f6', border: '#2563eb' },
        success: { bg: '#10b981', border: '#059669' }
    };
    
    const color = colors[type] || colors.info;
    
    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${color.bg};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            border-left: 4px solid ${color.border};
            z-index: 10000;
            max-width: 400px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease;
        ">
            ${message}
        </div>
        <style>
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        </style>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

/**
 * Convierte y valida una coordenada (latitud o longitud) a número.
 * @param {number|string|null} coord - La coordenada a parsear.
 * @returns {number|null} La coordenada como número flotante, o null si es inválida.
 */
function parseCoordinate(coord) {
    // Verificar valores nulos o indefinidos
    if (coord === null || coord === undefined || coord === 'null' || coord === 'undefined' || coord === '') {
        return null;
    }
    
    // Si ya es un número
    if (typeof coord === 'number') {
        return isNaN(coord) || coord === 0 ? null : coord;
    }
    
    // Si es string, intentar convertir
    if (typeof coord === 'string') {
        const parsed = parseFloat(coord.trim());
        return isNaN(parsed) || parsed === 0 ? null : parsed;
    }
    
    return null;
}

/**
 * Crea un marcador personalizado en el mapa para un reporte específico.
 * @param {Object} r - El objeto con los datos del reporte.
 * @returns {L.marker|null} El marcador Leaflet creado, o null si las coordenadas son inválidas.
 */
function createMarker(r) {
    try {
        // Validación de coordenadas
        const lat = parseCoordinate(r.lat);
        const lng = parseCoordinate(r.lng);
        
        if (lat === null || lng === null) {
            return null;
        }

        const color = severityColors[r.gravedad] || "#3b82f6";
        const icon = severityIcons[r.gravedad] || "🔵";
        const severityText = severityTexts[r.gravedad] || r.gravedad;

        // Icono mejorado con animación y mejor accesibilidad
        const customIcon = L.divIcon({
            className: 'custom-marker',
            html: `
                <div class="marker-container" style="
                    position: relative;
                    width: 40px;
                    height: 40px;
                ">
                    <div class="marker-pulse" style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 40px;
                        height: 40px;
                        background: ${color};
                        border-radius: 50%;
                        opacity: 0.3;
                        animation: pulse 2s infinite;
                    "></div>
                    <div class="marker-main" style="
                        position: relative;
                        background: ${color};
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        border: 3px solid white;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 16px;
                        color: white;
                        cursor: pointer;
                        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                        z-index: 1;
                    " onmouseover="this.style.transform='scale(1.2)'; this.style.zIndex='1000'" 
                       onmouseout="this.style.transform='scale(1)'; this.style.zIndex='1'">
                        ${icon}
                    </div>
                </div>
                <style>
                    @keyframes pulse {
                        0% { transform: scale(1); opacity: 0.3; }
                        50% { transform: scale(1.2); opacity: 0.1; }
                        100% { transform: scale(1); opacity: 0.3; }
                    }
                </style>
            `,
            iconSize: [40, 40],
            iconAnchor: [20, 20],
            popupAnchor: [0, -20]
        });

        const marker = L.marker([lat, lng], { 
            icon: customIcon,
            title: `Reporte #${r.id} - ${severityText}`,
            alt: `Marcador del reporte ${r.id}`
        }).addTo(markersLayer);

        // Popup mejorado con mejor diseño
        const popupContent = `
            <div style="min-width: 300px; font-family: 'Inter', Arial, sans-serif; color: #333;">
                <div style="
                    background: linear-gradient(135deg, ${color} 0%, ${adjustColor(color, -20)} 100%); 
                    color: white; 
                    padding: 16px 20px; 
                    border-radius: 12px 12px 0 0; 
                    margin: -16px -16px 16px -16px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 20px;">${icon}</span>
                        <strong style="font-size: 18px; font-weight: 700;">Reporte #${r.id}</strong>
                    </div>
                    <div style="font-size: 14px; opacity: 0.9; margin-top: 4px;">
                        ${severityText} • ${r.fecha_reporte ? new Date(r.fecha_reporte).toLocaleDateString('es-ES') : 'Fecha no disponible'}
                    </div>
                </div>
                
                <div style="padding: 0 4px;">
                    <div style="margin: 12px 0; padding: 12px; background: #f8fafc; border-radius: 8px; border-left: 4px solid ${color};">
                        <div style="display: flex; align-items: flex-start; gap: 8px;">
                            <span style="font-size: 16px; margin-top: 2px;">📍</span>
                            <div>
                                <strong style="color: #374151; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">Ubicación</strong><br>
                                <span style="color: #111827; font-weight: 500;">${r.ubicacion || 'No especificada'}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin: 12px 0;">
                        <div style="padding: 8px; background: #f8fafc; border-radius: 8px; text-align: center;">
                            <div style="color: #6b7280; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Zona</div>
                            <div style="color: #111827; font-weight: 600; font-size: 12px;">${r.zona || "N/A"}</div>
                        </div>
                        <div style="padding: 8px; background: #f8fafc; border-radius: 8px; text-align: center;">
                            <div style="color: #6b7280; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Tipo</div>
                            <div style="color: #111827; font-weight: 600; font-size: 12px;">${r.tipo_anomalia || "N/A"}</div>
                        </div>
                        <div style="padding: 8px; background: #f8fafc; border-radius: 8px; text-align: center;">
                            <div style="color: #6b7280; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">Estado</div>
                            <div style="color: #111827; font-weight: 600; font-size: 12px;">${getEstadoDisplay(r.estado)}</div>
                        </div>
                    </div>
                    
                    ${r.descripcion ? `
                    <div style="margin: 12px 0; padding: 10px; background: #f8fafc; border-radius: 8px;">
                        <div style="color: #6b7280; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">Descripción</div>
                        <div style="color: #374151; font-size: 13px; line-height: 1.4;">${r.descripcion.substring(0, 100)}${r.descripcion.length > 100 ? '...' : ''}</div>
                    </div>
                    ` : ''}
                </div>
                
                <button onclick="openModalFromPopup(${r.id})" style="
                    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                    color: white;
                    border: none;
                    padding: 12px 20px;
                    border-radius: 8px;
                    cursor: pointer;
                    margin-top: 16px;
                    width: 100%;
                    font-size: 14px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
                " onmouseover="this.style.transform='translateY(-1px)'; this.style.boxShadow='0 4px 12px rgba(59, 130, 246, 0.4)'" 
                   onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 8px rgba(59, 130, 246, 0.3)'">
                    <span style="margin-right: 8px;">📋</span>Ver detalles completos
                </button>
            </div>
        `;

        marker.bindPopup(popupContent, {
            maxWidth: 350,
            className: 'custom-popup',
            closeButton: true,
            autoClose: false,
            closeOnEscapeKey: true
        });
        
        marker.reportData = r;
        
        // Tooltip mejorado
        marker.bindTooltip(`
            <div style="text-align: center; font-weight: 600;">
                <div style="font-size: 14px;">Reporte #${r.id}</div>
                <div style="font-size: 12px; opacity: 0.8;">${severityText}</div>
            </div>
        `, {
            permanent: false,
            direction: 'top',
            offset: [0, -25],
            className: 'custom-tooltip'
        });

        return marker;

    } catch (error) {
        console.error('Error creando marcador:', error);
        return null;
    }
}

/**
 * Ajusta el brillo de un color hexadecimal.
 * @param {string} color - El color en formato hexadecimal (ej. "#ffffff").
 * @param {number} amount - La cantidad a ajustar (positivo aclara, negativo oscurece).
 * @returns {string} El nuevo color ajustado en formato hexadecimal.
 */
function adjustColor(color, amount) {
    const usePound = color[0] === "#";
    const col = usePound ? color.slice(1) : color;
    const num = parseInt(col, 16);
    let r = (num >> 16) + amount;
    let g = (num >> 8 & 0x00FF) + amount;
    let b = (num & 0x0000FF) + amount;
    r = r > 255 ? 255 : r < 0 ? 0 : r;
    g = g > 255 ? 255 : g < 0 ? 0 : g;
    b = b > 255 ? 255 : b < 0 ? 0 : b;
    return (usePound ? "#" : "") + (r << 16 | g << 8 | b).toString(16).padStart(6, '0');
}

/**
 * Obtiene el texto y emoji correspondiente para un estado de reporte.
 * @param {string} estado - El estado en formato de código (ej. 'pendiente').
 * @returns {string} El estado formateado para mostrar en la interfaz.
 */
function getEstadoDisplay(estado) {
    const estados = {
        "pendiente": "⏳ Pendiente",
        "aprobado": "✅ Aprobado", 
        "rechazado": "❌ Rechazado",
        "en_proceso": "🔄 En Proceso",
        "completado": "✅ Completado"
    };
    return estados[estado] || estado;
}

/**
 * Abre el modal de detalles buscando el reporte por su ID.
 * Se llama desde los popups de los marcadores del mapa.
 * @param {number} reportId - El ID del reporte a mostrar.
 */
function openModalFromPopup(reportId) {
    const report = allReports.find(r => r.id === reportId);
    if (report) {
        showReportDetails(report);
    }
}

/**
 * Muestra los detalles de un reporte en el modal (ventana emergente).
 * @param {Object} r - El objeto con los datos completos del reporte.
 */
function showReportDetails(r) {
    // Título y fecha
    modalTitle.textContent = `Reporte #${r.id}`;
    
    // Cambiar color del header según la gravedad
    const modalHeader = document.querySelector('.modal-header');
    if (modalHeader) {
        // Remover clases de gravedad anteriores
        modalHeader.classList.remove('leve', 'moderado', 'severo', 'critico');
        
        // Agregar clase según la gravedad actual
        const gravedad = r.gravedad ? r.gravedad.toLowerCase() : 'leve';
        modalHeader.classList.add(gravedad);
        
        // Aplicar colores según la gravedad
        const severityColors = {
            'leve': 'linear-gradient(135deg, #22c55e 0%, #16a34a 100%)',      // Verde
            'moderado': 'linear-gradient(135deg, #eab308 0%, #ca8a04 100%)',  // Amarillo
            'severo': 'linear-gradient(135deg, #f97316 0%, #ea580c 100%)',    // Naranja
            'critico': 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)'    // Rojo
        };
        
        modalHeader.style.background = severityColors[gravedad] || severityColors['leve'];
    }
    
    // Formatear fecha
    if (r.fecha_reporte) {
        const fecha = new Date(r.fecha_reporte);
        const fechaFormateada = fecha.toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        modalDate.textContent = fechaFormateada;
    } else {
        modalDate.textContent = 'Fecha no disponible';
    }
    
    // Información principal
    modalLocation.textContent = r.ubicacion || "Ubicación no especificada";
    modalEstado.innerHTML = getEstadoDisplay(r.estado);
    
    // Información detallada
    modalSeverity.textContent = severityTexts[r.gravedad] || r.gravedad || "No especificada";
    modalZone.textContent = r.zona || "No especificada";
    modalTipo.textContent = r.tipo_anomalia || "No especificado";
    
    // Descripción
    modalDescription.textContent = r.descripcion || "Sin descripción disponible";
    
    // Información adicional (mostrar solo si existe)
    if (r.info_adicional && r.info_adicional.trim()) {
        modalInfo.textContent = r.info_adicional;
        modalInfoContainer.style.display = "block";
    } else {
        modalInfoContainer.style.display = "none";
    }
    
    // Imágenes (mostrar las que existan)
    let hasImages = false;
    
    // Imagen 1
    if (r.image_url && r.imagen) {
        modalImage1.src = r.image_url;
        modalImage1.alt = `Imagen 1 del reporte ${r.id}`;
        modalImage1.style.display = "block";
        hasImages = true;
    } else {
        modalImage1.style.display = "none";
    }
    
    // Imagen 2
    if (r.image_url2 && r.imagen2) {
        modalImage2.src = r.image_url2;
        modalImage2.alt = `Imagen 2 del reporte ${r.id}`;
        modalImage2.style.display = "block";
        hasImages = true;
    } else {
        modalImage2.style.display = "none";
    }
    
    // Imagen 3
    if (r.image_url3 && r.imagen3) {
        modalImage3.src = r.image_url3;
        modalImage3.alt = `Imagen 3 del reporte ${r.id}`;
        modalImage3.style.display = "block";
        hasImages = true;
    } else {
        modalImage3.style.display = "none";
    }
    
    // Mostrar contenedor solo si hay imágenes
    if (hasImages) {
        modalImageContainer.style.display = "block";
    } else {
        modalImageContainer.style.display = "none";
    }

    // Mostrar modal con animación
    modal.style.display = "block";
    
    // Agregar clase para animación si no existe
    if (!modal.classList.contains('show')) {
        modal.classList.add('show');
    }
}

/**
 * Cierra el modal de detalles aplicando una animación de desvanecimiento (fade out).
 */
function closeModalWithAnimation() {
    modal.style.animation = 'fadeOut 0.3s ease';
    setTimeout(() => {
        modal.style.display = "none";
        modal.style.animation = '';
        modal.classList.remove('show');
    }, 300);
}

// Eventos para cerrar modal
if (closeModal) {
    closeModal.onclick = closeModalWithAnimation;
}

window.onclick = (e) => {
    if (e.target == modal) {
        closeModalWithAnimation();
    }
};

// Cerrar modal con tecla Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.style.display === 'block') {
        closeModalWithAnimation();
    }
});

/**
 * Actualiza los marcadores del mapa aplicando un filtro por gravedad.
 * @param {string} filter - El filtro a aplicar ('all', 'leve', 'moderado', 'severo', 'critico').
 */
function updateMap(filter) {
    // Limpiar marcadores existentes
    markersLayer.clearLayers();
    
    let filtered = [];
    
    // Aplicar filtro
    if (filter === "all") {
        filtered = [...allReports];
    } else {
        filtered = allReports.filter(r => r.gravedad === filter);
    }

    // Filtrar reportes con coordenadas válidas
    const validReports = filtered.filter(r => {
        const lat = parseCoordinate(r.lat);
        const lng = parseCoordinate(r.lng);
        return lat !== null && lng !== null;
    });
    
    // Crear marcadores
    const markers = [];
    
    validReports.forEach(report => {
        const marker = createMarker(report);
        if (marker) {
            markers.push(marker);
        }
    });
    
    // Actualizar estadísticas
    updateStatistics();
    
    // Ajustar vista del mapa si hay marcadores
    if (markers.length > 0) {
        try {
            const group = new L.featureGroup(markers);
            const bounds = group.getBounds();
            
            if (bounds.isValid()) {
                map.fitBounds(bounds.pad(0.1), {
                    maxZoom: 16,
                    animate: true,
                    duration: 1
                });
            }
        } catch (error) {
            console.error('Error ajustando vista del mapa:', error);
        }
    } else {
        // Si no hay marcadores, centrar en Bello
        map.setView([6.3389, -75.5627], 13);
        
        if (filtered.length > 0) {
            showInfoMessage(`Se encontraron ${filtered.length} reportes, pero ninguno tiene coordenadas válidas.`);
        } else {
            showInfoMessage(`No se encontraron reportes con el filtro "${filter}".`);
        }
    }
    
    // Actualizar UI del filtro activo
    updateFilterUI(filter);
}

/**
 * Actualiza el estado visual (clases activas) de los botones de filtro.
 * @param {string} activeFilter - El identificador del filtro activo.
 */
function updateFilterUI(activeFilter) {
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        const isActive = btn.dataset.filter === activeFilter;
        btn.classList.toggle('active', isActive);
        
        // Mejorar accesibilidad
        btn.setAttribute('aria-pressed', isActive.toString());
    });
}

/**
 * Recalcula y actualiza los contadores de estadísticas mostrados en pantalla.
 */
function updateStatistics() {
    const criticalCount = allReports.filter(r => r.gravedad === "critico").length;
    const severeCount = allReports.filter(r => r.gravedad === "severo").length;
    const moderateCount = allReports.filter(r => r.gravedad === "moderado").length;
    const leveCount = allReports.filter(r => r.gravedad === "leve").length;
    const totalCount = allReports.length;

    // Actualizar contadores
    document.getElementById("criticalCount").textContent = criticalCount;
    document.getElementById("severeCount").textContent = severeCount;
    document.getElementById("moderateCount").textContent = moderateCount;
    document.getElementById("leveCount").textContent = leveCount;
    document.getElementById("totalCount").textContent = totalCount;
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Configurar botones de filtro por gravedad
    const filterButtons = document.querySelectorAll(".filter-btn[data-type='gravedad']");
    
    // Configurar cada botón de filtro de gravedad
    filterButtons.forEach((btn, index) => {
        // Activar "Todos" por defecto
        if (index === 0) {
            btn.classList.add("active");
            btn.setAttribute('aria-pressed', 'true');
        } else {
            btn.setAttribute('aria-pressed', 'false');
        }
        
        // Mejorar accesibilidad
        btn.setAttribute('role', 'button');
        btn.setAttribute('tabindex', '0');
        
        // Event listener para click
        btn.addEventListener("click", function(e) {
            e.preventDefault();
            
            // Prevenir doble click
            if (this.classList.contains('active')) {
                return;
            }
            
            // Actualizar filtro de gravedad
            const filter = this.dataset.filter;
            currentGravedadFilter = filter;
            updateMap(filter);
            
            // Actualizar UI
            filterButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
        
        // Soporte para teclado
        btn.addEventListener("keydown", function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        // Efectos hover mejorados
        btn.addEventListener("mouseenter", function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        btn.addEventListener("mouseleave", function() {
            this.style.transform = '';
        });
    });
    
    // Configurar botones de filtro por estado (solo para admin)
    const estadoButtons = document.querySelectorAll(".filter-btn-estado");
    
    estadoButtons.forEach((btn, index) => {
        // Activar "Todos" por defecto
        if (index === 0) {
            btn.classList.add("active");
        }
        
        btn.setAttribute('role', 'button');
        btn.setAttribute('tabindex', '0');
        
        btn.addEventListener("click", function(e) {
            e.preventDefault();
            
            if (this.classList.contains('active')) {
                return;
            }
            
            // Actualizar filtro de estado
            const estado = this.dataset.estado;
            currentEstadoFilter = estado;
            
            // Recargar reportes con nuevo filtro
            loadReports(estado);
            
            // Actualizar UI
            estadoButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
        
        btn.addEventListener("keydown", function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        btn.addEventListener("mouseenter", function() {
            if (!this.classList.contains('active')) {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        btn.addEventListener("mouseleave", function() {
            this.style.transform = '';
        });
    });

    // Configurar controles del mapa
    setupMapControls();
    
    // Cargar reportes iniciales
    loadReports();
    
    // Configurar eventos del mapa
    setupMapEvents();
});

// Configurar controles adicionales del mapa
function setupMapControls() {
    // Agregar control de pantalla completa si está disponible
    if (L.Control.Fullscreen) {
        map.addControl(new L.Control.Fullscreen({
            title: {
                'false': 'Ver en pantalla completa',
                'true': 'Salir de pantalla completa'
            }
        }));
    }
    
    // Agregar control de ubicación si está disponible
    if (L.control.locate) {
        L.control.locate({
            position: 'bottomright',
            strings: {
                title: "Mostrar mi ubicación",
                popup: "Estás aquí (precisión: {distance}m)"
            },
            locateOptions: {
                maxZoom: 16
            }
        }).addTo(map);
    }
}

// Configurar eventos del mapa
function setupMapEvents() {
    // Evento cuando el mapa está listo
    map.whenReady(function() {
        // Invalidar tamaño para asegurar renderizado correcto
        setTimeout(() => {
            map.invalidateSize();
        }, 100);
    });
}

// Manejar redimensionamiento de ventana
window.addEventListener('resize', function() {
    clearTimeout(window.resizeTimeout);
    window.resizeTimeout = setTimeout(function() {
        map.invalidateSize();
    }, 250);
});

// Funciones para modal de imagen
function openImageModal(imageSrc) {
    const imageModal = document.getElementById('imageModal');
    const fullImage = document.getElementById('fullImage');
    
    fullImage.src = imageSrc;
    imageModal.style.display = 'block';
    
    // Cerrar con click fuera de la imagen
    imageModal.onclick = function(e) {
        if (e.target === imageModal) {
            closeImageModal();
        }
    };
}

function closeImageModal() {
    const imageModal = document.getElementById('imageModal');
    imageModal.style.display = 'none';
}

// Cerrar modal de imagen con Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const imageModal = document.getElementById('imageModal');
        if (imageModal && imageModal.style.display === 'block') {
            closeImageModal();
        }
    }
});

// Funciones globales
window.openModalFromPopup = openModalFromPopup;
window.filterMarkers = updateMap;
window.openImageModal = openImageModal;
window.closeImageModal = closeImageModal;