# Resultados de pruebas locales

## 1. Objetivo

Validar el funcionamiento local del servicio de procesamiento de datos, la integración con Redis, el almacenamiento de resultados en archivos JSON y el manejo de errores HTTP.

## 2. Entorno de pruebas

- **Sistema operativo:** Windows 10.
- **Lenguaje:** Python.
- **API local:** Flask.
- **Caché:** Redis 7 ejecutado mediante Docker.
- **Herramienta de pruebas HTTP:** PowerShell.
- **Almacenamiento de resultados:** archivos JSON locales.

## 3. Casos de prueba

### 3.1. Primera petición con datos válidos

- **Esperado:** HTTP 200 y `X-Cache: MISS`.
- **Resultado observado:** HTTP 200 y `X-Cache: MISS`.
- **Estado:** Correcto.

### 3.2. Segunda petición idéntica

- **Esperado:** HTTP 200 y `X-Cache: HIT`.
- **Resultado observado:** HTTP 200 y `X-Cache: HIT`.
- **Estado:** Correcto.

### 3.3. Expiración de una clave Redis

- **Esperado:** la clave expira después del TTL configurado.
- **Resultado observado:** la clave expiró.
- **Estado:** Correcto.

### 3.4. Solicitud con JSON inválido

- **Esperado:** HTTP 400.
- **Resultado observado:** HTTP 400.
- **Estado:** Correcto.

### 3.5. Solicitud con Redis detenido

- **Esperado:** HTTP 500 cuando la API no puede utilizar la caché.
- **Resultado observado:** HTTP 500.
- **Estado:** Correcto.

### 3.6. Recuperación de Redis

- **Esperado:** Redis vuelve a responder después de iniciarse nuevamente.
- **Resultado observado:** respuesta `PONG` al comando `PING`.
- **Estado:** Correcto.

### 3.7. Almacenamiento de resultados

- **Esperado:** se crea un archivo JSON local.
- **Resultado observado:** archivo JSON encontrado.
- **Estado:** Correcto.

## 4. Análisis de resultados

Las pruebas locales permitieron comprobar el procesamiento de solicitudes, el uso de la caché Redis, la expiración de claves, el almacenamiento en archivos JSON y el manejo de errores.

La cabecera `X-Cache` permite distinguir entre una respuesta obtenida mediante una entrada existente en caché (`HIT`) y una respuesta que requiere procesamiento (`MISS`).

La prueba con JSON inválido confirmó que la API rechaza solicitudes mal formadas. La prueba de indisponibilidad de Redis confirmó que la API devuelve HTTP 500 cuando no puede utilizar la caché. Tras iniciar nuevamente Redis, el servicio respondió correctamente al comando `PING`.

## 5. Alcance y limitaciones

Estas pruebas corresponden al entorno local de Flask y Redis. No demuestran por sí solas el funcionamiento de la arquitectura desplegada en AWS.

El almacenamiento descrito en este informe se realizó en archivos JSON locales. Las pruebas de almacenamiento en S3 de LocalStack se documentan por separado en `evidence/README.md`.

La infraestructura real de AWS, los permisos IAM, la seguridad de red, API Gateway, Lambda y CloudWatch requieren validación adicional en el entorno objetivo.

## 6. Evidencias

- `evidence/cache-miss-hit.png`: evidencia visual del comportamiento de la caché.
- `evidence/invalid-json.png`: evidencia visual del rechazo de JSON inválido.

La captura `evidence/redis-unavailable.png` no se incluye en la lista de archivos disponible actualmente. No debe presentarse como evidencia adjunta hasta que se guarde y verifique.

## 7. Conclusión

Las pruebas locales documentadas fueron satisfactorias para los casos descritos. La validación de la infraestructura como código y las pruebas de Lambda y S3 en LocalStack se documentan por separado. El despliegue y la validación completa de la arquitectura en AWS real permanecen pendientes.