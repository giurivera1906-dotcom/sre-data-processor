Resultados de pruebas locales

1. Objetivo

Validar el funcionamiento local del servicio de procesamiento de datos, la integracion con Redis, el almacenamiento de resultados en archivos JSON y el manejo de errores HTTP.

2. Entorno de pruebas

Sistema operativo: Windows 10.
Lenguaje: Python.
API local: Flask.
Cache: Redis 7 ejecutado mediante Docker.
Herramienta de pruebas HTTP: PowerShell.
Almacenamiento de resultados: archivos JSON locales.

3. Casos de prueba

Primera peticion con datos validos - HTTP 200 y X-Cache: MISS
Resultado : HTTP 200 y MISS - Correcto

Segunda peticion identica - HTTP 200 y X-Cache: HIT
Resultado : HTTP 200 y HIT - Correcto

Expiracion de una clave Redis - La clave expira despues del TTL configurado
Resultado : La clave expiro - Correcto

Solicitud con JSON invalido - HTTP 400
Resltado : HTTP 400 - Correcto

Solicitud con Redis detenido - HTTP 500
Resultado : HTTP 500 - Correcto

Recuperacion de Redis - Redis vuelve a responder
Respuesta a la solicitud de ping PONG - Corrrecto

Almacenamiento de resultados - Se crea un archivo JSON local
Resultado : Archivo JSON encontrado - Correcto

4. Analisis de resultados

Las pruebas locales permitieron comprobar el procesamiento de solicitudes, el uso de la cache Redis, la expiracion de claves, el almacenamiento en archivos JSON y el manejo de algunos errores.
La cabecera X-Cache permite distinguir entre una respuesta obtenida mediante una entrada existente en cache (HIT) y una respuesta que requiere procesamiento (MISS).
La prueba con JSON invalido confirmo que la API rechaza solicitudes mal formadas. La prueba de indisponibilidad de Redis confirmo que la API devuelve un error HTTP 500 cuando no puede utilizar la cache.
Tras iniciar nuevamente Redis, el servicio respondio correctamente al comando PING.

5. Alcance y limitaciones

Estas pruebas corresponden al entorno local. No demuestran por si solas el funcionamiento de la arquitectura desplegada en AWS.
El almacenamiento se realizo en archivos JSON locales; todavia debe verificarse por separado el almacenamiento real en Amazon S3. Tambien deben revisarse los requisitos de infraestructura, permisos IAM, seguridad de red, API Gateway, Lambda y CloudWatch.

6. Evidencias

evidence/cache-miss-hit.png: comportamiento de la cache.
evidence/invalid-json.png: rechazo de JSON invalido.
evidence/redis-unavailable.png: indisponibilidad de Redis, si se guardo esa captura.

7. Conclusion

Las pruebas locales ejecutadas hasta el momento fueron satisfactorias para los casos documentados. El siguiente paso consiste en revisar la infraestructura como codigo y validar el cumplimiento de los requisitos especificos de AWS antes de preparar la entrega final.