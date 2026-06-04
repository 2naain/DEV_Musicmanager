from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from typing import Optional

from db import SessionDep, create_all_tables, get_session
from models.song import SongBase, SongID, SongUpdate
from models.artist import ArtistBase, ArtistID
from models.playlist import PlaylistBase, PlaylistID
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
def update_artist_api(id: int, artist: ArtistBase, session: SessionDep):
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
def update_playlist_api(id: int, playlist: PlaylistBase, session: SessionDep):
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
async def home(request: Request):
    return templates.TemplateResponse(request, "base.html", {})


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
    return templates.TemplateResponse(request, "all_songs.html", {
        "song_list": songs,
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
    title: str = Form(...),
    genre: Optional[str] = Form(None),
    duration: Optional[int] = Form(None),
    artist_id: int = Form(...),
    image: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    image_url = None
    if image and image.filename:
        image_url = save_img_remote(image)
    new_song = SongBase(
        title=title,
        genre=genre,
        duration=duration,
        artist_id=artist_id,
        image_url=image_url
    )
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
    name: str = Form(...),
    image: UploadFile = File(None),
    session: Session = Depends(get_session)
):
    image_url = None
    if image and image.filename:
        image_url = save_img_remote(image)
    new_artist = ArtistBase(name=name, image_url=image_url)
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
def playlist_created(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    new_playlist = PlaylistBase(name=name, description=description)
    create_playlist_db(new_playlist, session)
    return RedirectResponse("/playlists", status_code=302)


@app.get("/playlists/{id}", response_class=HTMLResponse, tags=["Frontend"])
def show_one_playlist_html(request: Request, id: int, session: SessionDep):
    playlist = get_one_playlist(id, session)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    songs = get_songs_of_playlist(id, session)
    return templates.TemplateResponse(request, "one_playlist.html", {
        "playlist": playlist,
        "songs": songs
    })