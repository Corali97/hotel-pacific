
# Hotel Pacific

Este repositorio contiene el prototipo funcional del sistema de reservas del Hotel Pacific. Incluye la documentación de diseño y un MVP construido con Python, SQLite y un servidor WSGI ligero que permite registrar reservas básicas desde un formulario web.

## 🚀 Cómo ejecutar el MVP


1. Ejecutar la aplicación:
	```bash
	python app/app.py
	```
2. Abrir `http://127.0.0.1:5000/` en el navegador para acceder al formulario de reservas.

La base de datos SQLite (`app/reservations.db`) se crea automáticamente la primera vez que se levanta el servidor.

## 📂 Contenido del Repositorio
- `/app` → Código fuente del MVP conectado a la base de datos.
- `/docs/uml` → Diagramas UML.
- `/docs/vistas` → Mockups, prototipos y capturas de pantalla del MVP en ejecución.
- `/docs/testing` → Reportes de QA (formato PRY3211), manual de usuario de testing y referencias a evidencias.
- `/docs/DOD` → Planilla Definition of Done.
- `/design` → Archivos de diseño.

## 🧪 Escenarios probados

Consulta `docs/testing/PRY3211_Exp3_S8_Formato_de_respuestas.md` para revisar las pruebas realizadas sobre las historias de usuario del MVP y `docs/testing/Manual_de_Usuario_Testing.md` para replicar los flujos cubiertos.
