# Notas

### Qué hice y por qué
Decidí concentrarme en tres áreas específicas, priorizando profundidad sobre amplitud. El objetivo fue abordar los principales riesgos técnicos del proyecto y dejar una base sólida para su evolución.

### 1. Mejoras en la experiencia de desarrollo local
Implementé una configuración reproducible basada en Docker Compose, agregué un .env.example, moví la configuración a variables de entorno y documenté los comandos principales de operación.

#### Motivación
- Reducir la fricción de incorporación para nuevos desarrolladores.
- Garantizar consistencia entre entornos de desarrollo.
- Adoptar desde el inicio prácticas alineadas con los principios de configuración externa y Twelve-Factor App.
- Facilitar la ejecución del proyecto en una máquina nueva con el menor esfuerzo posible.

Docker permite abstraer diferencias entre sistemas operativos y configuraciones locales, mientras que las variables de entorno evitan dependencias implícitas y favorecen una gestión más segura de la configuración.

### 2. Optimización de rendimiento y organización del dominio
Me enfoqué en los endpoints más impactados por el dataset existente mediante:

- Eager loading de relaciones.
- Paginación de resultados(Si esta API ya estuviera integrada con plataformas externas, esto habría significado un breaking change (cambio disruptivo), por lo que la decisión correcta en un entorno real habría sido introducirlo bajo una nueva versión de la API (/v2/) para no romper clientes existentes.).
- Separación de comentarios en un endpoint dedicado.
- Creación de índices de base de datos.
- Actualización atómica del contador de visitas.
- Organización del código por dominios funcionales.

#### Motivación

La optimización de rendimiento no debe limitarse únicamente a mejorar consultas SQL; también debe considerar la capacidad del sistema para escalar y evolucionar de forma sostenible.

Adicionalmente, separé la lógica por dominios (Posts, Comments y Users) para evitar la concentración de responsabilidades en un único módulo. Esta estructura reduce acoplamiento, mejora mantenibilidad, facilita la escalabilidad del código y disminuye conflictos de integración entre equipos.

### 3. Preparación para despliegue y operación en producción

Preparé una ruta básica de producción utilizando Docker, Gunicorn, un endpoint de salud (/healthz), despliegue en Fly.io y automatización mediante GitHub Actions.

#### Motivación

- Garantizar consistencia entre desarrollo y producción.
- Facilitar despliegues repetibles y automatizadas.
- Incorporar validaciones tempranas mediante pipelines de CI.
- Establecer una base para observabilidad y operación continua.
- La inclusión de GitHub Actions permite automatizar pruebas y verificaciones de calidad antes de cada despliegue. Además, la integración con herramientas como CodeQL impulsa prácticas de desarrollo seguro desde etapas tempranas del proyecto.

### Decisiones deliberadas que no implementé
#### No intentar resolver todos los problemas simultáneamente
Priorizé identificar los problemas más relevantes y resolver aquellos con mayor impacto inmediato sobre rendimiento, mantenibilidad y experiencia de desarrollo.
Considero más valioso establecer prioridades explícitas que distribuir esfuerzo en múltiples frentes con bajo retorno.
#### No implementar versionado de API
Dado el alcance y la ambigüedad de los requerimientos, decidí no incorporar versionado en esta iteración.
Sin embargo, es un aspecto importante a considerar en futuras versiones, ya que la ausencia de versionado puede dificultar la evolución de contratos y generar incompatibilidades para consumidores existentes.
#### No mover el conteo de visitas a procesamiento asíncrono
Mantuve el incremento mediante una actualización atómica porque resultaba suficiente para el volumen esperado en esta etapa.
Reconozco que existe una deuda técnica: una petición GET idealmente no debería modificar el estado del sistema. En una etapa posterior evaluaría desacoplar esta responsabilidad mediante eventos o procesamiento asíncrono.
#### No incorporar una capa de caché
Opté por resolver primero los problemas estructurales de acceso a datos mediante optimización de consultas, paginación e índices antes de introducir mecanismos de caché.
Aunque una caché podría mejorar el rendimiento percibido, también introduce complejidad adicional:
- Estrategias de invalidación.
- Mayor costo operativo.
- Nuevos componentes de infraestructura.
- Incremento de la carga de mantenimiento.
Considero que la decisión de incorporar caché debe estar respaldada por métricas y análisis de costo-beneficio.


### Qué haría con un día adicional

- Implementar rate limiting para mitigar abusos y proteger recursos críticos.
- Incorporar autenticación y autorización basada en roles y permisos.
- Agregaria serializadores por tipo de role, asi avanzamos para la ley de protección de datos.
- Integrar una solución APM para monitoreo de rendimiento.
- Incorporar Sentry para detección y seguimiento de errores en tiempo real.
- Migrar la paginación basada en offset hacia cursor pagination para mejorar el comportamiento en conjuntos de datos grandes.
- Incorporar una estrategia de caché para lecturas frecuentes.
- Ejecutar pruebas de carga utilizando Apache K6 para validar comportamiento bajo estrés.
- Fortalecer los pipelines de calidad y seguridad existentes.
- Introducir versionado explícito de la API para permitir cambios evolutivos sin afectar clientes existentes.
- Revisar el mecanismo de conteo de visitas para eliminar efectos secundarios en peticiones GET y migrarlo hacia una arquitectura basada en eventos o procesamiento asíncrono.
- Priorizar cada una de estas con el equipo de producto y engineering.

