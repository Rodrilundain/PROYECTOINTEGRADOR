-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-06-2026 a las 23:56:04
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyredqualitas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contextos`
--

CREATE TABLE `contextos` (
  `id_contexto` int(11) NOT NULL,
  `origen` varchar(100) NOT NULL,
  `actividad` varchar(150) NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `contextos`
--

INSERT INTO `contextos` (`id_contexto`, `origen`, `actividad`, `ubicacion`, `descripcion`) VALUES
(1, 'Aplicación educativa', 'Práctica guiada de variables', 'Laboratorio de informática', 'Actividad introductoria para declarar variables, tipos de datos y operaciones simples.'),
(2, 'Aplicación educativa', 'Ejercicio de condicionales', 'Laboratorio de informática', 'Resolución de problemas con estructuras if, elif y else.'),
(3, 'Aplicación educativa', 'Ejercicio de bucles', 'Laboratorio de informática', 'Práctica con ciclos for y while para recorrer datos.'),
(4, 'Aplicación educativa', 'Práctica de funciones', 'Laboratorio de informática', 'Diseño de funciones con parámetros, retorno y responsabilidad única.'),
(5, 'Plataforma virtual', 'Entrega de tarea individual', 'Aula virtual', 'Carga de una solución individual en la plataforma institucional.'),
(6, 'Plataforma virtual', 'Reentrega corregida', 'Aula virtual', 'Nueva entrega luego de revisar observaciones o errores previos.'),
(7, 'Plataforma virtual', 'Carga de proyecto parcial', 'Aula virtual', 'Subida de avances del proyecto integrador para revisión.'),
(8, 'Plataforma virtual', 'Entrega final de módulo', 'Aula virtual', 'Entrega de producto final correspondiente a una unidad del curso.'),
(9, 'Actividad presencial', 'Trabajo en pares', 'Aula taller', 'Resolución de una consigna breve junto a otro estudiante.'),
(10, 'Actividad presencial', 'Trabajo en equipo', 'Aula taller', 'Construcción colaborativa de una solución de programación.'),
(11, 'Actividad presencial', 'Revisión cruzada entre pares', 'Aula taller', 'Lectura y comentario del código producido por otros estudiantes.'),
(12, 'Actividad presencial', 'Debate de soluciones', 'Aula taller', 'Comparación grupal de distintas estrategias para resolver un problema.'),
(13, 'Formulario web', 'Evaluación diagnóstica inicial', 'Aula virtual', 'Cuestionario inicial para identificar conocimientos previos.'),
(14, 'Formulario web', 'Mini quiz de repaso', 'Aula virtual', 'Preguntas breves sobre contenidos trabajados recientemente.'),
(15, 'Formulario web', 'Encuesta de comprensión', 'Aula virtual', 'Registro rápido de dudas y nivel de comprensión percibido.'),
(16, 'Sistema de evaluación', 'Prueba parcial', 'Laboratorio de informática', 'Evaluación individual con tiempo limitado y consignas integradoras.'),
(17, 'Sistema de evaluación', 'Simulacro de prueba', 'Laboratorio de informática', 'Instancia de práctica con formato similar a una evaluación formal.'),
(18, 'Sistema de evaluación', 'Ejercicio contrarreloj', 'Laboratorio de informática', 'Resolución de una tarea breve bajo límite estricto de tiempo.'),
(19, 'Sistema de evaluación', 'Defensa individual breve', 'Aula taller', 'Explicación oral de decisiones tomadas en una solución de código.'),
(20, 'Foro educativo', 'Consulta en foro técnico', 'Aula virtual', 'Publicación de una pregunta sobre errores, consignas o conceptos.'),
(21, 'Foro educativo', 'Respuesta a compañeros en foro', 'Aula virtual', 'Colaboración con otros estudiantes mediante respuestas o sugerencias.'),
(22, 'Foro educativo', 'Lectura de dudas frecuentes', 'Aula virtual', 'Revisión de preguntas frecuentes y respuestas del curso.'),
(23, 'Plataforma virtual', 'Navegación por plataforma', 'Aula virtual', 'Acceso a secciones, materiales, tareas y comunicaciones del curso.'),
(24, 'Plataforma virtual', 'Revisión de recursos del curso', 'Aula virtual', 'Consulta de materiales obligatorios y guías de trabajo.'),
(25, 'Plataforma virtual', 'Acceso a videotutorial', 'Domicilio', 'Visualización de explicaciones grabadas para reforzar contenidos.'),
(26, 'Entorno de desarrollo', 'Depuración de error sintáctico', 'Laboratorio de informática', 'Corrección de errores de escritura del código detectados al ejecutar.'),
(27, 'Entorno de desarrollo', 'Depuración de error lógico', 'Laboratorio de informática', 'Búsqueda de fallas en el razonamiento o resultado del programa.'),
(28, 'Entorno de desarrollo', 'Prueba de casos límite', 'Laboratorio de informática', 'Verificación del programa con entradas especiales o poco frecuentes.'),
(29, 'Entorno de desarrollo', 'Corrección de importación de archivos', 'Laboratorio de informática', 'Ajuste de rutas, lectura de CSV o conexión con base de datos.'),
(30, 'Entorno de desarrollo', 'Ajuste de visualización de gráficos', 'Laboratorio de informática', 'Corrección de títulos, ejes, filtros o representación gráfica.'),
(31, 'Actividad presencial', 'Presentación de avance', 'Aula taller', 'Exposición breve del progreso del proyecto integrador.'),
(32, 'Actividad presencial', 'Presentación final', 'Aula taller', 'Presentación del producto final y principales resultados obtenidos.'),
(33, 'Actividad presencial', 'Retroalimentación oral', 'Aula taller', 'Recepción de comentarios inmediatos durante una instancia presencial.'),
(34, 'Formulario web', 'Autoevaluación de unidad', 'Aula virtual', 'Reflexión individual sobre aprendizaje, dificultades y logros.'),
(35, 'Formulario web', 'Diario reflexivo', 'Aula virtual', 'Registro escrito breve sobre el proceso personal de aprendizaje.'),
(36, 'Formulario web', 'Encuesta de cierre', 'Aula virtual', 'Valoración final de una unidad, actividad o entrega.'),
(37, 'Sistema docente', 'Lectura de devolución docente', 'Aula virtual', 'Revisión de comentarios y sugerencias realizadas por el docente.'),
(38, 'Sistema docente', 'Corrección luego de feedback', 'Aula virtual', 'Ajuste de una entrega a partir de la devolución recibida.'),
(39, 'Sistema docente', 'Reunión breve con docente', 'Aula taller', 'Intercambio corto para orientar dudas o dificultades del proyecto.'),
(40, 'Sistema docente', 'Consulta individual', 'Aula virtual', 'Consulta personalizada sobre una dificultad técnica o conceptual.'),
(41, 'Repositorio de recursos', 'Exploración de documentación', 'Domicilio', 'Búsqueda de información en documentación o apuntes del curso.'),
(42, 'Repositorio de recursos', 'Búsqueda de ejemplos externos', 'Domicilio', 'Consulta de ejemplos de código o explicaciones complementarias.'),
(43, 'Repositorio de recursos', 'Revisión de notebook modelo', 'Domicilio', 'Lectura y ejecución de un notebook de referencia provisto por el curso.'),
(44, 'Repositorio de recursos', 'Práctica autónoma domiciliaria', 'Domicilio', 'Resolución individual de ejercicios fuera del horario de clase.'),
(45, 'Repositorio de recursos', 'Repaso previo a evaluación', 'Domicilio', 'Estudio autónomo de contenidos antes de una instancia evaluativa.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `etiquetas_emocionales`
--

CREATE TABLE `etiquetas_emocionales` (
  `id_etiqueta` int(11) NOT NULL,
  `nombre_etiqueta` varchar(50) NOT NULL,
  `valencia_min` decimal(4,2) NOT NULL,
  `valencia_max` decimal(4,2) NOT NULL,
  `activacion_min` decimal(4,2) NOT NULL,
  `activacion_max` decimal(4,2) NOT NULL,
  `cuadrante` varchar(30) NOT NULL CHECK (`valencia_min` >= -1.00 and `valencia_max` <= 1.00 and `valencia_min` <= `valencia_max` and `activacion_min` >= -1.00 and `activacion_max` <= 1.00 and `activacion_min` <= `activacion_max`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `etiquetas_emocionales`
--

INSERT INTO `etiquetas_emocionales` (`id_etiqueta`, `nombre_etiqueta`, `valencia_min`, `valencia_max`, `activacion_min`, `activacion_max`, `cuadrante`) VALUES
(1, 'Entusiasta', 0.30, 1.00, 0.30, 1.00, 'Positiva-Alta'),
(2, 'Calmo', 0.30, 1.00, -1.00, 0.29, 'Positiva-Baja'),
(3, 'Frustrado', -1.00, -0.30, 0.30, 1.00, 'Negativa-Alta'),
(4, 'Triste', -1.00, -0.30, -1.00, 0.29, 'Negativa-Baja'),
(5, 'Tenso', -0.29, 0.29, 0.60, 1.00, 'Neutra-Alta'),
(6, 'Alerta', -0.29, 0.29, 0.30, 0.59, 'Neutra-Media-Alta'),
(7, 'Neutro', -0.29, 0.29, -0.29, 0.29, 'Centro'),
(8, 'Cansado', -0.29, 0.29, -1.00, -0.30, 'Neutra-Baja');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros_afectivos`
--

CREATE TABLE `registros_afectivos` (
  `id_registro` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_contexto` int(11) NOT NULL,
  `fecha_hora` datetime NOT NULL,
  `valencia` decimal(4,2) NOT NULL CHECK (`valencia` between -1.00 and 1.00),
  `activacion` decimal(4,2) NOT NULL CHECK (`activacion` between -1.00 and 1.00),
  `comentario` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `edad` int(11) NOT NULL,
  `genero` varchar(20) DEFAULT NULL CHECK (`edad` between 12 and 100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `edad`, `genero`) VALUES
(1, 'Ana Pérez', 35, 'F'),
(2, 'Bruno Gómez', 39, 'M'),
(3, 'Carla Rodríguez', 40, 'F'),
(4, 'Diego Fernández', 26, 'M'),
(5, 'Elena Silva', 32, 'F'),
(6, 'Federico Martínez', 34, 'M'),
(7, 'Gabriela López', 35, 'F'),
(8, 'Hernán Cardozo', 42, 'M'),
(9, 'Inés Acosta', 36, 'F'),
(10, 'Joaquín Suárez', 25, 'M'),
(11, 'Lucía Méndez', 22, 'F'),
(12, 'Martín Castro', 39, 'M'),
(13, 'Natalia Ramos', 36, 'F'),
(14, 'Octavio Varela', 37, 'M'),
(15, 'Paula Costa', 22, 'F'),
(16, 'Rafael Sosa', 18, 'M'),
(17, 'Sofía Díaz', 19, 'F'),
(18, 'Tomás Moreira', 19, 'M'),
(19, 'Valentina Benítez', 32, 'F'),
(20, 'Agustín Álvarez', 18, 'M'),
(21, 'Camila Torres', 41, 'F'),
(22, 'Emiliano Ferreira', 24, 'M'),
(23, 'Florencia Molina', 33, 'F'),
(24, 'Ignacio Ríos', 32, 'M'),
(25, 'Julieta Cabrera', 34, 'F'),
(26, 'Leandro Morales', 27, 'M'),
(27, 'Manuela Navarro', 28, 'F'),
(28, 'Nicolás Ibarra', 35, 'M'),
(29, 'Romina Perdomo', 27, 'F'),
(30, 'Santiago Olivera', 32, 'M');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `contextos`
--
ALTER TABLE `contextos`
  ADD PRIMARY KEY (`id_contexto`);

--
-- Indices de la tabla `etiquetas_emocionales`
--
ALTER TABLE `etiquetas_emocionales`
  ADD PRIMARY KEY (`id_etiqueta`);

--
-- Indices de la tabla `registros_afectivos`
--
ALTER TABLE `registros_afectivos`
  ADD PRIMARY KEY (`id_registro`),
  ADD KEY `fk_registros_usuarios` (`id_usuario`),
  ADD KEY `fk_registros_contextos` (`id_contexto`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `contextos`
--
ALTER TABLE `contextos`
  MODIFY `id_contexto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `registros_afectivos`
--
ALTER TABLE `registros_afectivos`
  ADD CONSTRAINT `fk_registros_contextos` FOREIGN KEY (`id_contexto`) REFERENCES `contextos` (`id_contexto`),
  ADD CONSTRAINT `fk_registros_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
