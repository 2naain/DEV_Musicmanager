from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from typing import Optional

from db import SessionDep, create_all_tables, get_session
from models.song import SongBase, SongID, SongUpdate
from models.artist import ArtistBase, ArtistID, ArtistUpdate
from models.playlist import PlaylistBase, PlaylistID, PlaylistUpdate
from utils import save_img_remote, save_img_local

from operations.operations_song_db import (
    createSong_db,
    show_all_songs_db,
    find_one_song_db,
    update_one_song_db,
    kill_one_song_db
)
from operations.operations_artist_db import (
    createArtist,
    findArtist,
    findAllArtists,
    updateArtist,
    deleteArtist
)
from operations.operations_playlist_db import (
    create_playlist as create_playlist_db,
    get_all_playlists,
    get_one_playlist,
    update_playlist as update_playlist_db,
    delete_playlist as delete_playlist_db,
    add_song_to_playlist,
    remove_song_from_playlist,
    get_songs_of_playlist
)

app = FastAPI(lifespan=create_all_tables)
templates = Jinja2Templates(directory="templates")


def format_duration(seconds):
    if not seconds:
        return "0:00"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"


templates.env.filters["duration"] = format_duration


# ==========================
# IMAGES
# ==========================

@app.post("/image/local", tags=["Images"])
async def image_save_local(img: UploadFile = File(...)):
    path = save_img_local(img)
    return {"path": path}


@app.post("/image/remote", tags=["Images"])
async def image_save_remote(file: UploadFile = File(...)):
    url = save_img_remote(file)
    return {"url": url}


# ==========================
# API - SONGS
# ==========================

@app.post("/song", response_model=SongID, tags=["Songs API"])
async def create_song_api(
    title: str = Form(),
    genre: Optional[str] = Form(None),
    duration: Optional[int] = Form(None),
    artist_id: int = Form(...),
    image: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    artist = findArtist(artist_id, session)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    image_url = save_img_remote(image)
    new_song = SongBase(
        title=title,
        genre=genre,
        duration=duration,
        artist_id=artist_id,
        image_url=image_url
    )
    return await createSong_db(new_song, session)


@app.get("/song", response_model=list[SongID], tags=["Songs API"])
async def show_songs_api(session: SessionDep):
    return await show_all_songs_db(session)


@app.get("/song/{id}", response_model=SongID, tags=["Songs API"])
async def show_one_song_api(id: int, session: SessionDep):
    song = await find_one_song_db(id, session)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@app.patch("/song/{id}", response_model=SongID, tags=["Songs API"])
async def update_song_api(id: int, song: SongUpdate, session: SessionDep):
    updated = await update_one_song_db(id, song, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Song not found")
    return updated


@app.delete("/song/{id}", response_model=SongBase, tags=["Songs API"])
async def delete_song_api(id: int, session: SessionDep):
    deleted = kill_one_song_db(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Song not found")
    return deleted


# ==========================
# API - ARTISTS
# ==========================

@app.post("/artist", response_model=ArtistID, tags=["Artists API"])
def create_artist_api(artist: ArtistBase, session: SessionDep):
    return createArtist(artist, session)


@app.get("/artist", response_model=list[ArtistID], tags=["Artists API"])
def get_all_artists_api(session: SessionDep):
    return findAllArtists(session)


@app.get("/artist/{id}", response_model=ArtistID, tags=["Artists API"])
def get_one_artist_api(id: int, session: SessionDep):
    artist = findArtist(id, session)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@app.patch("/artist/{id}", response_model=ArtistID, tags=["Artists API"])
def update_artist_api(id: int, artist: ArtistUpdate, session: SessionDep):
    updated = updateArtist(id, artist, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Artist not found")
    return updated

@app.delete("/artist/{id}", response_model=ArtistID, tags=["Artists API"])
def delete_artist_api(id: int, session: SessionDep):
    deleted = deleteArtist(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Artist not found")
    return deleted


# ==========================
# API - PLAYLISTS
# ==========================

@app.post("/playlist", response_model=PlaylistID, tags=["Playlists API"])
def create_playlist_api(playlist: PlaylistBase, session: SessionDep):
    return create_playlist_db(playlist, session)


@app.get("/playlist", response_model=list[PlaylistID], tags=["Playlists API"])
def get_playlists_api(session: SessionDep):
    return get_all_playlists(session)


@app.get("/playlist/{id}", response_model=PlaylistID, tags=["Playlists API"])
def get_one_playlist_api(id: int, session: SessionDep):
    playlist = get_one_playlist(id, session)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@app.patch("/playlist/{id}", response_model=PlaylistID, tags=["Playlists API"])
def update_playlist_api(id: int, playlist: PlaylistUpdate, session: SessionDep):
    updated = update_playlist_db(id, playlist, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return updated

@app.delete("/playlist/{id}", response_model=PlaylistID, tags=["Playlists API"])
def delete_playlist_api(id: int, session: SessionDep):
    deleted = delete_playlist_db(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return deleted


@app.post("/playlist/{playlist_id}/song/{song_id}", tags=["Playlists API"])
def add_song_to_playlist_api(playlist_id: int, song_id: int, session: SessionDep):
    result, error = add_song_to_playlist(playlist_id, song_id, session)
    if error == "playlist":
        raise HTTPException(status_code=404, detail="Playlist not found")
    if error == "song":
        raise HTTPException(status_code=404, detail="Song not found")
    if error == "duplicate":
        raise HTTPException(status_code=400, detail="Song already in playlist")
    return {"message": "Song added to playlist"}


@app.delete("/playlist/{playlist_id}/song/{song_id}", tags=["Playlists API"])
def remove_song_from_playlist_api(playlist_id: int, song_id: int, session: SessionDep):
    result = remove_song_from_playlist(playlist_id, song_id, session)
    if not result:
        raise HTTPException(status_code=404, detail="Song not in playlist")
    return {"message": "Song removed from playlist"}


@app.get("/playlist/{id}/songs", response_model=list[SongID], tags=["Playlists API"])
def get_playlist_songs_api(id: int, session: SessionDep):
    playlist = get_one_playlist(id, session)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return get_songs_of_playlist(id, session)


# ==========================
# FRONTEND - HOME
# ==========================

@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def home(request: Request, q: Optional[str] = None, session: Session = Depends(get_session)):
    songs = await show_all_songs_db(session)
    artists = findAllArtists(session)
    playlists = get_all_playlists(session)

    artist_map = {a.id: a.name for a in artists}
    search_results = None
    if q:
        q_clean = q.strip().lower()
        search_results = {
            "canciones": [s for s in songs if q_clean in (s.title or "").lower()
                          or q_clean in artist_map.get(s.artist_id, "").lower()],
            "artistas": [a for a in artists if q_clean in (a.name or "").lower()],
            "playlists": [p for p in playlists if q_clean in (p.name or "").lower()],
        }

    return templates.TemplateResponse(request, "home.html", {
        "search_action": "/",
        "search_placeholder": "Buscar...",
        "songs": songs,
        "artists": artists,
        "playlists": playlists,
        "artist_map": artist_map,
        "q": q,
        "search_results": search_results,
    })


# ==========================
# FRONTEND - STATS
# ==========================

@app.get("/stats", response_class=HTMLResponse, tags=["Frontend"])
async def stats_html(request: Request, session: Session = Depends(get_session)):
    songs = await show_all_songs_db(session)
    artists = findAllArtists(session)
    playlists = get_all_playlists(session)

    # Songs per genre
    genre_counts = {}
    for s in songs:
        g = s.genre.value if s.genre else "Sin género"
        genre_counts[g] = genre_counts.get(g, 0) + 1

    # Songs per artist (top 8)
    artist_map = {a.id: a.name for a in artists}
    artist_counts = {}
    for s in songs:
        name = artist_map.get(s.artist_id, "Desconocido")
        artist_counts[name] = artist_counts.get(name, 0) + 1
    top_artists = sorted(artist_counts.items(), key=lambda x: -x[1])[:8]

    return templates.TemplateResponse(request, "stats.html", {
        "total_songs": len(songs),
        "total_artists": len(artists),
        "total_playlists": len(playlists),
        "genre_counts": genre_counts,
        "top_artists": top_artists,
    })


# ==========================
# FRONTEND - SONGS
# ==========================

@app.get("/songs", response_class=HTMLResponse, tags=["Frontend"])
async def show_all_songs_html(
    request: Request,
    q: Optional[str] = None,
    session: Session = Depends(get_session)
):
    q = q.strip() if q else None
    songs = await show_all_songs_db(session, q=q)
    artists = findAllArtists(session)
    artist_map = {a.id: a.name for a in artists}
    return templates.TemplateResponse(request, "all_songs.html", {
        "song_list": songs,
        "artist_map": artist_map,
        "q": q,
        "search_action": "/songs",
        "search_placeholder": "Buscar canción...",
        "create_url": "/songs/create"
    })


@app.get("/songs/create", response_class=HTMLResponse, tags=["Frontend"])
async def create_song_html(
    request: Request,
    session: Session = Depends(get_session)
):
    artists = findAllArtists(session)
    return templates.TemplateResponse(request, "create_song.html", {
        "artists": artists,
        "create_url": "/songs/create"
    })


@app.post("/songs/create", response_class=HTMLResponse, tags=["Frontend"])
async def song_created(
    request: Request,
    title: str = Form(...),
    genre: Optional[str] = Form(None),
    duration: Optional[int] = Form(None),
    artist_id: int = Form(...),
    image: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    artists = findAllArtists(session)
    if len(title.strip()) < 2:
        return templates.TemplateResponse(request, "create_song.html", {
            "error": "El título debe tener al menos 2 caracteres",
            "artists": artists,
            "create_url": "/songs/create"
        })
    if duration and duration <= 0:
        return templates.TemplateResponse(request, "create_song.html", {
            "error": "La duración debe ser mayor a 0",
            "artists": artists,
            "create_url": "/songs/create"
        })
    image_url = None
    if image and image.filename:
        image_url = save_img_remote(image)
    new_song = SongBase(title=title.strip(), genre=genre, duration=duration, artist_id=artist_id, image_url=image_url)
    await createSong_db(new_song, session)
    return RedirectResponse("/songs", status_code=302)


@app.get("/songs/{id}", response_class=HTMLResponse, tags=["Frontend"])
async def show_one_song_html(request: Request, id: int, session: SessionDep):
    song = await find_one_song_db(id, session)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return templates.TemplateResponse(request, "one_song.html", {"song": song})


# ==========================
# FRONTEND - ARTISTS
# ==========================

@app.get("/artists", response_class=HTMLResponse, tags=["Frontend"])
def show_all_artists_html(
    request: Request,
    q: Optional[str] = None,
    session: Session = Depends(get_session)
):
    q = q.strip() if q else None
    artists = findAllArtists(session, q=q)
    return templates.TemplateResponse(request, "all_artists.html", {
        "artist_list": artists,
        "q": q,
        "search_action": "/artists",
        "search_placeholder": "Buscar artista...",
        "create_url": "/artists/create"
    })


@app.get("/artists/create", response_class=HTMLResponse, tags=["Frontend"])
def create_artist_html(request: Request):
    return templates.TemplateResponse(request, "create_artist.html", {
        "create_url": "/artists/create"
    })


@app.post("/artists/create", response_class=HTMLResponse, tags=["Frontend"])
async def artist_created(
    request: Request,
    name: str = Form(...),
    descripcion: Optional[str] = Form(None),
    image: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    if len(name.strip()) < 2:
        return templates.TemplateResponse(request, "create_artist.html", {
            "error": "El nombre debe tener al menos 2 caracteres",
            "create_url": "/artists/create"
        })
    image_url = None
    if image and image.filename:
        image_url = save_img_remote(image)
    new_artist = ArtistBase(name=name.strip(), image_url=image_url, descripcion=descripcion)
    createArtist(new_artist, session)
    return RedirectResponse("/artists", status_code=302)


@app.get("/artists/{id}", response_class=HTMLResponse, tags=["Frontend"])
def show_one_artist_html(request: Request, id: int, session: SessionDep):
    artist = findArtist(id, session)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return templates.TemplateResponse(request, "one_artist.html", {"artist": artist})


# ==========================
# FRONTEND - PLAYLISTS
# ==========================

@app.get("/playlists", response_class=HTMLResponse, tags=["Frontend"])
def show_all_playlists_html(
    request: Request,
    q: Optional[str] = None,
    session: Session = Depends(get_session)
):
    q = q.strip() if q else None
    playlists = get_all_playlists(session, q=q)
    return templates.TemplateResponse(request, "all_playlists.html", {
        "playlist_list": playlists,
        "q": q,
        "search_action": "/playlists",
        "search_placeholder": "Buscar playlist...",
        "create_url": "/playlists/create"
    })


@app.get("/playlists/create", response_class=HTMLResponse, tags=["Frontend"])
def create_playlist_html(request: Request):
    return templates.TemplateResponse(request, "create_playlist.html", {
        "create_url": "/playlists/create"
    })


@app.post("/playlists/create", response_class=HTMLResponse, tags=["Frontend"])
async def playlist_created(
    request: Request,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    image: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    if len(name.strip()) < 2:
        return templates.TemplateResponse(request, "create_playlist.html", {
            "error": "El nombre debe tener al menos 2 caracteres",
            "create_url": "/playlists/create"
        })
    image_url = None
    if image and image.filename:
        image_url = save_img_remote(image)
    new_playlist = PlaylistBase(name=name.strip(), description=description, image_url=image_url)
    create_playlist_db(new_playlist, session)
    return RedirectResponse("/playlists", status_code=302)


@app.get("/playlists/{id}", response_class=HTMLResponse, tags=["Frontend"])
def show_one_playlist_html(request: Request, id: int, session: SessionDep):
    playlist = get_one_playlist(id, session)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    songs = get_songs_of_playlist(id, session)
    all_songs = session.exec(select(SongID).where(SongID.is_active == True)).all()
    return templates.TemplateResponse(request, "one_playlist.html", {
        "playlist": playlist,
        "songs": songs,
        "all_songs": all_songs
    })


@app.post("/playlists/{id}/add", tags=["Frontend"])
def add_song_html(id: int, song_id: int = Form(...), session: Session = Depends(get_session)):
    add_song_to_playlist(id, song_id, session)
    return RedirectResponse(f"/playlists/{id}", status_code=302)


@app.post("/playlists/{id}/remove/{song_id}", tags=["Frontend"])
def remove_song_html(id: int, song_id: int, session: SessionDep):
    remove_song_from_playlist(id, song_id, session)
    return RedirectResponse(f"/playlists/{id}", status_code=302)
