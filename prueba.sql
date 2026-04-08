-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 04-03-2026 a las 13:52:59
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
(1, 21, 1, 'el rosario', 'Carrera 58 #50-24', 'critico', 'fefwfwefwe', 'fwefwefwefwe', 'be924c8a9173d91a_2025_Acer_Consumer_Default_3840x2400.jpg', '0f6cfe262417a94c_2025_Acer_Consumer_Option_3840x2400.jpg', NULL, 6.32980000, -75.55730000, 'cerrado', 'Estado cambiado a cerrado', '2026-03-04 12:13:55', '2026-03-04 12:35:54'),
(2, 21, 1, 'el rosario', 'Carrera 58 #50-24', 'moderado', 'fedgfwfwe', 'fwefwe', 'bce2dd194ceed0a6_2025_Acer_Consumer_Default_3840x2400.jpg', '427b8331dc225b70_2025_Acer_Consumer_Option_3840x2400.jpg', NULL, 6.32980000, -75.55730000, 'pendiente', '', '2026-03-04 12:37:40', '2026-03-04 12:43:40'),
(3, 21, 1, 'la florida', 'Carrera 58 #50-22', 'moderado', 'fdasdfsdff', 'dasdfasda', 'e541ed372da96397_2025_Acer_Consumer_Default_3840x2400.jpg', 'e7f1de9a939fd2e6_2025_Acer_Consumer_Option_3840x2400.jpg', NULL, 6.33700000, -75.55200000, 'rechazado', '', '2026-03-04 12:38:46', '2026-03-04 12:43:30'),
(4, 21, 1, 'niquía bifamiliares', 'Av. 43 #57-07', 'critico', 'fsdfsdf', 'fsdfsdfsdf', 'b5b7e5aa24db1445_2025_Acer_Consumer_Default_3840x2400.jpg', 'b7d63d279200a96c_2025_Acer_Consumer_Option_3840x2400.jpg', NULL, 6.34300000, -75.54500000, 'cerrado', 'Estado cambiado a cerrado', '2026-03-04 12:41:13', '2026-03-04 12:45:33');

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
(5, 'admin_tecnico', 'Administrador técnico - Gestiona flujo de trabajo de reportes aprobados', '2025-12-15 01:51:55');

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
  `id_rol` int(11) NOT NULL DEFAULT 2,
  `activo` tinyint(1) DEFAULT 1,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `ultimo_acceso` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre_usuario`, `correo_electronico`, `contrasena_hash`, `id_rol`, `activo`, `fecha_registro`, `ultimo_acceso`) VALUES
(3, 'Invitado Sistema', 'guest@safezone.com', 'NO_PASSWORD_NEEDED', 3, 1, '2025-12-15 01:29:33', NULL),
(4, 'Usuario Demo', 'usuario@safezone.com', '$2b$12$hDUn4gxbzghBnPdZIBSFk.ACONih0mVzRKhfFZx4bRtqy2uXru7Nq', 2, 1, '2025-12-15 01:31:18', NULL),
(19, 'Admin Principal', 'admin@safezone.com', '$2b$12$9JIuZbX3gxaD.R/Fw04G5u4n97jR6WqyWwLkdc5iSRghQxD8wg77u', 4, 1, '2025-12-15 23:10:39', NULL),
(20, 'Admin Técnico', 'tecnico@safezone.com', '$2b$12$ychycySTxao9uGh4pxJPJuAJq4Zf3S3avQaOF4v.nBrbBidSQAqt2', 5, 1, '2025-12-15 23:10:56', NULL),
(21, 'Cristian Garcia', 'criscagarpa@gmail.com', '$2b$12$uzCyqZwxZFyG7kNtKjdO3ej7T8QJGBrRsJYjZJl.i4uEbFjgba4pe', 2, 1, '2026-03-04 12:12:12', NULL);

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
-- Indices de la tabla `configuracionsistema`
--
ALTER TABLE `configuracionsistema`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `clave` (`clave`);

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

-- Agregar columna teléfono si no existe
ALTER TABLE `usuarios` ADD COLUMN IF NOT EXISTS `telefono` varchar(20) DEFAULT NULL AFTER `contrasena_hash`;

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
-- AUTO_INCREMENT de la tabla `configuracionsistema`
--
ALTER TABLE `configuracionsistema`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `historialreporte`
--
ALTER TABLE `historialreporte`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `reportes`
--
ALTER TABLE `reportes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `tiposanomalia`
--
ALTER TABLE `tiposanomalia`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `zonas`
--
ALTER TABLE `zonas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=115;

--
-- Restricciones para tablas volcadas
--

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
