from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.login_view, name='login_html'),
    path('login/', views.login_view, name='login_post'),
    path('register_html/', views.register_page, name='register_page'),
    path('register/', views.register, name='register'),
    path('guest_login/', views.guest_login, name='guest_login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('esperando_verificacion/', views.esperando_verificacion, name='esperando_verificacion'),
    path('verificar/<str:timed_token>/', views.verificar_token, name='verificar_token'),
    path('recuperar_contrasena/', views.solicitar_recuperacion, name='solicitar_recuperacion'),
    path('restablecer_contrasena/<str:token>/', views.restablecer_contrasena, name='restablecer_contrasena'),

    # Reports
    path('inicio/', views.inicio_html, name='inicio_html'),
    path('panel_info/', views.panel_info_html, name='panel_info_html'),
    path('reporte/', views.registro_html, name='registro_html'),
    path('registro/', views.registro_reporte, name='registro_reporte'),
    path('mis_reportes/', views.mis_reportes_html, name='mis_reportes_html'),
    path('editar_reporte/<int:reporte_id>/', views.editar_reporte_html, name='editar_reporte_html'),
    path('actualizar_reporte/<int:reporte_id>/', views.actualizar_reporte, name='actualizar_reporte'),
    path('api/reportes/', views.api_reportes, name='api_reportes'),

    # Admin
    path('admin_panel/', views.panel_admin, name='panel_admin'),
    path('panel_tecnico/', views.panel_tecnico, name='panel_tecnico'),
    path('validar/<int:id>/', views.validar, name='validar'),
    path('admin_info/', views.admin_info, name='admin_info'),
    path('usuarios/', views.gestion_usuarios, name='gestion_usuarios'),

    # Visualizations
    path('mapa/', views.mapa_html, name='mapa_html'),
    path('estadisticas/', views.estadisticas_html, name='estadisticas_html'),
    path('api/estadisticas/', views.api_estadisticas, name='api_estadisticas'),
]
