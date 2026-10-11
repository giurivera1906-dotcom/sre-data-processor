# Evidencias de pruebas — SRE Data Processor

## Entorno de ejecución

- **Entorno:** LocalStack ejecutado mediante Docker Compose.
- **Región simulada:** `us-east-1`.
- **Función Lambda:** `sre-data-processor-local`.
- **Bucket de pruebas:** `sre-data-processor-smoke-20261010`.
- **Caché:** Redis 7.
- **AWS real:** No se ha desplegado infraestructura en una cuenta AWS real.

## Pruebas ejecutadas

### 1. Procesamiento correcto

Se invocó la función Lambda con el evento `evento-prueba.json`.

Resultado observado:
- `statusCode`: `200`.
- `X-Cache`: `MISS` en la primera solicitud.
- El campo `input` contiene `event_id` y `message`.
- Se generó una clave de objeto bajo `results/`.
- El resultado se guardó en S3 de LocalStack.

### 2. Caché Redis

Se repitió la invocación con el mismo evento.

Resultado observado:
- `statusCode`: `200`.
- `X-Cache`: `HIT`.
- Se reutilizaron el mismo `request_id` y la misma `s3_key` de la primera respuesta.

### 3. JSON inválido

Se invocó Lambda con un evento HTTP cuyo campo `body` contenía JSON inválido.

Resultado observado:
- `statusCode`: `400`.
- Mensaje: `Request body is not valid JSON.`

### 4. Validación de Terraform

Comando ejecutado:

```powershell
terraform -chdir=terraform validate
```

Resultado observado:

```text
Success! The configuration is valid.
```

Esta validación confirma la validez de la configuración de Terraform, pero no demuestra que los recursos puedan desplegarse correctamente en AWS real.

## Archivos de resultados

- `../local-results/evento-prueba.json`
- `../local-results/respuesta-lambda.json`
- `../local-results/respuesta-lambda-hit.json`
- `../local-results/evento-invalido.json`
- `../local-results/respuesta-invalida.json`
- `../local-results/resultado-s3.json`

## Capturas de pantalla

Las capturas deben corresponder a las ejecuciones reales y mostrar los resultados descritos. Si una captura anterior no refleja las pruebas actuales, debe actualizarse antes de presentarla.

**Nota:** las pruebas se realizaron en LocalStack. No se ha ejecutado `terraform apply` y no se afirma un despliegue exitoso en AWS real.