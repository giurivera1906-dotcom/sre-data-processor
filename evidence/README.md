# Evidencias de pruebas — SRE Data Processor

## 1. Entorno de ejecución

- **Entorno:** LocalStack ejecutado mediante Docker Compose.
- **Región simulada:** `us-east-1`.
- **Función Lambda:** `sre-data-processor-local`.
- **Bucket de pruebas:** `sre-data-processor-smoke-20261010`.
- **Caché:** Redis 7.
- **AWS real:** no se ha desplegado infraestructura en una cuenta AWS real.

## 2. Pruebas ejecutadas

### 2.1. Procesamiento correcto

Se invocó la función Lambda con el evento `evento-prueba.json`.

**Resultados observados:**

- `statusCode`: `200`.
- `X-Cache`: `MISS` en la primera solicitud.
- El campo `input` contiene `event_id` y `message`.
- Se generó una clave de objeto bajo `results/`.
- El resultado se guardó en S3 de LocalStack.

### 2.2. Caché Redis

Se repitió la invocación con el mismo evento.

**Resultados observados:**

- `statusCode`: `200`.
- `X-Cache`: `HIT`.
- Se reutilizaron el mismo `request_id` y la misma `s3_key` de la primera respuesta.

### 2.3. JSON inválido

Se invocó Lambda con un evento HTTP cuyo campo `body` contenía JSON inválido.

**Resultados observados:**

- `statusCode`: `400`.
- Mensaje: `Request body is not valid JSON.`

### 2.4. Validación de Terraform

Comando ejecutado desde la raíz del proyecto:

```powershell
terraform -chdir=terraform validate
```

Resultado observado:

```text
Success! The configuration is valid.
```

Esta validación confirma que Terraform acepta la estructura de la configuración. No demuestra que todos los recursos puedan desplegarse correctamente en AWS real.

## 3. Archivos de resultados locales

Durante las pruebas se utilizaron archivos bajo `local-results/`, entre ellos:

- `evento-prueba.json`
- `respuesta-lambda.json`
- `respuesta-lambda-hit.json`
- `evento-invalido.json`
- `respuesta-invalida.json`
- `resultado-s3.json`

Estos archivos se mantienen fuera del repositorio Git mediante `.gitignore`. Por tanto, sus nombres documentan los resultados locales, pero los archivos no forman parte de la entrega versionada.

## 4. Capturas incluidas

- `cache-miss-hit.png`: evidencia visual del comportamiento de la caché.
- `invalid-json.png`: evidencia visual del rechazo de JSON inválido.

Antes de presentar la entrega, verifica que ambas capturas correspondan a las ejecuciones descritas y que sus resultados sean legibles.

## 5. Alcance y limitaciones

Las pruebas de Lambda y S3 se realizaron con LocalStack. No se ha ejecutado `terraform apply` y no se afirma que la infraestructura haya sido desplegada en AWS real.

La validación completa de la arquitectura, los permisos IAM, la conectividad de red y el comportamiento de los servicios en AWS real permanece pendiente.