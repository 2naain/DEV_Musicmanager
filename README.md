# MusicItself — Biblioteca Musical Personal con API REST

**Autor:** Juan Diego Lozano  
**Repositorio:** [github.com/2naain/DEV_Musicmanager](https://github.com/2naain/DEV_Musicmanager)  
**Despliegue:** [musiicitself.onrender.com](https://musiicitself.onrender.com)  
**Institución:** Universidad Católica de Colombia — 2026

---

## Descripción

MusicItself es una aplicación web para la gestión de una biblioteca musical personal. Permite administrar canciones, artistas y playlists mediante una interfaz web (Jinja2 SSR) y una API REST documentada con Swagger UI.

**Stack:** FastAPI · SQLModel · PostgreSQL (Neon DB) · Supabase Storage · Jinja2 · Render

---

## Instalación y ejecución local

```bash
git clone https://github.com/2naain/DEV_Musicmanager.git
cd DEV_Musicmanager
pip install -r requirements.txt
```

Crea un archivo `.env` con las siguientes variables:

```
DATABASE_URL_NEON=<tu_cadena_de_conexion>
SUPABASE_URL=<tu_url_de_supabase>
SUPABASE_KEY=<tu_api_key_de_supabase>
ENV=dev
```

Ejecuta la aplicación:

```bash
uvicorn main:app --reload
```

La aplicación quedará disponible en `http://localhost:8000`.  
La documentación interactiva (Swagger UI) estará en `http://localhost:8000/docs`.

---

## Endpoints API REST

### Songs API — `/song`

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/song` | Lista todas las canciones activas. Soporta `?q=` para búsqueda |
| POST | `/song` | Crea una nueva canción con imagen (`multipart/form-data`) |
| GET | `/song/{id}` | Obtiene una canción por ID |
| PATCH | `/song/{id}` | Actualiza parcialmente una canción |
| DELETE | `/song/{id}` | Borrado lógico (`is_active=False`) |

### Artists API — `/artist`

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/artist` | Lista todos los artistas activos. Soporta `?q=` para búsqueda |
| POST | `/artist` | Registra un nuevo artista (JSON body) |
| GET | `/artist/{id}` | Obtiene un artista por ID |
| PATCH | `/artist/{id}` | Actualiza datos de un artista |
| DELETE | `/artist/{id}` | Borrado lógico de un artista |

### Playlists API — `/playlist`

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/playlist` | Lista todas las playlists activas |
| POST | `/playlist` | Crea una nueva playlist (JSON body) |
| GET | `/playlist/{id}` | Obtiene una playlist por ID |
| PATCH | `/playlist/{id}` | Actualiza una playlist |
| DELETE | `/playlist/{id}` | Borrado lógico de una playlist |
| POST | `/playlist/{playlist_id}/song/{song_id}` | Agrega una canción a una playlist |
| DELETE | `/playlist/{playlist_id}/song/{song_id}` | Elimina una canción de una playlist |
| GET | `/playlist/{id}/songs` | Lista las canciones de una playlist |

### Images API — `/image`

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/image/local` | Guarda imagen en el filesystem local (solo dev) |
| POST | `/image/remote` | Sube imagen a Supabase Storage y retorna URL pública |

---

## Endpoints Frontend (Jinja2 SSR)

### Inicio

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Panel estadístico y canciones recientes |

### Canciones

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/songs` | Lista canciones. Soporta `?q=` |
| GET | `/songs/create` | Formulario de creación |
| POST | `/songs/create` | Procesa el formulario y redirige a `/songs` |
| GET | `/songs/{id}` | Detalle de una canción |

### Artistas

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/artists` | Lista artistas. Soporta `?q=` |
| GET | `/artists/create` | Formulario de creación |
| POST | `/artists/create` | Procesa el formulario y redirige a `/artists` |
| GET | `/artists/{id}` | Detalle de un artista |

### Playlists

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/playlists` | Lista playlists. Soporta `?q=` |
| GET | `/playlists/create` | Formulario de creación |
| POST | `/playlists/create` | Procesa el formulario y redirige a `/playlists` |
| GET | `/playlists/{id}` | Detalle de playlist y canciones asociadas |
| POST | `/playlists/{id}/add` | Agrega canción a playlist desde formulario |
| POST | `/playlists/{id}/remove/{song_id}` | Quita canción de playlist |

---

## Modelo de Datos

### Canción (SongID)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Identificador único |
| title | String (2–100) | Título de la canción |
| genre | Enum (SongGenre) | Género musical (opcional) |
| duration | Integer (1–10 000) | Duración en segundos |
| artist_id | Integer (FK) | Artista asociado |
| in_playlist | Boolean | Indica si está en playlist |
| is_active | Boolean | Borrado lógico |
| image_url | String (máx. 500) | URL de imagen en Supabase |

Géneros válidos: `pop`, `rock`, `jazz`, `hiphop`, `electronica`, `clasica`, `reggaeton`, `metal`

### Artista (ArtistID)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Identificador único |
| name | String (2–100) | Nombre del artista |
| description | String | Descripción del artista |
| image_url | String (máx. 500) | URL de imagen en Supabase |
| is_active | Boolean | Borrado lógico |

### Playlist (PlaylistID)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Integer (PK) | Identificador único |
| name | String (2–100) | Nombre de la playlist |
| description | String (máx. 500) | Descripción opcional |
| is_active | Boolean | Borrado lógico |

### Relación Playlist ↔ Canción (PlaylistSong)

Tabla intermedia con clave compuesta `playlist_id` + `song_id` para la relación N:M.

---

## Estructura del proyecto

```
├── main.py                          # Endpoints API REST y frontend
├── db.py                            # Conexión a PostgreSQL (Neon DB)
├── utils.py                         # Almacenamiento de imágenes
├── seed.py                          # Población inicial de datos
├── models/
│   ├── song.py                      # SongBase, SongID, SongUpdate
│   ├── artist.py                    # ArtistBase, ArtistID, ArtistUpdate
│   ├── playlist.py                  # PlaylistBase, PlaylistID, PlaylistUpdate
│   ├── song_genres.py               # Enum SongGenre
│   └── playlist_song.py             # Tabla intermedia PlaylistSong
├── operations/
│   ├── operations_song_db.py        # CRUD canciones
│   ├── operations_artist_db.py      # CRUD artistas
│   └── operations_playlist_db.py   # CRUD playlists
├── templates/                       # Plantillas Jinja2
├── requirements.txt
└── runtime.txt
```

---

## Infraestructura

| Servicio | Rol |
|----------|-----|
| Render | Hosting FastAPI — `musiicitself.onrender.com` |
| Neon DB | PostgreSQL serverless |
| Supabase Storage | Almacenamiento de imágenes (URLs públicas) |
| GitHub | Control de versiones y CI/CD con Render |

---

## Documentación interactiva

Swagger UI disponible en: [`musiicitself.onrender.com/docs`](https://musiicitself.onrender.com/docs)
