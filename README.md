# 🛡️ Enterprise API Security Scanner

<p align="center">
  <b>Un escáner automatizado de vulnerabilidades para APIs de alto rendimiento, diseñado bajo el estándar OWASP API Security Top 10.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Asyncio-Enabled-orange.svg" alt="Asyncio">
  <img src="https://img.shields.io/badge/OWASP-Top%2010-red.svg" alt="OWASP Top 10">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

---

## 🚀 ¿Qué es y qué hace?

**Enterprise API Security Scanner** es una herramienta de seguridad ofensiva y auditoría automatizada desarrollada en Python. Su objetivo principal es ayudar a equipos de desarrollo, analistas de seguridad y entusiastas de la ciberseguridad a identificar fallos críticos en arquitecturas de microservicios y APIs REST **antes de que lleguen a producción**.

A diferencia de los escáneres web tradicionales, esta herramienta lee directamente las definiciones de la API (especificaciones **OpenAPI / Swagger**) para mapear endpoints, parámetros y métodos de forma inteligente, ejecutando pruebas de concepto (PoC) concurrentes y generando reportes ejecutivos listos para auditoría.

---

## 🔍 Vectores de Ataque Implementados (OWASP API Top 10)

El motor evalúa las vulnerabilidades más críticas que afectan a las APIs modernas:

| Código OWASP | Vulnerabilidad | Descripción de la Prueba |
| :--- | :--- | :--- |
| **API1:2023** | **Broken Object Level Authorization (BOLA)** | Manipula identificadores numéricos y UUIDs en las rutas (`/users/1` $\rightarrow$ `/users/2`) para verificar si el servidor expone datos de otros usuarios sin validar permisos de sesión. |
| **API2:2023** | **Broken Authentication** | Evalúa si endpoints protegidos responden exitosamente ante peticiones que carecen completamente de cabeceras de autorización (`Bearer Token`). |
| **API3:2023** | **Excessive Data Exposure** | Analiza las respuestas JSON en busca de palabras clave sensibles filtradas indebidamente (`password_hash`, `secret`, `credit_card`, `ssn`). |

---

## 🛠️ Arquitectura del Proyecto

El proyecto está diseñado bajo un modelo modular y altamente extensible:

```text
api-security-scanner/
│
├── scanner/
│   ├── __init__.py        # Inicializador del paquete
│   ├── parser.py          # Lector y extractor de especificaciones OpenAPI (JSON/YAML)
│   ├── engine.py          # Motor asíncrono de ataques y pruebas de seguridad
│   └── reporter.py        # Generador de reportes en consola (Rich), JSON y HTML
│
├── main.py                # Interfaz de Línea de Comandos (CLI) principal
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación oficial

```
## 📦 Instalación y Configuración
Sigue estos pasos para clonar y poner en marcha el entorno de pruebas en tu máquina local:

1. Clonar el repositorio
Bash
git clone [https://github.com/fazzztos11-gg/api-security-scanner.git](https://github.com/fazzztos11-gg/api-security-scanner.git)
cd api-security-scanner
2. Crear y activar un entorno virtual (Recomendado)
Bash
# En Linux / macOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
3. Instalar las dependencias
Bash
pip install -r requirements.txt


## 🖥️ Guía de Ejecución y Uso
El script cuenta con una interfaz de línea de comandos (CLI) intuitiva basada en parámetros.

Opciones de la CLI:
--spec: (Requerido) Ruta al archivo de especificación OpenAPI (.json o .yaml).

--url: (Opcional) URL base de la API a escanear (si no se define, el escáner la extraerá automáticamente del archivo spec).

--token: (Opcional) Token JWT o Bearer de autorización para auditar endpoints protegidos.

Ejemplos de Uso:
📌 Ejemplo 1: Escaneo local utilizando la URL definida en el archivo Swagger
Bash
python main.py --spec examples/swagger.json
📌 Ejemplo 2: Escaneo apuntando a un entorno externo con autenticación Bearer
Bash
python main.py --spec swagger.yaml --url [https://api.staging-empresa.com](https://api.staging-empresa.com) --token "eyJhbGciOiJIUzI1NiIsIn..."


## 📊 Reportes Generados
Al finalizar el escaneo, la herramienta genera automáticamente dos tipos de salida:

Consola Interactiva: Una tabla colorida y detallada con los hallazgos críticos utilizando la librería rich.

Archivos de Reporte:

report.json: Ideal para integrar en pipelines de integración continua (CI/CD).

report.html: Un informe visual moderno y estilizado para presentar con métricas de severidad.


## 🗺️ Roadmap y Próximas Mejoras

[ ] Soporte para pruebas de Rate Limiting / Brute Force (API4).

[ ] Inclusión de validación para Mass Assignment (API6).

[ ] Exportación directa de reportes en formato PDF.

[ ] Interfaz gráfica web opcional (Dash / Streamlit).

## 👤 Autor
Desarrollado con fines educativos y de investigación en ciberseguridad por williams-rgb.

## ⚠️ Aviso Legal
Esta herramienta ha sido desarrollada estrictamente con fines educativos y para auditorías de seguridad autorizadas (Ethical Hacking / Bug Bounty). Los autores no se hacen responsables del mal uso o de los daños causados por el incumplimiento de las leyes aplicables.
