# Proyecto Isard - Gestor de Máquinas Virtuales

## Descripción del Proyecto

Este proyecto es una aplicación web desarrollada en **Python** utilizando el framework **Flask**. Su propósito principal es gestionar y organizar máquinas virtuales (VMs) de IsardVDI, un sistema de virtualización basado en la nube. Creada por la alumna de ciberseguridad Unai Urzainqui, conocida en github como [tears-mysthrala](https://github.com/tears-mysthrala).

### Funcionalidades Principales

- **Gestión de VMs**: La aplicación se conecta a la API de IsardVDI (`https://cloud.uni.eus/api/v3`) para obtener la lista de escritorios (desktops) del usuario.
- **Organización en Carpetas**: Permite agrupar las VMs en carpetas personalizadas, almacenadas en un archivo JSON (`folders.json`).
- **Interfaz Web**: Proporciona una interfaz web para visualizar, organizar y gestionar las máquinas virtuales.
- **Cache de VMs**: Mantiene un caché en memoria de las máquinas para optimizar las consultas.

### Tecnologías Utilizadas

- **Lenguaje**: Python 3.9
- **Framework Web**: Flask 2.3.3
- **Bibliotecas**:
  - `requests` 2.31.0: Para realizar peticiones HTTP a la API
  - `urllib.parse`: Para decodificar URLs
  - `json`: Para manejar archivos JSON
  - `os`: Para acceder a variables de entorno
- **Contenedorización**: Docker y Docker Compose para despliegue
- **Almacenamiento**: Archivo JSON (`folders.json`) para persistir las carpetas y asignaciones de máquinas

### Estructura del Proyecto

```bash
/home/kalista/isard/
├── app.py                 # Archivo principal de la aplicación Flask
├── requirements.txt       # Dependencias de Python
├── Dockerfile             # Configuración para construir la imagen Docker
├── docker-compose.yml     # Configuración para ejecutar el contenedor
├── folders.json          # Archivo JSON con las carpetas y máquinas asignadas
└── __pycache__/          # Archivos compilados de Python (generado automáticamente)
```

### Configuración y Despliegue

1. **Variables de Entorno**: Requiere una variable `API_KEY` con el token de autenticación para la API de IsardVDI.
2. **Archivo .env**: Se utiliza un archivo `.env` para configurar las variables de entorno (referenciado en `docker-compose.yml`).
3. **Puerto**: La aplicación expone el puerto 5000.
4. **Despliegue**: Se puede ejecutar localmente con `python app.py` o utilizando Docker Compose.

### Proceso de Desarrollo

El desarrollo de esta aplicación fue un proceso iterativo de prueba y error, marcado por la falta de documentación oficial y la necesidad de explorar directamente las capacidades de la API de IsardVDI. A continuación, se describe cómo se llegó al estado actual:

1. **Exploración Inicial de la API**: Comenzamos realizando queries básicas a la API (`https://cloud.uni.eus/api/v3`) para entender qué endpoints estaban disponibles. Usando herramientas como `curl` o scripts simples en Python con `requests`, probamos diferentes rutas y métodos HTTP para mapear las funcionalidades expuestas.

2. **Investigación de Versiones**: No había documentación clara sobre qué versión de la API se estaba utilizando. A través de prueba y error, descubrimos que la versión v3 era la activa, probando diferentes paths como `/v1`, `/v2` y `/v3` hasta encontrar respuestas válidas. Esto implicó manejar errores 404 y 401 para identificar credenciales correctas y endpoints funcionales.

3. **Descifrado de Documentación Inexistente**: La documentación oficial era prácticamente inexistente o muy limitada. Para entender la estructura de las respuestas JSON y los parámetros requeridos, tuvimos que analizar directamente las respuestas de la API. Esto incluyó inspeccionar campos como `interfaces`, `guest_properties` y `ips` para extraer información relevante sobre las máquinas virtuales.

4. **Investigación en GitLab**: Ante fallos persistentes (como errores de autenticación o datos incompletos), recurrimos al repositorio público de IsardVDI en GitLab. Exploramos el código fuente para entender cómo funcionaba internamente la API, qué campos se devolvían y cómo se estructuraban las peticiones. Esto nos permitió ajustar nuestros queries para obtener datos completos y manejar casos edge.

5. **Iteraciones de Prueba y Error**: Cada nueva funcionalidad se implementó probando diferentes combinaciones de headers, parámetros y métodos. Por ejemplo:
   - Probamos diferentes formatos de autenticación hasta encontrar que `Bearer {API_KEY}` funcionaba.
   - Experimentamos con diferentes formas de parsear las IPs de las interfaces de red.
   - Ajustamos el manejo de errores para casos donde la API devolvía datos inesperados.

6. **Optimización y Refinamiento**: Una vez que los queries básicos funcionaban, se agregó lógica para cachear datos, organizar en carpetas y construir la interfaz web. Cada paso involucró más pruebas para asegurar estabilidad.

Este enfoque de desarrollo "hands-on" resultó en una aplicación funcional, pero destaca la importancia de una mejor documentación en proyectos de código abierto para facilitar el desarrollo de integraciones.
