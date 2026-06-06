# 🎵 MusicItself — Biblioteca Musical Personal con API REST

> Aplicación web full-stack para gestionar tu colección de canciones, artistas y playlists.  
> Backend con FastAPI · Base de datos PostgreSQL · Imágenes en Supabase · Interfaz con Jinja2

**Autor:** Juan Diego Lozano  
**Repositorio:** [github.com/2naain/DEV_Musicmanager](https://github.com/2naain/DEV_Musicmanager)  
**Despliegue:** [musiicitself.onrender.com](https://musiicitself.onrender.com)  
**Institución:** Universidad Católica de Colombia — 2026

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Tecnologías](#-tecnologías)
- [Instalación local](#-instalación-local)
- [Variables de entorno](#-variables-de-entorno)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Modelo de datos](#-modelo-de-datos)
- [API REST](#-api-rest)
- [Frontend (Jinja2)](#-frontend-jinja2)
- [Imágenes](#-módulo-de-imágenes)
- [Despliegue](#-despliegue)

---

## 📖 Descripción

MusicItself es una aplicación web orientada a la gestión de una biblioteca musical personal. Permite al usuario administrar canciones, artistas y listas de reproducción (playlists) mediante:

- Una **API REST** documentada automáticamente con Swagger UI (OpenAPI 3.0)
- Una **interfaz web** renderizada en el servidor con Jinja2 (SSR)
- **Almacenamiento de imágenes** en la nube con Supabase Storage
- **Persistencia** en PostgreSQL serverless (Neon DB)
- **Despliegue continuo** desde GitHub hacia Render

El sistema implementa borrado lógico (`is_active`) en todas las entidades, búsqueda parcial insensible a mayúsculas con ILIKE, y conversión de duración al formato `mm:ss` mediante un filtro personalizado de Jinja2.

---

## 🛠 Tecnologías

| Tecnología | Rol | Versión |
|---|---|---|
| Python | Lenguaje principal del backend | 3.12 |
| FastAPI | Framework web y API REST | 0.115.12 |
| SQLModel | ORM + validación (SQLAlchemy + Pydantic) | 0.0.22 |
| PostgreSQL — Neon DB | Base de datos relacional serverless | — |
| Supabase Storage | Almacenamiento de imágenes en la nube | 2.15.1 |
| Jinja2 | Motor de plantillas HTML (SSR) | 3.1.6 |
| Uvicorn | Servidor ASGI | 0.34.0 |
| Render | Plataforma de despliegue en la nube | — |

---

## 🚀 Instalación local

**1. Clona el repositorio:**
```bash
git clone https://github.com/2naain/DEV_Musicmanager.git
cd DEV_Musicmanager
```

**2. Instala las dependencias:**
```bash
pip install -r requirements.txt
```

**3. Configura las variables de entorno** (ver sección siguiente)

**4. Ejecuta la aplicación:**
```bash
uvicorn main:app --reload
```

La app queda disponible en `http://localhost:8000`  
La documentación interactiva en `http://localhost:8000/docs`

**5. (Opcional) Poblar la base de datos con datos de prueba:**
```bash
python seed.py
```

---

## 🔐 Variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Conexión a PostgreSQL (Neon DB)
DATABASE_URL_NEON=postgresql://user:password@host/dbname

# Credenciales de Supabase Storage
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Entorno: 'dev' crea tablas al iniciar, 'prod' no
ENV=dev
```

> ⚠️ El archivo `.env` está incluido en `.gitignore`. Nunca lo subas al repositorio.

---

## 📁 Estructura del proyecto

```
MusicItself/
│
├── main.py                           # Punto de entrada: todos los endpoints API y frontend
├── db.py                             # Conexión a PostgreSQL (Neon DB) y ciclo de sesiones
├── utils.py                          # Almacenamiento de imágenes (local y Supabase)
├── seed.py                           # Población inicial de datos para desarrollo y pruebas
│
├── models/
│   ├── song.py                       # SongBase, SongID, SongUpdate
│   ├── artist.py                     # ArtistBase, ArtistID, ArtistUpdate
│   ├── playlist.py                   # PlaylistBase, PlaylistID, PlaylistUpdate
│   ├── song_genres.py                # Enum SongGenre (8 géneros válidos)
│   └── playlist_song.py              # Tabla intermedia PlaylistSong (N:M)
│
├── operations/
│   ├── operations_song_db.py         # CRUD canciones: ILIKE, borrado lógico, update parcial
│   ├── operations_artist_db.py       # CRUD artistas: búsqueda por nombre, borrado lógico
│   └── operations_playlist_db.py     # CRUD playlists + gestión de canciones asociadas
│
├── templates/                        # Plantillas Jinja2 para todas las vistas HTML
│   ├── base.html                     # Layout base con navbar, header y footer
│   ├── home.html                     # Inicio: estadísticas y canciones recientes
│   ├── all_songs.html                # Catálogo de canciones
│   ├── one_song.html                 # Detalle de canción
│   ├── create_song.html              # Formulario de creación de canción
│   ├── all_artists.html              # Listado de artistas
│   ├── one_artist.html               # Detalle de artista
│   ├── create_artist.html            # Formulario de creación de artista
│   ├── all_playlists.html            # Listado de playlists
│   ├── one_playlist.html             # Detalle de playlist con canciones
│   └── create_playlist.html          # Formulario de creación de playlist
│
├── requirements.txt                  # Dependencias Python
└── runtime.txt                       # Versión de Python para Render
```

---

## 🗄 Modelo de datos

### 🎵 Canción (`SongID`)

| Campo | Tipo | Restricción | Descripción |
|---|---|---|---|
| id | Integer | PK, Auto | Identificador único |
| title | String | 2–100 chars | Título de la canción |
| genre | Enum (SongGenre) | Opcional | Género musical |
| duration | Integer | 1–10 000 seg | Duración en segundos |
| artist_id | Integer | FK → ArtistID | Artista asociado |
| in_playlist | Boolean | Default: False | Indica si está en alguna playlist |
| is_active | Boolean | Default: True | Borrado lógico |
| image_url | String | Máx. 500 chars | URL pública de imagen en Supabase |

**Géneros válidos (`SongGenre`):** `pop` · `rock` · `jazz` · `hiphop` · `electronica` · `clasica` · `reggaeton` · `metal`

### 🎤 Artista (`ArtistID`)

| Campo | Tipo | Restricción | Descripción |
|---|---|---|---|
| id | Integer | PK, Auto | Identificador único |
| name | String | 2–100 chars | Nombre del artista |
| description | String | Opcional | Descripción biográfica |
| image_url | String | Máx. 500 chars | URL pública de imagen en Supabase |
| is_active | Boolean | Default: True | Borrado lógico |

### 📂 Playlist (`PlaylistID`)

| Campo | Tipo | Restricción | Descripción |
|---|---|---|---|
| id | Integer | PK, Auto | Identificador único |
| name | String | 2–100 chars | Nombre de la playlist |
| description | String | Máx. 500 chars | Descripción opcional |
| is_active | Boolean | Default: True | Borrado lógico |

### 🔗 Relación Playlist ↔ Canción (`PlaylistSong`)

Tabla intermedia con clave primaria compuesta `(playlist_id, song_id)` que implementa la relación muchos-a-muchos entre playlists y canciones. Garantiza integridad referencial y evita canciones duplicadas dentro de una misma playlist.

---

## 🌐 API REST

La documentación interactiva completa está disponible en `/docs` (Swagger UI).  
Todos los endpoints de listado soportan el parámetro `?q=` para búsqueda parcial insensible a mayúsculas.

### 🎵 Songs API — `/song`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/song` | Lista todas las canciones activas. Soporta `?q=` |
| `POST` | `/song` | Crea una nueva canción con imagen (`multipart/form-data`) |
| `GET` | `/song/{id}` | Obtiene una canción por ID |
| `PATCH` | `/song/{id}` | Actualiza parcialmente una canción |
| `DELETE` | `/song/{id}` | Borrado lógico (`is_active = False`) |

### 🎤 Artists API — `/artist`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/artist` | Lista todos los artistas activos. Soporta `?q=` |
| `POST` | `/artist` | Registra un nuevo artista (JSON body) |
| `GET` | `/artist/{id}` | Obtiene un artista por ID |
| `PATCH` | `/artist/{id}` | Actualiza los datos de un artista |
| `DELETE` | `/artist/{id}` | Borrado lógico de un artista |

### 📂 Playlists API — `/playlist`

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/playlist` | Lista todas las playlists activas |
| `POST` | `/playlist` | Crea una nueva playlist (JSON body) |
| `GET` | `/playlist/{id}` | Obtiene una playlist por ID |
| `PATCH` | `/playlist/{id}` | Actualiza una playlist existente |
| `DELETE` | `/playlist/{id}` | Borrado lógico de una playlist |
| `POST` | `/playlist/{playlist_id}/song/{song_id}` | Agrega una canción a una playlist |
| `DELETE` | `/playlist/{playlist_id}/song/{song_id}` | Elimina una canción de una playlist |
| `GET` | `/playlist/{id}/songs` | Lista todas las canciones de una playlist |

### 🖼 Images API — `/image`

| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/image/local` | Guarda imagen en el filesystem local *(solo dev)* |
| `POST` | `/image/remote` | Sube imagen a Supabase Storage y retorna URL pública |

> ⚠️ `/image/local` no funciona en producción (Render usa filesystem efímero). En producción siempre usar `/image/remote`.

---

## 💻 Frontend (Jinja2)

Rutas que devuelven páginas HTML renderizadas en el servidor. Comparten la misma capa de operaciones de base de datos que la API REST.

### Inicio

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Panel estadístico (total canciones, artistas, playlists) + canciones recientes |

### 🎵 Canciones

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/songs` | Catálogo completo con buscador `?q=` |
| `GET` | `/songs/create` | Formulario de creación de canción |
| `POST` | `/songs/create` | Procesa el formulario y redirige a `/songs` |
| `GET` | `/songs/{id}` | Detalle de una canción |

### 🎤 Artistas

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/artists` | Listado de artistas con buscador `?q=` |
| `GET` | `/artists/create` | Formulario de creación de artista |
| `POST` | `/artists/create` | Procesa el formulario y redirige a `/artists` |
| `GET` | `/artists/{id}` | Detalle de artista con imagen y descripción biográfica |

### 📂 Playlists

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/playlists` | Listado de playlists con buscador `?q=` |
| `GET` | `/playlists/create` | Formulario de creación de playlist |
| `POST` | `/playlists/create` | Procesa el formulario y redirige a `/playlists` |
| `GET` | `/playlists/{id}` | Detalle de playlist con canciones asociadas |
| `POST` | `/playlists/{id}/add` | Agrega canción a la playlist desde formulario |
| `POST` | `/playlists/{id}/remove/{song_id}` | Quita una canción de la playlist |

---

## 🖼 Módulo de imágenes

El sistema maneja dos estrategias según el entorno:

- **`save_img_local`** — Guarda el archivo en el filesystem local. Solo para desarrollo.
- **`save_img_remote`** — Valida el tipo MIME (`image/*`), sube el binario al bucket de Supabase mediante el cliente oficial de Python, y persiste la URL pública en el campo `image_url` de la entidad correspondiente.

---

## ☁️ Despliegue

La infraestructura de producción se compone de tres servicios cloud:

| Servicio | Rol | URL / Acceso |
|---|---|---|
| **Render** | Hosting de la app FastAPI | `musiicitself.onrender.com` |
| **Neon DB** | PostgreSQL serverless | Conexión via `DATABASE_URL_NEON` |
| **Supabase Storage** | Almacenamiento de imágenes | URLs públicas en `image_url` |

Render detecta cambios en la rama `main` de GitHub y despliega automáticamente la nueva versión (CI/CD básico).

### Variables de entorno en producción (Render)

```
DATABASE_URL_NEON  →  cadena de conexión Neon DB
SUPABASE_URL       →  URL del proyecto Supabase
SUPABASE_KEY       →  API key de Supabase
ENV                →  prod
```

---

## 📚 Documentación interactiva

Swagger UI disponible en producción:  
👉 **[musiicitself.onrender.com/docs](https://musiicitself.onrender.com/docs)**

Incluye todos los endpoints con esquemas de entrada/salida, ejemplos y códigos de respuesta. No requiere herramientas externas como Postman.

---

*Universidad Católica de Colombia · Facultad de Ingeniería de Sistemas y Computación · 2026*
