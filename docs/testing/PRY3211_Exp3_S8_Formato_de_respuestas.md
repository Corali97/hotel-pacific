# PRY3211 Exp3 S8 - Formato de respuestas de pruebas funcionales

## Resumen ejecutivo
Las siguientes ejecuciones corresponden al ciclo de validación funcional del MVP de Hotel Pacific realizado durante la semana 8. Los objetivos del ciclo fueron validar el acceso autenticado, el flujo principal de reservas y la gestión de cancelaciones desde el panel del huésped.

| Fecha | Usuario de prueba | Escenario | Pasos clave | Resultado | Observaciones | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| 2024-05-07 | Laura Méndez (QA Intern) | Inicio de sesión con credenciales válidas | 1. Navegar a `/login`.<br>2. Ingresar `qa.huesped@hotelpacific.com` / `Pacific#2024`.<br>3. Confirmar acceso al panel del huésped. | Aprobado | Se visualiza dashboard con widgets activos. | [Captura 01](evidencias/README.md#captura-01) |
| 2024-05-07 | Daniel Ruiz (QA Lead) | Creación de reserva estándar | 1. Autenticarse como huésped.<br>2. Abrir "Reservar habitación".<br>3. Seleccionar Suite Coral (2 noches).<br>4. Confirmar pago con tarjeta de prueba. | Aprobado con observaciones | El modal de confirmación tarda ~4 s en cerrar. | [Video 01](evidencias/README.md#video-01) |
| 2024-05-08 | Laura Méndez (QA Intern) | Cancelación de reserva vigente | 1. Iniciar sesión.<br>2. Abrir "Mis reservas".<br>3. Seleccionar reserva #4571.<br>4. Confirmar cancelación. | Rechazado | Mensaje de error HTTP 409 al reintentar cancelaciones consecutivas. | [Ticket 409](evidencias/README.md#ticket-409) |

## Detalle de ejecuciones

### Escenario: Inicio de sesión con credenciales válidas
- **Precondiciones:** Usuario registrado con rol huésped, ambiente QA disponible.
- **Pasos ejecutados:**
  1. Acceder a `https://qa.hotelpacific.io/login`.
  2. Completar formulario de acceso con credenciales de huésped QA.
  3. Hacer clic en "Ingresar" y esperar la redirección automática.
- **Resultado obtenido:** Redirección a `/dashboard` en 2.1 s; widgets de resumen visibles.
- **Notas adicionales:** Se verificó que la cookie `hp_session` tenga vigencia de 30 minutos.
- **Evidencia:** Captura de pantalla disponible en la referencia [Captura 01](evidencias/README.md#captura-01).

### Escenario: Creación de reserva estándar
- **Precondiciones:** Usuario autenticado; disponibilidad configurada para Suite Coral.
- **Pasos ejecutados:**
  1. Ingresar al módulo "Reservar habitación" desde el menú lateral.
  2. Seleccionar fechas de entrada 10/05/2024 y salida 12/05/2024.
  3. Elegir método de pago "Tarjeta tokenizada".
  4. Confirmar la operación y esperar notificación.
- **Resultado obtenido:** Reserva creada exitosamente (ID 4571) y notificación push emitida.
- **Notas adicionales:** Se detectó latencia en el modal de confirmación; se sugirió ticket de performance.
- **Evidencia:** Registro audiovisual consignado en [Video 01](evidencias/README.md#video-01).

### Escenario: Cancelación de reserva vigente
- **Precondiciones:** Reserva ID 4571 creada con anterioridad y estado "Confirmada".
- **Pasos ejecutados:**
  1. Abrir el historial de reservas desde el dashboard.
  2. Seleccionar la reserva ID 4571.
  3. Hacer clic en "Cancelar" y confirmar la acción.
- **Resultado obtenido:** Primer intento exitoso, pero el servicio responde `409 Conflict` en reintentos inmediatos.
- **Notas adicionales:** Se registró issue en Jira con prioridad Alta (HP-221) para revisar manejo idempotente.
- **Evidencia:** Captura de logs y seguimiento en [Ticket 409](evidencias/README.md#ticket-409).

## Seguimiento y próximos pasos
- Repetir pruebas de cancelación tras corregir el manejo de reintentos en el servicio de reservas.
- Ejecutar pruebas exploratorias en el flujo de modificación de datos personales.
- Integrar las evidencias al repositorio una vez se anonimicen datos sensibles.

## Firmas de conformidad
- **QA Lead:** Daniel Ruiz – 08/05/2024
- **Product Owner:** Mariana Ortega – 08/05/2024
