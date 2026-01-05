# TechCorp Portal - HackConRD 2026 Web Security Workshop

Bienvenido al repositorio oficial del taller de Seguridad Web en **HackConRD 2026**.

Esta es una aplicación de práctica diseñada específicamente con fines educativos. El objetivo principal es proporcionar un entorno controlado para aprender a detectar, analizar y explotar vulnerabilidades críticas en aplicaciones modernas.

---

## Inicio Rapido

### Con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/ndivilight/hackconrd-web-workshop.git
cd hackconrd-web-workshop

# Construir e iniciar
docker-compose up --build

# Acceder en: http://localhost:8080
```
---

## Comandos Utiles

```bash
# Reiniciar la base de datos
cd hackconrd-web-workshop
docker-compose down
rm -f data/portal.db
docker-compose up --build

# Ver logs 
cd hackconrd-web-workshop
docker-compose logs -f

# Acceder al contenedor
cd hackconrd-web-workshop
docker exec -it techcorp-portal /bin/bash

# Detener
cd hackconrd-web-workshop
docker-compose down
```

---

## Credenciales por Defecto

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `admin123` | Administrador |
| `jsmith` | `password123` | Empleado |
| `test` | `test` | Pruebas |

---

## Objetivos del Taller

El laboratorio está estructurado para cubrir los vectores de ataque mas comunes del OWASP Top 10:

| # | Vulnerabilidad | Ubicacion | Dificultad |
|---|----------------|-----------|------------|
| 1 | **SQL Injection** | Login, Employee Search | Media |
| 2 | **Cross-Site Scripting (XSS)** | Announcements | Facil |
| 3 | **IDOR** | Employee Profiles/Payslips | Facil |
| 4 | **Directory Traversal** | Document Downloads | Media |
| 5 | **Command Injection** | Network Tools | Media |
| 6 | **SSTI** | Report Generator | Dificil |
| 7 | **JWT Vulnerabilities** | API Endpoints | Dificil |

---

## Estructura del Proyecto

```
hackconrd-web-workshop/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuracion
│   ├── models.py            # Modelos de base de datos
│   ├── auth.py              # Utilidades JWT
│   ├── routes/              # Endpoints de la aplicacion
│   │   ├── auth.py          # Login/Logout (SQLi)
│   │   ├── employees.py     # Directorio (SQLi, IDOR)
│   │   ├── announcements.py # Anuncios (XSS)
│   │   ├── documents.py     # Documentos (Dir Traversal)
│   │   ├── tools.py         # Herramientas IT (Cmd Injection)
│   │   ├── reports.py       # Reportes (SSTI)
│   │   └── api.py           # API REST (JWT vulns)
│   ├── templates/           # Plantillas HTML
│   └── static/              # CSS, JS
├── data/
│   ├── documents/           # Archivos descargables
│   └── portal.db            # Base de datos SQLite
├── scripts/
│   └── init_db.py           # Script de inicializacion
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Sistema de Dificultad

La aplicación incluye tres niveles de dificultad que controlan la cantidad de pistas:

| Nivel | Descripción |
|-------|-------------|
| **Easy** | Pistas en HTML, mensajes de error verbosos, payloads sugeridos |
| **Medium** | Pistas sutiles en comentarios, algunos errores |
| **Hard** | Sin pistas, errores genéricos, comportamiento realista |

Cambiar dificultad: Click en el menu de dificultad en la barra de navegación.

---

## Herramientas Requeridas

| Herramienta | Proposito |
|-------------|-----------|
| **Burp Suite Community** | Intercepcion y manipulacion de trafico HTTP |
| **ffuf** | Fuzzing de directorios y parametros |
| **cURL** | Peticiones HTTP desde terminal |
| **sqlmap** | Automatizacion de SQL Injection |
| **jwt_tool** | Analisis y explotacion de JWT |

---

## Aviso de Etica y Uso

> **ADVERTENCIA:** Este entorno ha sido creado **exclusivamente con fines academicos**.
>
> El uso de las tecnicas aqui descritas sobre sistemas reales sin autorizacion previa es **ilegal y poco etico**.
>
> El objetivo es formar mejores profesionales para defender y construir aplicaciones mas seguras.

---

**Organizado por:** HackConRD 2026
**Facilitador:** Nelson Colon / Bry Mano Negra

---

## Licencia

Este proyecto es solo para fines educativos. Úselo responsablemente.
