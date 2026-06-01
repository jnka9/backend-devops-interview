# Transcripcion Compacta de IA

Use un asistente de IA durante el ejercicio. Esta es una transcripcion compacta de los prompts y decisiones relevantes.

## 1. Revision inicial del codigo

**Prompt:** Analiza el proyecto Django para identificar N+1, recursion, iteraciones innecesarias, riesgos de rendimiento en la API e indices faltantes en la base de datos.

**Salida util:** El asistente identifico N+1 en los endpoints de lista/search/by-tag de posts, carga de autores en comentarios del detalle, respuestas no acotadas, busquedas de tags una por una al crear posts e indices faltantes para posts publicados, comentarios, email de usuario, busqueda trigram y lookup por tag.

## 2. Seleccion de alcance

**Prompt:** Planifica la solucion de la prueba tecnica alrededor de experiencia de desarrollo, rendimiento y preparacion para produccion, usando Fly.io y un flujo `develop -> main`.

**Salida util:** El asistente recomendo profundizar en tres areas: setup local reproducible, rendimiento de API/base de datos y una ruta simple a produccion con Docker, Fly.io y GitHub Actions.

## 3. Apoyo de implementacion

**Prompt:** Implementa los cambios planificados.

**Salida util:** El asistente ayudo a aplicar Docker Compose, settings por variables de entorno, mejoras N+1, paginacion, indices de base de datos, Gunicorn, configuracion de Fly.io, GitHub Actions.

## 4. Decisiones de arquitectura posteriores

**Prompt:** Mejora el diseno de respuestas anidadas y separa la API por dominio/entidad.

**Salida util:** El asistente recomendo mover comentarios fuera del detalle de post hacia `GET /api/posts/{post_id}/comments` y luego dividir el modulo API monolitico en posts, comments, users, serializers compartidos y helpers de paginacion.
