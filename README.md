
# 🌍 Proyecto Flask de Sistema Bite

Este proyecto es una aplicación web construida con Flask que incluye soporte multilenguaje utilizando Flask-Babel. 
Además, está preparado para pruebas automatizadas y despliegue con Docker.

---

## 🔧 Requisitos

- Python 3.12
- Docker (opcional)

---

## 📦 Instalación del Entorno

```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución del Proyecto
### 1. Configurar el entorno
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
SECRET_KEY=""
BABEL_DEFAULT_LOCALE=""
COVERAGE_CONFIGS=.coveragerc
```

### 2. Ejecutar la aplicación

```
Ejecuta la aplicacion desde el directorio raíz del proyecto: src/app.py
```

## 🌐 Configuración de Flask-Babel

### 1. Instalar Flask-Babel (incluido en `requirements.txt`)

```bash
pip install Flask-Babel
```

### 2. Crear estructura de directorios para traducciones

```bash
translations
translations/en/LC_MESSAGES
translations/es/LC_MESSAGES
```

> Repite este patrón para cada idioma soportado (`fr`, `de`, `pt`, etc.)

### 3. Crear archivo `babel.cfg` en la raíz del proyecto

```ini
[jinja2: templates/**.html]
[python: **.py]
```

Este archivo indica a Babel qué archivos analizar.

### 4. Extraer los textos traducibles

```bash
pybabel extract -F babel.cfg -o messages.pot .
```

Este comando genera el archivo base `messages.pot` con los textos encontrados.

### 5. Inicializar archivos de traducción

Para español, por ejemplo:

```bash
pybabel init -i messages.pot -d src/translations -l es
```

Esto crea el archivo `messages.po` en `translations/es/LC_MESSAGES`.

> Si ya tienes un `.po` y solo necesitas actualizarlo con nuevos textos:

```bash
pybabel update -d src/translations -i messages.pot -l es
```

### 6. Traducir los textos

Abre `translations/es/LC_MESSAGES/messages.po` y edita cada entrada `msgstr` con su traducción:

```po
msgid "Hello"
msgstr "Hola"
```

### 7. Compilar los archivos `.po` a `.mo`

```bash
pybabel compile -d src/translations
```

> Esto es necesario para que Flask-Babel utilice las traducciones.


## 🧪 Pruebas Automatizadas

> ✍️ El proyecto cuenta con pruebas unitarias como pruebas de IU.
> Para Ejecutar estas últimas necesitas de los drivers de los navegadores correspondientes.
> Puedes ejecutar las pruebas con `pytest` o el framework de tu elección.

Por ejemplo:

```bash
pytest tests/
```

- Las pruebas se encuentran en la carpeta `tests/`.
- Asegúrate de que tienes las dependencias de `requirements.txt`.
- Asegúrate de que los drivers de Selenium acceden a la URL en la cual se está ejecutando el sistema. 
---

## 🐳 Ejecución con Docker

### 1. Crear imagen

Asegúrate de tener el `Dockerfile`.

```bash
docker build -t bite-app .
```

### 2. Ejecutar contenedor

```bash
docker run -p 5000:5000 bite-app
```

> Puedes modificar el puerto o usar variables de entorno para producción.

---

La app estará disponible en: [http://localhost:5000](http://localhost:5000)

---

## ✅ TODO

- [ ] Agregar más idiomas
