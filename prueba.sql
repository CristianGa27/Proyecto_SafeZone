-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 24-06-2026 a las 21:35:12
-- Versión del servidor: 12.2.2-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `prueba`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add Configuración del sistema', 7, 'add_configuracionsistema'),
(26, 'Can change Configuración del sistema', 7, 'change_configuracionsistema'),
(27, 'Can delete Configuración del sistema', 7, 'delete_configuracionsistema'),
(28, 'Can view Configuración del sistema', 7, 'view_configuracionsistema'),
(29, 'Can add Historial de reporte', 8, 'add_historialreporte'),
(30, 'Can change Historial de reporte', 8, 'change_historialreporte'),
(31, 'Can delete Historial de reporte', 8, 'delete_historialreporte'),
(32, 'Can view Historial de reporte', 8, 'view_historialreporte'),
(33, 'Can add Reporte', 9, 'add_reportes'),
(34, 'Can change Reporte', 9, 'change_reportes'),
(35, 'Can delete Reporte', 9, 'delete_reportes'),
(36, 'Can view Reporte', 9, 'view_reportes'),
(37, 'Can add Rol', 10, 'add_roles'),
(38, 'Can change Rol', 10, 'change_roles'),
(39, 'Can delete Rol', 10, 'delete_roles'),
(40, 'Can view Rol', 10, 'view_roles'),
(41, 'Can add Tipo de anomalía', 11, 'add_tiposanomalia'),
(42, 'Can change Tipo de anomalía', 11, 'change_tiposanomalia'),
(43, 'Can delete Tipo de anomalía', 11, 'delete_tiposanomalia'),
(44, 'Can view Tipo de anomalía', 11, 'view_tiposanomalia'),
(45, 'Can add Usuario', 12, 'add_usuarios'),
(46, 'Can change Usuario', 12, 'change_usuarios'),
(47, 'Can delete Usuario', 12, 'delete_usuarios'),
(48, 'Can view Usuario', 12, 'view_usuarios'),
(49, 'Can add zonas', 13, 'add_zonas'),
(50, 'Can change zonas', 13, 'change_zonas'),
(51, 'Can delete zonas', 13, 'delete_zonas'),
(52, 'Can view zonas', 13, 'view_zonas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracionsistema`
--

CREATE TABLE `configuracionsistema` (
  `id` int(11) NOT NULL,
  `clave` varchar(100) NOT NULL,
  `valor` text NOT NULL,
  `descripcion` text DEFAULT NULL,
  `tipo` enum('string','number','boolean','json') DEFAULT 'string',
  `fecha_actualizacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `configuracionsistema`
--

INSERT INTO `configuracionsistema` (`id`, `clave`, `valor`, `descripcion`, `tipo`, `fecha_actualizacion`) VALUES
(1, 'sistema_nombre', 'SafeZone', 'Nombre del sistema', 'string', '2025-12-15 04:41:39'),
(2, 'sistema_version', '2.0.0', 'Versión actual del sistema', 'string', '2025-12-15 01:29:33'),
(3, 'reportes_por_pagina', '10', 'Número de reportes por página', 'number', '2025-12-15 01:29:33'),
(4, 'max_imagenes_reporte', '3', 'Máximo número de imágenes por reporte', 'number', '2025-12-15 01:29:33'),
(5, 'auto_aprobar_reportes', 'false', 'Aprobar reportes automáticamente', 'boolean', '2025-12-15 01:29:33'),
(6, 'coordenadas_centro', '{\"lat\": 6.3372, \"lng\": -75.5625}', 'Coordenadas del centro del mapa (Bello, Antioquia)', 'json', '2025-12-15 01:29:33'),
(7, 'colores_gravedad', '{\"leve\": \"#22c55e\", \"moderado\": \"#eab308\", \"severo\": \"#f97316\", \"critico\": \"#ef4444\"}', 'Colores para niveles de gravedad', 'json', '2025-12-15 01:29:33'),
(8, 'estados_permitidos', '[\"pendiente\", \"aprobado\", \"en_proceso\", \"resuelto\", \"rechazado\"]', 'Estados permitidos para reportes', 'json', '2025-12-15 01:29:33');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(7, 'safezone_app', 'configuracionsistema'),
(8, 'safezone_app', 'historialreporte'),
(9, 'safezone_app', 'reportes'),
(10, 'safezone_app', 'roles'),
(11, 'safezone_app', 'tiposanomalia'),
(12, 'safezone_app', 'usuarios'),
(13, 'safezone_app', 'zonas'),
(6, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-05-12 23:20:57.977979'),
(2, 'auth', '0001_initial', '2026-05-12 23:20:58.211398'),
(3, 'admin', '0001_initial', '2026-05-12 23:20:58.266231'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-05-12 23:20:58.273838'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-05-12 23:20:58.281377'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-05-12 23:20:58.324545'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-05-12 23:20:58.353768'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-05-12 23:20:58.372581'),
(9, 'auth', '0004_alter_user_username_opts', '2026-05-12 23:20:58.380538'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-05-12 23:20:58.405385'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-05-12 23:20:58.407124'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-05-12 23:20:58.416685'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-05-12 23:20:58.434256'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-05-12 23:20:58.452173'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-05-12 23:20:58.469159'),
(16, 'auth', '0011_update_proxy_permissions', '2026-05-12 23:20:58.478667'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-05-12 23:20:58.496379'),
(18, 'sessions', '0001_initial', '2026-05-12 23:20:58.512281'),
(19, 'safezone_app', '0001_initial', '2026-06-03 14:39:00.569483'),
(20, 'safezone_app', '0002_alter_configuracionsistema_options_and_more', '2026-06-03 14:39:00.580623');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('2b3kcwsu45s0mj6w0g98pz3lf7dibldv', '.eJyrViotTi2Kz0xRsjI31wFz8hJzU5WslJyLMotLMhPzFJwTczNz8hXcE4uSMxMVAhJLMmNKDQzSDPOVdJTS8kvy4wtSi9Iyc5Ss8kpzciBGxBfl54DMALGVagHBXCKX:1wZrXJ:02RUtkI3OaDZUuhDJhrVYw7Nrwxy3DnRHn8yCJLB7mA', '2026-07-01 14:46:37.096951'),
('eraw68ch9sxivfebwm766d3pizy121g3', '.eJyrViotTi2Kz0xRsjIz0wFz8hJzU5WslJyLMotLMhPzFJwTczNz8hXcE4uSMxMVAhJLMmNKDQzSDPOVIOrji_JzQBpAbKBQWn5JfnxBalFaZo6SVV5pTk4tALcYIpU:1wXL99:s58k7lEGGnzVXaKpO5N7S_MoDa9mOU-kdbc1Eu-pX_M', '2026-06-24 15:47:15.042251'),
('ydv5xtijqxw9zv1lhdk1hhxae0nujysm', '.eJyrViotTi2Kz0xRsjI31wFz8hJzU5WslJyLMotLMhPzFJwTczNz8hXcE4uSMxMVAhJLMmNKDQzSDPOVdJTS8kvy4wtSi9Iyc5Ss8kpzciBGxBfl54DMALGVagHBXCKX:1wcRRI:0gLMzoAvjIGLDCroHWesFwrso2yV3GwVLr_Byf7Jdkk', '2026-07-08 17:31:04.817996');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historialreporte`
--

CREATE TABLE `historialreporte` (
  `id` int(11) NOT NULL,
  `reporte_id` int(11) NOT NULL,
  `usuario_admin_id` int(11) DEFAULT NULL,
  `estado_anterior` enum('nuevo','pendiente','asignado','en_progreso','resuelto','cerrado','rechazado') DEFAULT NULL,
  `estado_nuevo` enum('nuevo','pendiente','asignado','en_progreso','resuelto','cerrado','rechazado') NOT NULL,
  `observaciones` text DEFAULT NULL,
  `fecha_cambio` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes`
--

CREATE TABLE `reportes` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `id_tipo_anomalia` int(11) NOT NULL,
  `barrio` varchar(100) NOT NULL,
  `ubicacion` varchar(500) NOT NULL,
  `gravedad` enum('leve','moderado','severo','critico') NOT NULL,
  `descripcion` text NOT NULL,
  `info_adicional` text DEFAULT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `imagen2` varchar(255) DEFAULT NULL,
  `imagen3` varchar(255) DEFAULT NULL,
  `latitud` decimal(10,8) DEFAULT NULL,
  `longitud` decimal(11,8) DEFAULT NULL,
  `estado` enum('nuevo','pendiente','asignado','en_progreso','resuelto','cerrado','rechazado') DEFAULT 'nuevo',
  `observaciones` text DEFAULT NULL,
  `fecha_reporte` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_actualizacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `reportes`
--

INSERT INTO `reportes` (`id`, `usuario_id`, `id_tipo_anomalia`, `barrio`, `ubicacion`, `gravedad`, `descripcion`, `info_adicional`, `imagen`, `imagen2`, `imagen3`, `latitud`, `longitud`, `estado`, `observaciones`, `fecha_reporte`, `fecha_actualizacion`) VALUES
(1, NULL, 1, 'el rosario', 'Carrera 58 #50-24', 'critico', 'fefwfwefwe', 'fwefwefwefwe', 'be924c8a9173d91a_2025_Acer_Consumer_Default_3840x2400.jpg', '0f6cfe262417a94c_2025_Acer_Consumer_Option_3840x2400.jpg', NULL, 6.32980000, -75.55730000, 'cerrado', 'Estado cambiado a cerrado', '2026-03-04 12:13:55', '2026-03-04 12:35:54'),
(2, NULL, 1, 'el rosario', 'Carrera 58 #50-24', 'moderado', 'fedgfwfwe', 'fwefwe', 'bce2dd194ceed0a6_2025_Acer_Consumer_Default_3840x2400.jpg', '427b8331dc225b70_2025_Acer_Consumer_Option_3840x2400.jpg', NULL, 6.32980000, -75.55730000, 'cerrado', 'Estado cambiado a cerrado', '2026-03-04 12:37:40', '2026-03-11 14:25:51'),
(3, NULL, 1, 'la florida', 'Carrera 58 #50-22', 'moderado', 'fdasdfsdff', 'dasdfasda', 'e541ed372da96397_2025_Acer_Consumer_Default_3840x2400.jpg', 'e7f1de9a939fd2e6_2025_Acer_Consumer_Option_3840x2400.jpg', NULL, 6.33700000, -75.55200000, 'rechazado', '', '2026-03-04 12:38:46', '2026-03-04 12:43:30'),
(4, NULL, 1, 'niquía bifamiliares', 'Av. 43 #57-07', 'critico', 'fsdfsdf', 'fsdfsdfsdf', 'b5b7e5aa24db1445_2025_Acer_Consumer_Default_3840x2400.jpg', 'b7d63d279200a96c_2025_Acer_Consumer_Option_3840x2400.jpg', NULL, 6.34300000, -75.54500000, 'cerrado', 'Estado cambiado a cerrado', '2026-03-04 12:41:13', '2026-03-04 12:45:33'),
(5, NULL, 1, 'altos de niquía', 'Carrera 58 #50-22', 'critico', 'dwfwrf', 'efwfe', '76a9c0e286be3396_2025_Acer_Consumer_Default_3840x2400.jpg', 'f03c949f77a3f8b1_2025_Acer_Consumer_Option_3840x2400.jpg', NULL, 6.34500000, -75.54300000, 'cerrado', 'Estado cambiado a cerrado', '2026-03-18 23:21:08', '2026-05-04 12:06:36'),
(6, NULL, 2, 'róterdam', 'Carrera 58 #50-22', 'critico', 'fqwfewfwe', '', NULL, NULL, NULL, 6.33720000, -75.56250000, 'nuevo', NULL, '2026-03-25 03:26:29', '2026-03-25 03:26:29'),
(7, NULL, 2, 'alcalá', 'tg5gt5', 'severo', 'vtgvt', 'vtgvtg', NULL, NULL, NULL, 6.33550000, -75.55150000, 'nuevo', NULL, '2026-04-08 12:20:42', '2026-04-08 12:20:42'),
(8, NULL, 1, 'panamericano', 'Carrera 58 #50-24', 'severo', '5hg6hr\r\n', 'g6gy6gy6', NULL, NULL, NULL, 6.33900000, -75.54900000, 'nuevo', NULL, '2026-04-08 12:21:24', '2026-04-08 12:21:24'),
(9, NULL, 1, 'aralias', 'Av. 43 #57-07', 'leve', 'dfwerwef', 'wefwefwef', 'd2c4b597334b88b3_WhatsApp Image 2026-04-27 at 5.18.37 PM (2).jpeg', '3a999d5e4e99c9b3_WhatsApp Image 2026-04-27 at 5.18.37 PM (1).jpeg', '3c98d89a5a7b3677_WhatsApp Image 2026-04-27 at 5.18.37 PM.jpeg', 6.33720000, -75.56250000, 'cerrado', 'Estado cambiado a cerrado', '2026-05-12 23:42:54', '2026-05-12 23:54:19'),
(10, NULL, 1, 'guasimalito', 'Crerra 58 #50-33', 'leve', 'sfefwefew', 'dvfwevwe', '86bb9a24dec06e9c_WhatsApp Image 2026-04-27 at 5.18.38 PM.jpeg', '46ef1f8ca9965c26_WhatsApp Image 2026-04-27 at 5.18.37 PM (2).jpeg', '57cf940973d7a152_WhatsApp Image 2026-04-27 at 5.18.37 PM (1).jpeg', 6.34350000, -75.54550000, 'cerrado', 'Estado cambiado a cerrado', '2026-05-12 23:43:30', '2026-05-12 23:54:18'),
(11, 77, 2, 'la navarra', 'Carrera 58 #50-22', 'moderado', 'rfergeg', 'rgegre', 'da49da474c9a4f1f9da415f244dcd2d4_Captura de pantalla 2026-06-23 152550.png', 'cb9826542e8f4a6b895c996db6794c1c_Captura de pantalla 2026-06-23 151440.png', 'e37d5f5a33874be5a7d8181551ee12ef_Captura de pantalla 2026-06-23 134652.png', 6.34550000, -75.54350000, 'nuevo', NULL, '2026-06-24 17:22:55', '2026-06-24 17:22:55'),
(12, 77, 1, 'el trébol', 'Ubicación en mapa (6.3341, -75.5646)', 'critico', 'cv vc vcvc', 'v vc vc vcvfvefd', 'f5cc2e17414440bda685886b2a6345aa_Captura de pantalla 2025-06-17 063619.png', 'c50871c433f14911856be512d10d9d65_Captura de pantalla 2025-06-17 063628.png', 'b6d9d17a98ca4338853a360b1954ef9f_Captura de pantalla 2025-06-17 065039.png', 6.33413514, -75.56463857, 'nuevo', NULL, '2026-06-24 18:01:10', '2026-06-24 18:01:10'),
(13, 77, 2, 'altos de niquía', 'Ubicación en mapa (6.3454, -75.5546)', 'leve', 'cvcbgbgf', 'vdfvdfvfd', 'c5768f22392c4938928afe64643163cf_Captura de pantalla 2025-06-17 063628.png', '016e323245d341c8b4d82781e5c64604_Captura de pantalla 2025-06-17 065039.png', 'ba8519aeb71649dd9166fe81b4a3b96f_Captura de pantalla 2025-06-24 114730.png', 6.34537898, -75.55460954, 'nuevo', NULL, '2026-06-24 18:03:59', '2026-06-24 18:03:59'),
(14, 77, 1, 'el rosario', 'Ubicación en mapa (6.3341, -75.5641)', 'leve', 'vfdbdbb', 'dfbdbdfbfd', '66b764f37c2d4025a0a9a20fc529cd67_Captura de pantalla 2025-06-17 063619.png', 'f658bc4b0e834501937a2515b64d7969_Captura de pantalla 2025-06-17 063628.png', 'b8d7797eb9264ae98b78d3dca274ee97_Captura de pantalla 2025-06-17 065039.png', 6.33412234, -75.56410472, 'nuevo', NULL, '2026-06-24 18:09:50', '2026-06-24 18:09:50');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `nombre_rol` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id`, `nombre_rol`, `descripcion`, `fecha_creacion`) VALUES
(2, 'usuario', 'Usuario registrado que puede crear y gestionar sus propios reportes', '2025-12-15 01:29:32'),
(3, 'invitado', 'Usuario temporal sin registro que puede crear reportes básicos', '2025-12-15 01:29:32'),
(4, 'admin_principal', 'Administrador principal - Aprueba/rechaza reportes', '2025-12-15 01:51:55'),
(5, 'admin_tecnico', 'Administrador técnico - Gestiona flujo de trabajo de reportes aprobados', '2025-12-15 01:51:55'),
(6, 'moderador', 'Moderador - Gestiona cuentas de usuarios', '2026-03-25 03:40:36');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tiposanomalia`
--

CREATE TABLE `tiposanomalia` (
  `id` int(11) NOT NULL,
  `nombre_anomalia` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `tiposanomalia`
--

INSERT INTO `tiposanomalia` (`id`, `nombre_anomalia`, `descripcion`, `activo`, `fecha_creacion`) VALUES
(1, 'Bache', 'Hoyo o depresión en la superficie del pavimento que afecta el tránsito vehicular', 1, '2025-12-15 01:29:32'),
(2, 'Vía Dañada', 'Deterioro general del pavimento incluyendo grietas, hundimientos y desgaste del asfalto', 1, '2025-12-15 04:33:26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre_usuario` varchar(100) NOT NULL,
  `correo_electronico` varchar(150) NOT NULL,
  `contrasena_hash` varchar(255) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `codigo_verificacion` varchar(36) DEFAULT NULL,
  `verificado` tinyint(1) DEFAULT 0,
  `id_rol` int(11) NOT NULL DEFAULT 2,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `ultimo_acceso` timestamp NULL DEFAULT NULL,
  `direccion_residencia` varchar(200) DEFAULT NULL,
  `numero_documento` varchar(50) DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL,
  `estado_cuenta` enum('activo','inactivo','pendiente','bloqueado') DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre_usuario`, `correo_electronico`, `contrasena_hash`, `telefono`, `codigo_verificacion`, `verificado`, `id_rol`, `activo`, `fecha_registro`, `ultimo_acceso`, `direccion_residencia`, `numero_documento`, `foto_perfil`, `estado_cuenta`) VALUES
(3, 'Invitado Sistema', 'guest@safezone.com', 'NO_PASSWORD_NEEDED', NULL, NULL, 0, 3, 1, '2025-12-15 01:29:33', NULL, NULL, NULL, NULL, 'activo'),
(4, 'Usuario Demo', 'usuario@safezone.com', '$2b$12$hDUn4gxbzghBnPdZIBSFk.ACONih0mVzRKhfFZx4bRtqy2uXru7Nq', NULL, NULL, 0, 2, 1, '2025-12-15 01:31:18', NULL, NULL, NULL, NULL, 'activo'),
(19, 'Admin Principal', 'admin@safezone.com', '$2b$12$9JIuZbX3gxaD.R/Fw04G5u4n97jR6WqyWwLkdc5iSRghQxD8wg77u', NULL, NULL, 1, 4, 1, '2025-12-15 23:10:39', NULL, NULL, NULL, NULL, 'activo'),
(20, 'Admin Técnico', 'tecnico@safezone.com', '$2b$12$ychycySTxao9uGh4pxJPJuAJq4Zf3S3avQaOF4v.nBrbBidSQAqt2', NULL, NULL, 1, 5, 1, '2025-12-15 23:10:56', NULL, NULL, NULL, NULL, 'activo'),
(77, 'Cristian Camilo Garcia Patiño', 'criscagarpa@gmail.com', '$2b$12$C3U19iJ5HL6NFKyIMCk/bucxW2l1IPWB8Tl2VK6LEIQzFUKKbZ.lG', '3045204947', NULL, 1, 2, 1, '2026-06-17 14:37:19', NULL, 'Avenida Boyacá #54-24', '1018232092', NULL, NULL),
(78, 'hector maya', 'maya@gamail.com', '$2b$12$WeOwWZljycRaLx2VJ9G3tOSkQijyEjh.n5tCSJmYuJiHFKCbMP3SC', '2019874833', 'b6fd7fa7-5bab-431a-9285-65aa19343bfd', 0, 2, 1, '2026-06-17 14:45:09', NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `zonas`
--

CREATE TABLE `zonas` (
  `id` int(11) NOT NULL,
  `nombre_zona` varchar(100) NOT NULL,
  `zona_geografica` enum('norte','nororiente','centro-norte','centro','centro-sur','sur','occidente','urbanizacion','popular','industrial','corregimiento') NOT NULL,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `zonas`
--

INSERT INTO `zonas` (`id`, `nombre_zona`, `zona_geografica`, `activo`, `fecha_creacion`) VALUES
(1, 'niquía bifamiliares', 'norte', 1, '2025-12-15 01:29:33'),
(2, 'altos de niquía', 'norte', 1, '2025-12-15 01:29:33'),
(3, 'ciudad niquía', 'norte', 1, '2025-12-15 01:29:33'),
(4, 'panamericano', 'norte', 1, '2025-12-15 01:29:33'),
(5, 'ciudadela del norte', 'norte', 1, '2025-12-15 01:29:33'),
(6, 'alpes del norte', 'norte', 1, '2025-12-15 01:29:33'),
(7, 'norteamérica', 'norte', 1, '2025-12-15 01:29:33'),
(8, 'róterdam', 'norte', 1, '2025-12-15 01:29:33'),
(9, 'altos de quitasol', 'norte', 1, '2025-12-15 01:29:33'),
(10, 'la navarra', 'norte', 1, '2025-12-15 01:29:33'),
(11, 'el trébol', 'norte', 1, '2025-12-15 01:29:33'),
(12, 'guasimalito', 'norte', 1, '2025-12-15 01:29:33'),
(13, 'los sauces', 'nororiente', 1, '2025-12-15 01:29:33'),
(14, 'campo alegre', 'nororiente', 1, '2025-12-15 01:29:33'),
(15, 'las granjas', 'nororiente', 1, '2025-12-15 01:29:33'),
(16, 'la florida', 'nororiente', 1, '2025-12-15 01:29:33'),
(17, 'gran avenida', 'nororiente', 1, '2025-12-15 01:29:33'),
(18, 'aralias', 'nororiente', 1, '2025-12-15 01:29:33'),
(19, 'urapanes', 'nororiente', 1, '2025-12-15 01:29:33'),
(20, 'la primavera', 'nororiente', 1, '2025-12-15 01:29:33'),
(21, 'villa maría', 'nororiente', 1, '2025-12-15 01:29:33'),
(22, 'fontidueño', 'nororiente', 1, '2025-12-15 01:29:33'),
(23, 'la mina', 'nororiente', 1, '2025-12-15 01:29:33'),
(24, 'alcalá', 'nororiente', 1, '2025-12-15 01:29:33'),
(25, 'los ciruelos', 'nororiente', 1, '2025-12-15 01:29:33'),
(26, 'parís', 'centro-norte', 1, '2025-12-15 01:29:33'),
(27, 'la cumbre', 'centro-norte', 1, '2025-12-15 01:29:33'),
(28, 'altavista', 'centro-norte', 1, '2025-12-15 01:29:33'),
(29, 'el carmelo', 'centro-norte', 1, '2025-12-15 01:29:33'),
(30, 'pérez', 'centro-norte', 1, '2025-12-15 01:29:33'),
(31, 'serramonte', 'centro-norte', 1, '2025-12-15 01:29:33'),
(32, 'salento', 'centro-norte', 1, '2025-12-15 01:29:33'),
(33, 'rincón santos', 'centro-norte', 1, '2025-12-15 01:29:33'),
(34, 'estación primera', 'centro-norte', 1, '2025-12-15 01:29:33'),
(35, 'las vegas', 'centro-norte', 1, '2025-12-15 01:29:33'),
(36, 'la camila', 'centro-norte', 1, '2025-12-15 01:29:33'),
(37, 'el rosario', 'centro', 1, '2025-12-15 01:29:33'),
(38, 'centro', 'centro', 1, '2025-12-15 01:29:33'),
(39, 'prado', 'centro', 1, '2025-12-15 01:29:33'),
(40, 'nazareth', 'centro', 1, '2025-12-15 01:29:33'),
(41, 'la meseta', 'centro', 1, '2025-12-15 01:29:33'),
(42, 'central', 'centro', 1, '2025-12-15 01:29:33'),
(43, 'espíritu santo', 'centro', 1, '2025-12-15 01:29:33'),
(44, 'manchester', 'centro', 1, '2025-12-15 01:29:33'),
(45, 'la estación', 'centro', 1, '2025-12-15 01:29:33'),
(46, 'cinco estrellas', 'centro', 1, '2025-12-15 01:29:33'),
(47, 'marco fidel suárez', 'centro', 1, '2025-12-15 01:29:33'),
(48, 'la gabriela', 'centro', 1, '2025-12-15 01:29:33'),
(49, 'belvedere', 'centro', 1, '2025-12-15 01:29:33'),
(50, 'acevedo', 'centro', 1, '2025-12-15 01:29:33'),
(51, 'zamora', 'centro', 1, '2025-12-15 01:29:33'),
(52, 'bellavista', 'centro-sur', 1, '2025-12-15 01:29:33'),
(53, 'suárez', 'centro-sur', 1, '2025-12-15 01:29:33'),
(54, 'andaluz', 'centro-sur', 1, '2025-12-15 01:29:33'),
(55, 'el cafetal', 'centro-sur', 1, '2025-12-15 01:29:33'),
(56, 'la pradera', 'centro-sur', 1, '2025-12-15 01:29:33'),
(57, 'la esmeralda', 'centro-sur', 1, '2025-12-15 01:29:33'),
(58, 'la maruchenga', 'centro-sur', 1, '2025-12-15 01:29:33'),
(59, 'santa ana', 'centro-sur', 1, '2025-12-15 01:29:33'),
(60, 'los búcaros', 'centro-sur', 1, '2025-12-15 01:29:33'),
(61, 'lópez de mesa', 'centro-sur', 1, '2025-12-15 01:29:33'),
(62, 'el cairo', 'centro-sur', 1, '2025-12-15 01:29:33'),
(63, 'fátima', 'sur', 1, '2025-12-15 01:29:33'),
(64, 'san martín', 'sur', 1, '2025-12-15 01:29:33'),
(65, 'playa rica', 'sur', 1, '2025-12-15 01:29:33'),
(66, 'tierradentro', 'sur', 1, '2025-12-15 01:29:33'),
(67, 'villa linda', 'sur', 1, '2025-12-15 01:29:33'),
(68, 'girasoles', 'sur', 1, '2025-12-15 01:29:33'),
(69, 'la milagrosa', 'sur', 1, '2025-12-15 01:29:33'),
(70, 'el congolo', 'sur', 1, '2025-12-15 01:29:33'),
(71, 'el porvenir', 'sur', 1, '2025-12-15 01:29:33'),
(72, 'el rosalpi', 'sur', 1, '2025-12-15 01:29:33'),
(73, 'briceño', 'sur', 1, '2025-12-15 01:29:33'),
(74, 'buenos aires', 'sur', 1, '2025-12-15 01:29:33'),
(75, 'el paraíso', 'sur', 1, '2025-12-15 01:29:33'),
(76, 'riachuelos', 'sur', 1, '2025-12-15 01:29:33'),
(77, 'valadares', 'sur', 1, '2025-12-15 01:29:33'),
(78, 'el trapiche', 'sur', 1, '2025-12-15 01:29:33'),
(79, 'san gabriel', 'sur', 1, '2025-12-15 01:29:33'),
(80, 'pachelly', 'sur', 1, '2025-12-15 01:29:33'),
(81, 'los alpes', 'sur', 1, '2025-12-15 01:29:33'),
(82, 'el ducado', 'sur', 1, '2025-12-15 01:29:33'),
(83, 'la aldea', 'sur', 1, '2025-12-15 01:29:33'),
(84, 'la selva', 'sur', 1, '2025-12-15 01:29:33'),
(85, 'el mirador', 'sur', 1, '2025-12-15 01:29:33'),
(86, 'santa rita', 'sur', 1, '2025-12-15 01:29:33'),
(87, 'villas de occidente', 'occidente', 1, '2025-12-15 01:29:33'),
(88, 'villas del sol', 'occidente', 1, '2025-12-15 01:29:33'),
(89, 'molinares', 'occidente', 1, '2025-12-15 01:29:33'),
(90, 'san simón', 'occidente', 1, '2025-12-15 01:29:33'),
(91, 'amazonía', 'occidente', 1, '2025-12-15 01:29:33'),
(92, 'villas de comfenalco', 'urbanizacion', 1, '2025-12-15 01:29:33'),
(93, 'puerto bello', 'urbanizacion', 1, '2025-12-15 01:29:33'),
(94, 'terranova', 'urbanizacion', 1, '2025-12-15 01:29:33'),
(95, 'hermosa provincia', 'urbanizacion', 1, '2025-12-15 01:29:33'),
(96, 'valle verde', 'urbanizacion', 1, '2025-12-15 01:29:33'),
(97, 'la virginia', 'urbanizacion', 1, '2025-12-15 01:29:33'),
(98, 'josé antonio galán', 'popular', 1, '2025-12-15 01:29:33'),
(99, 'salvador allende', 'popular', 1, '2025-12-15 01:29:33'),
(100, 'barrio nuevo', 'popular', 1, '2025-12-15 01:29:33'),
(101, 'la cabañita', 'popular', 1, '2025-12-15 01:29:33'),
(102, 'la cabaña', 'popular', 1, '2025-12-15 01:29:33'),
(103, 'san josé obrero', 'popular', 1, '2025-12-15 01:29:33'),
(104, 'zona industrial #1', 'industrial', 1, '2025-12-15 01:29:33'),
(105, 'zona industrial #3', 'industrial', 1, '2025-12-15 01:29:33'),
(106, 'zona industrial #4', 'industrial', 1, '2025-12-15 01:29:33'),
(107, 'zona industrial #5', 'industrial', 1, '2025-12-15 01:29:33'),
(108, 'zona industrial #6', 'industrial', 1, '2025-12-15 01:29:33'),
(109, 'zona industrial #7', 'industrial', 1, '2025-12-15 01:29:33'),
(110, 'san félix', 'corregimiento', 1, '2025-12-15 01:29:33'),
(111, 'potrerito', 'corregimiento', 1, '2025-12-15 01:29:33'),
(112, 'granizal', 'corregimiento', 1, '2025-12-15 01:29:33'),
(113, 'el tambo', 'corregimiento', 1, '2025-12-15 01:29:33'),
(114, 'hato viejo', 'corregimiento', 1, '2025-12-15 01:29:33');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `configuracionsistema`
--
ALTER TABLE `configuracionsistema`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `clave` (`clave`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `historialreporte`
--
ALTER TABLE `historialreporte`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usuario_admin_id` (`usuario_admin_id`),
  ADD KEY `idx_reporte` (`reporte_id`),
  ADD KEY `idx_fecha` (`fecha_cambio`);

--
-- Indices de la tabla `reportes`
--
ALTER TABLE `reportes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_tipo_anomalia` (`id_tipo_anomalia`),
  ADD KEY `idx_usuario` (`usuario_id`),
  ADD KEY `idx_barrio` (`barrio`),
  ADD KEY `idx_gravedad` (`gravedad`),
  ADD KEY `idx_estado` (`estado`),
  ADD KEY `idx_fecha` (`fecha_reporte`),
  ADD KEY `idx_ubicacion` (`latitud`,`longitud`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre_rol` (`nombre_rol`);

--
-- Indices de la tabla `tiposanomalia`
--
ALTER TABLE `tiposanomalia`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre_anomalia` (`nombre_anomalia`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  ADD UNIQUE KEY `correo_electronico` (`correo_electronico`),
  ADD KEY `id_rol` (`id_rol`),
  ADD KEY `idx_email` (`correo_electronico`),
  ADD KEY `idx_usuario` (`nombre_usuario`);

--
-- Indices de la tabla `zonas`
--
ALTER TABLE `zonas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre_zona` (`nombre_zona`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `configuracionsistema`
--
ALTER TABLE `configuracionsistema`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `historialreporte`
--
ALTER TABLE `historialreporte`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reportes`
--
ALTER TABLE `reportes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `tiposanomalia`
--
ALTER TABLE `tiposanomalia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=79;

--
-- AUTO_INCREMENT de la tabla `zonas`
--
ALTER TABLE `zonas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=115;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `historialreporte`
--
ALTER TABLE `historialreporte`
  ADD CONSTRAINT `historialreporte_ibfk_1` FOREIGN KEY (`reporte_id`) REFERENCES `reportes` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `historialreporte_ibfk_2` FOREIGN KEY (`usuario_admin_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL;

--
-- Filtros para la tabla `reportes`
--
ALTER TABLE `reportes`
  ADD CONSTRAINT `reportes_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL,
  ADD CONSTRAINT `reportes_ibfk_2` FOREIGN KEY (`id_tipo_anomalia`) REFERENCES `tiposanomalia` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
