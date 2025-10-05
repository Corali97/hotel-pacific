# Manual de Usuario Testing

Este manual describe el procedimiento para ejecutar las pruebas funcionales sobre el MVP de Hotel Pacific en el ambiente de calidad. Incluye accesos, credenciales de referencia, flujos cubiertos y tiempos estimados de ejecución.

## 1. Acceso al ambiente de pruebas
- **URL base:** `https://qa.hotelpacific.io`
- **Disponibilidad:** Lunes a viernes de 08:00 a 20:00 (GMT-5).
- **Requisitos técnicos:** Navegador Google Chrome 122+, conexión estable a Internet (≥ 10 Mbps), permisos para ejecutar scripts de automatización en caso de pruebas asistidas.

## 2. Credenciales de prueba
| Rol | Usuario | Contraseña | Observaciones |
| --- | --- | --- | --- |
| Huésped QA | `qa.huesped@hotelpacific.com` | `Pacific#2024` | Permite validar dashboard, reservas y cancelaciones. |
| Recepción QA | `qa.recepcion@hotelpacific.com` | `FrontDesk#2024` | Acceso a tablero operativo y a administración de reservas. |
| Administrador QA | `qa.admin@hotelpacific.com` | `Root#2024` | Úsese solo para configurar datos maestros. |

> **Nota:** Las credenciales se regeneran cada lunes. Solicitar versiones actualizadas al canal `#qa-hotel-pacific` si aparece error de autenticación.

## 3. Flujo de inicio de sesión
1. Abrir `https://qa.hotelpacific.io/login`.
2. Ingresar correo y contraseña correspondientes al rol evaluado.
3. Hacer clic en **Ingresar**.
4. Confirmar que la URL cambia a `/dashboard` y que el banner de bienvenida se muestra con el nombre del usuario.

**Tiempo estimado:** 1 minuto por intento.

## 4. Navegación por funcionalidades cubiertas
### 4.1 Dashboard de huésped
- Verificar widgets de "Próximas estadías", "Recomendaciones" y "Historial".
- Revisar que los indicadores se actualicen tras crear una reserva.
- Tiempo estimado: 3 minutos.

### 4.2 Creación de reserva
1. Desde el menú lateral, seleccionar **Reservar habitación**.
2. Elegir fechas de entrada y salida dentro de las ventanas disponibles.
3. Seleccionar el tipo de habitación y confirmar tarifa.
4. Ingresar datos de pago de prueba (tarjeta sandbox).
5. Revisar el resumen y confirmar.

**Tiempo estimado:** 5 a 7 minutos, dependiendo de la complejidad de la reserva.

### 4.3 Cancelación de reserva
1. Abrir la sección **Mis reservas**.
2. Identificar la reserva activa (estado "Confirmada").
3. Seleccionar **Cancelar reserva** y confirmar la acción.
4. Verificar que el estado cambie a "Cancelada" y que se envíe correo de confirmación.

**Tiempo estimado:** 4 minutos.

### 4.4 Reporte de incidencias
- Si se detecta un comportamiento inesperado, abrir ticket en Jira (proyecto HP) con prioridad según matriz de impacto.
- Adjuntar evidencias descritas en [Formato de respuestas](PRY3211_Exp3_S8_Formato_de_respuestas.md).
- Tiempo estimado: 6 minutos por ticket.

## 5. Registro de evidencias
- Guardar capturas de pantalla y videos en la carpeta compartida del equipo QA.
- Actualizar referencias en [`docs/testing/evidencias/README.md`](evidencias/README.md) al finalizar cada ciclo.
- Anonimizar datos personales antes de compartir material.

## 6. Consideraciones adicionales
- Utilizar el usuario de recepción únicamente para pruebas coordinadas con el equipo de operaciones.
- Limpiar reservas creadas durante la jornada para mantener base de datos estable.
- Documentar tiempos reales de ejecución en el reporte diario.

## 7. Contacto
- **QA Lead:** Daniel Ruiz – `druiz@hotelpacific.com`
- **Soporte de infraestructura:** InfraOps – `infra@hotelpacific.com`
