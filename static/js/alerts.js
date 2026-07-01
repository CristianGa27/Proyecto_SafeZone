/**
 * SafeZone — Global Alert System
 * Handles Django flash messages with auto-dismiss, animations, and icons.
 */
(function () {
    'use strict';

    /* ── Icons per tag ─────────────────────────────────────── */
    const ICONS = {
        success : '✅',
        error   : '❌',
        warning : '⚠️',
        info    : 'ℹ️',
        debug   : '🔧',
    };

    /**
     * Cierra (oculta) un elemento de alerta con una animación.
     * @param {HTMLElement} el - El elemento de alerta que se va a cerrar.
     */
    function dismissAlert(el) {
        if (!el || el._dismissing) return;
        el._dismissing = true;
        el.style.transition = 'opacity 0.3s ease, transform 0.3s ease, max-height 0.4s ease, margin 0.4s ease, padding 0.4s ease';
        el.style.opacity    = '0';
        el.style.transform  = 'translateY(-8px) scale(0.97)';
        el.style.maxHeight  = '0';
        el.style.marginBottom = '0';
        el.style.paddingTop   = '0';
        el.style.paddingBottom = '0';
        setTimeout(() => el.remove(), 420);
    }

    /**
     * Inyecta los estilos CSS globales para las alertas en el documento si aún no están presentes.
     */
    function injectStyles() {
        if (document.getElementById('sz-alert-styles')) return;
        const style = document.createElement('style');
        style.id = 'sz-alert-styles';
        style.textContent = `
            /* SafeZone Alert Container */
            .sz-alert-container {
                position: fixed;
                top: 1.25rem;
                right: 1.25rem;
                z-index: 99999;
                display: flex;
                flex-direction: column;
                gap: 0.6rem;
                max-width: min(400px, calc(100vw - 2.5rem));
                pointer-events: none;
            }

            /* Individual alert */
            .sz-alert {
                display: flex;
                align-items: flex-start;
                gap: 0.75rem;
                padding: 0.95rem 1.1rem;
                border-radius: 14px;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 0.9rem;
                font-weight: 500;
                line-height: 1.45;
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.35), 0 2px 8px rgba(0,0,0,0.2);
                border: 1px solid transparent;
                max-height: 200px;
                overflow: hidden;
                pointer-events: all;
                cursor: default;
                animation: szAlertIn 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) both;
                position: relative;
            }

            @keyframes szAlertIn {
                from { opacity: 0; transform: translateX(24px) scale(0.92); }
                to   { opacity: 1; transform: translateX(0)      scale(1);   }
            }

            /* Type variants */
            .sz-alert-success {
                background: rgba(16, 185, 129, 0.15);
                border-color: rgba(16, 185, 129, 0.3);
                color: #6ee7b7;
            }
            .sz-alert-error {
                background: rgba(239, 68, 68, 0.15);
                border-color: rgba(239, 68, 68, 0.3);
                color: #fca5a5;
            }
            .sz-alert-warning {
                background: rgba(245, 158, 11, 0.15);
                border-color: rgba(245, 158, 11, 0.3);
                color: #fcd34d;
            }
            .sz-alert-info, .sz-alert-debug {
                background: rgba(99, 102, 241, 0.15);
                border-color: rgba(99, 102, 241, 0.3);
                color: #a5b4fc;
            }

            .sz-alert-icon {
                font-size: 1.1rem;
                flex-shrink: 0;
                margin-top: 0.05rem;
            }

            .sz-alert-body { flex: 1; }
            .sz-alert-title {
                font-weight: 700;
                font-size: 0.78rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                opacity: 0.75;
                margin-bottom: 0.2rem;
            }
            .sz-alert-text { opacity: 0.95; }

            .sz-alert-close {
                background: none;
                border: none;
                cursor: pointer;
                color: inherit;
                opacity: 0.5;
                font-size: 1rem;
                padding: 0;
                line-height: 1;
                flex-shrink: 0;
                transition: opacity 0.2s;
                margin-left: 0.25rem;
            }
            .sz-alert-close:hover { opacity: 1; }

            /* Progress bar */
            .sz-alert-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                border-radius: 0 0 14px 14px;
                animation: szProgress linear forwards;
                opacity: 0.6;
            }
            .sz-alert-success .sz-alert-progress { background: #10b981; }
            .sz-alert-error   .sz-alert-progress { background: #ef4444; }
            .sz-alert-warning .sz-alert-progress { background: #f59e0b; }
            .sz-alert-info    .sz-alert-progress,
            .sz-alert-debug   .sz-alert-progress { background: #6366f1; }

            @keyframes szProgress {
                from { width: 100%; }
                to   { width: 0%; }
            }

            /* Inline (legacy) flash messages — hide them, we replace with toasts */
            .flash-messages { display: none !important; }

            @media (max-width: 480px) {
                .sz-alert-container {
                    top: auto;
                    bottom: 1rem;
                    right: 0.75rem;
                    left: 0.75rem;
                    max-width: none;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Obtiene o crea el contenedor principal para las alertas.
     * @returns {HTMLElement} El elemento contenedor de alertas.
     */
    function getContainer() {
        let c = document.getElementById('sz-alert-container');
        if (!c) {
            c = document.createElement('div');
            c.id = 'sz-alert-container';
            c.className = 'sz-alert-container';
            document.body.appendChild(c);
        }
        return c;
    }

    /* ── Title map ─────────────────────────────────────────── */
    const TITLES = {
        success : 'Éxito',
        error   : 'Error',
        warning : 'Advertencia',
        info    : 'Información',
        debug   : 'Debug',
    };

    /**
     * Muestra una alerta (toast) de forma programática.
     * @param {string} message - El mensaje a mostrar en la alerta.
     * @param {string} [type='info'] - El tipo de alerta ('success', 'error', 'warning', 'info', 'debug').
     * @param {number} [duration=5000] - La duración en milisegundos antes de que la alerta se cierre automáticamente (0 para no cerrar).
     * @returns {HTMLElement} El elemento de alerta creado.
     */
    window.SafeZoneAlert = function (message, type, duration) {
        type     = type     || 'info';
        duration = duration !== undefined ? duration : 5000;

        injectStyles();
        const container = getContainer();

        const el = document.createElement('div');
        el.className = `sz-alert sz-alert-${type}`;

        const icon  = ICONS[type]  || 'ℹ️';
        const title = TITLES[type] || 'Aviso';

        el.innerHTML = `
            <span class="sz-alert-icon">${icon}</span>
            <div class="sz-alert-body">
                <div class="sz-alert-title">${title}</div>
                <div class="sz-alert-text">${message}</div>
            </div>
            <button class="sz-alert-close" aria-label="Cerrar">✕</button>
            ${duration > 0 ? `<div class="sz-alert-progress" style="animation-duration:${duration}ms"></div>` : ''}
        `;

        el.querySelector('.sz-alert-close').addEventListener('click', () => dismissAlert(el));
        container.appendChild(el);

        if (duration > 0) setTimeout(() => dismissAlert(el), duration);
        return el;
    };

    /**
     * Convierte los mensajes flash de Django (ocultos por CSS) en alertas toast.
     */
    function convertInlineMessages() {
        document.querySelectorAll('.flash-messages .flash-message, .flash-messages p').forEach(msg => {
            const text = msg.textContent.trim();
            if (!text) return;

            /* Determine type from class */
            let type = 'info';
            const cls = msg.className || '';
            if (cls.includes('success'))  type = 'success';
            else if (cls.includes('error'))   type = 'error';
            else if (cls.includes('warning')) type = 'warning';
            else if (cls.includes('debug'))   type = 'debug';

            /* Clean emoji prefix that some templates add */
            const cleaned = text.replace(/^[✅❌⚠️ℹ️🔧]\s*/, '');

            window.SafeZoneAlert(cleaned, type, type === 'error' ? 8000 : 5000);
        });
    }

    /**
     * Inicializa el sistema de alertas inyectando los estilos y convirtiendo los mensajes en línea.
     */
    function init() {
        injectStyles();
        convertInlineMessages();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
