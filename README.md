# 🎵 MusicItself

Aplicación web de gestión musical desarrollada con **FastAPI**, **SQLModel** y **PostgreSQL (Neon)**, desplegada en **Render**.

- **URL:** https://musiicitself.onrender.com
- **Repositorio:** https://github.com/2naain/DEV_Musicmanager

---

## 📋 Descripción

MusicItself es una plataforma que permite gestionar canciones, artistas y playlists. El usuario puede registrar artistas con imagen, agregar canciones asociadas a un artista, crear playlists y agregar canciones a ellas. Todo esto a través de una interfaz web con formularios HTML y también mediante una API REST documentada en /docs.

---

## 🗂️ Modelos

### ArtistID
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | int | Primary key |
| name | str | Nombre del artista (2-100 chars) |
| image_url | str | URL de imagen en Supabase |
| is_active | bool | Soft delete |

### SongID
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | int | Primary key |
| title | str | Título (2-100 chars) |
| genre | SongGenre | pop, rock, jazz, hiphop, electronica, clasica, reggaeton, metal |
| duration | int | Duración en segundos |
| artist_id | int | FK → ArtistID |
| image_url | str | URL de imagen en Supabase |
| in_playlist | bool | Si está en playlist |
| is_active | bool | Soft delete |

### PlaylistID
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | int | Primary key |
| name | str | Nombre (2-100 chars) |
| description | str | Descripción (max 500 chars) |
| is_active | bool | Soft delete |

### PlaylistSong
| Campo | Tipo | Descripción |
|-------|------|-------------|
| playlist_id | int | FK → PlaylistID |
| song_id | int | FK → SongID |

---

## 📊 Diagrama de clases
ArtistID                        SongID
──────────────────              ──────────────────

id: int                       + id: int
name: str                     + title: str
image_url: str       1──N     + genre: SongGenre
is_active: bool  ──────────►  + duration: int
+ artist_id: int (FK)
+ image_url: str
+ in_playlist: bool
+ is_active: bool
│
│ N
▼
PlaylistSong (tabla intermedia)
──────────────────
+ playlist_id (FK)
+ song_id (FK)
│
│ N
▼
PlaylistID
──────────────────
+ id: int
+ name: str
+ description: str
+ is_active: bool


---

## 🔄 Diagrama de actividades
Usuario
│
├──► GET /
│        └──► Ve estadísticas + canciones recientes
│
├──► GET /songs
│        ├──► Lista canciones (con buscador ?q=)
│        └──► GET /songs/create
│                  └──► Valida datos (front + back)
│                  └──► POST /songs/create → redirige a /songs
│
├──► GET /artists
│        ├──► Lista artistas (con buscador ?q=)
│        └──► GET /artists/create
│                  └──► Valida datos (front + back)
│                  └──► POST /artists/create → redirige a /artists
│
└──► GET /playlists
├──► Lista playlists (con buscador ?q=)
├──► GET /playlists/create
│         └──► Valida datos (front + back)
│         └──► POST /playlists/create → redirige a /playlists
└──► GET /playlists/{id}
├──► Ve canciones de la playlist
├──► Agrega canción → POST /playlists/{id}/add
└──► Quita canción → POST /playlists/{id}/remove/{song_id}

---

## 🌐 Endpoints

### 🎵 Songs API
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /song | Listar canciones |
| POST | /song | Crear canción |
| GET | /song/{id} | Obtener canción |
| PATCH | /song/{id} | Actualizar canción |
| DELETE | /song/{id} | Eliminar canción |

### 🎤 Artists API
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /artist | Listar artistas |
| POST | /artist | Crear artista |
| GET | /artist/{id} | Obtener artista |
| PATCH | /artist/{id} | Actualizar artista |
| DELETE | /artist/{id} | Eliminar artista |

### 🎶 Playlists API
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /playlist | Listar playlists |
| POST | /playlist | Crear playlist |
| GET | /playlist/{id} | Obtener playlist |
| PATCH | /playlist/{id} | Actualizar playlist |
| DELETE | /playlist/{id} | Eliminar playlist |
| POST | /playlist/{playlist_id}/song/{song_id} | Agregar canción |
| DELETE | /playlist/{playlist_id}/song/{song_id} | Quitar canción |
| GET | /playlist/{id}/songs | Ver canciones de playlist |

### 🖥️ Frontend
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | / | Inicio con estadísticas |
| GET | /songs | Lista canciones + buscador |
| GET | /songs/create | Formulario crear canción |
| POST | /songs/create | Procesar y validar formulario |
| GET | /songs/{id} | Detalle canción |
| GET | /artists | Lista artistas + buscador |
| GET | /artists/create | Formulario crear artista |
| POST | /artists/create | Procesar y validar formulario |
| GET | /artists/{id} | Detalle artista |
| GET | /playlists | Lista playlists + buscador |
| GET | /playlists/create | Formulario crear playlist |
| POST | /playlists/create | Procesar y validar formulario |
| GET | /playlists/{id} | Detalle playlist + canciones |
| POST | /playlists/{id}/add | Agregar canción a playlist |
| POST | /playlists/{id}/remove/{song_id} | Quitar canción de playlist |

---

## 🚀 Despliegue

### Stack
- **Backend:** FastAPI + SQLModel + Uvicorn
- **Base de datos:** PostgreSQL en Neon
- **Almacenamiento imágenes:** Supabase Storage
- **Hosting:** Render

### Diagrama de despliegue