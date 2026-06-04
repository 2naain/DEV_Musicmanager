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
from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Form, Depends
from typing import Optional
from sqlmodel import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.playlist import PlaylistBase, PlaylistID
from models.song import SongBase, SongID, SongUpdate
from models.artist import ArtistBase, ArtistID
from db import SessionDep, create_all_tables, get_session
from operations.operations_song_db import (createSong_db,
                                           show_all_songs_db,
                                           find_one_song_db,
                                           update_one_song_db,
                                           kill_one_song_db)
from operations.operations_artist_db import createArtist, findArtist, findAllArtists, updateArtist, deleteArtist
from utils import save_img_local, save_img_remote


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
    return {"path for your image": path}


@app.post("/image/remote", tags=["Images"])
async def image_save_remote(file: UploadFile = File(...)):
    url_img = save_img_remote(file)
    return {"url for your image": url_img}


# ==========================
# SONGS
# ==========================

@app.post("/song", response_model=SongID, tags=["Songs"])
async def create_song(
        title: str = Form(),
        genre: Optional[str] = Form(None),
        duration: Optional[int] = Form(None),
        artist_id: int = Form(...),
        image: UploadFile = File(...),
        session: Session = Depends(get_session)):

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


@app.get("/song", response_model=list[SongID], tags=["Songs"])
async def show_songs(session: SessionDep):
    return await show_all_songs_db(session)


@app.get("/song/{id}", response_model=SongID, tags=["Songs"])
async def show_one_song(id: int, session: SessionDep):
    song = await find_one_song_db(id, session)
    if not song:
        raise HTTPException(status_code=404, detail=f"{id} Song not found")
    return song


@app.patch(
    "/song/{id}",
    response_model=SongID,
    response_model_exclude={"title", "genre"},
    tags=["Songs"]
)
async def update_song(id: int, song: SongUpdate, session: SessionDep):
    update = await update_one_song_db(id, song, session)
    if not update:
        raise HTTPException(status_code=404, detail=f"{id} Song not found")
    return update


@app.delete("/song/{id}", response_model=SongBase, tags=["Songs"])
async def delete_one_song(id: int, session: SessionDep):
    deleted = kill_one_song_db(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"{id} Song not found")
    return deleted


# ==========================
# ARTISTS
# ==========================

@app.post("/artist", response_model=ArtistID, tags=["Artists"])
def create_artist(artist: ArtistBase, session: SessionDep):
    return createArtist(artist, session)


@app.get("/artist", response_model=list[ArtistID], tags=["Artists"])
def get_all_artists(session: SessionDep):
    return findAllArtists(session)


@app.get("/artist/{id}", response_model=ArtistID, tags=["Artists"])
def get_one_artist(id: int, session: SessionDep):
    artist = findArtist(id, session)
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    return artist


@app.patch("/artist/{id}", response_model=ArtistID, tags=["Artists"])
def update_artist(id: int, artist: ArtistBase, session: SessionDep):
    updated = updateArtist(id, artist, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Artist not found")
    return updated


@app.delete("/artist/{id}", response_model=ArtistID, tags=["Artists"])
def delete_artist(id: int, session: SessionDep):
    deleted = deleteArtist(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Artist not found")
    return deleted


# ==========================
# FRONTEND
# ==========================

@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def home(request: Request):
    return templates.TemplateResponse(
        {"request": request},
        "base.html"
    )


@app.get("/songs", response_class=HTMLResponse, tags=["Frontend"])
async def show_all_songs_html(
    request: Request,
    session: Session = Depends(get_session)
):
    songs = await show_all_songs_db(session)
    return templates.TemplateResponse(
        request,
        "all_songs.html",
        {"song_list": songs}
    )


@app.get("/songs/{id}", response_class=HTMLResponse, tags=["Frontend"])
async def show_one_song_html(
    request: Request,
    id: int,
    session: SessionDep
):
    one_song = await find_one_song_db(id, session)
    return templates.TemplateResponse(
        request,
        "one_song.html",
        {"song": one_song}
    )


@app.get("/songs/create/", response_class=HTMLResponse, tags=["Frontend"])
async def add_song_html(request: Request):
    return templates.TemplateResponse(
        request,
        "add_song.html"
    )


@app.post("/songs/create/", response_class=HTMLResponse, tags=["Frontend"])
async def song_added(
    title: str = Form(),
    genre: Optional[str] = Form(None),
    duration: Optional[int] = Form(None),
    artist_id: Optional[int] = Form(None),
    session: Session = Depends(get_session)
):
    new_song = SongBase(
        title=title,
        genre=genre,
        duration=duration,
        artist_id=artist_id
    )
    await createSong_db(new_song, session)
    return RedirectResponse("/songs", status_code=302)


# ==========================
# PLAYLIST
# ==========================

@app.post("/playlist", response_model=PlaylistID, tags=["Playlists"])
def create_playlist_endpoint(playlist: PlaylistBase, session: SessionDep):
    return create_playlist_db(playlist, session)


@app.get("/playlist", response_model=list[PlaylistID], tags=["Playlists"])
def get_playlists(session: SessionDep):
    return get_all_playlists(session)


@app.get("/playlist/{id}", response_model=PlaylistID, tags=["Playlists"])
def get_playlist(id: int, session: SessionDep):
    playlist = get_one_playlist(id, session)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist


@app.patch("/playlist/{id}", response_model=PlaylistID, tags=["Playlists"])
def update_playlist_endpoint(id: int, playlist: PlaylistBase, session: SessionDep):
    updated = update_playlist_db(id, playlist, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return updated


@app.delete("/playlist/{id}", response_model=PlaylistID, tags=["Playlists"])
def delete_playlist_endpoint(id: int, session: SessionDep):
    deleted = delete_playlist_db(id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return deleted


@app.post("/playlist/{playlist_id}/song/{song_id}", tags=["Playlists"])
def add_song(playlist_id: int, song_id: int, session: SessionDep):
    result, error = add_song_to_playlist(playlist_id, song_id, session)
    if error == "playlist":
        raise HTTPException(status_code=404, detail="Playlist not found")
    if error == "song":
        raise HTTPException(status_code=404, detail="Song not found")
    if error == "duplicate":
        raise HTTPException(status_code=400, detail="Song already in playlist")
    return {"message": "Song added to playlist"}


@app.delete("/playlist/{playlist_id}/song/{song_id}", tags=["Playlists"])
def remove_song(playlist_id: int, song_id: int, session: SessionDep):
    result = remove_song_from_playlist(playlist_id, song_id, session)
    if not result:
        raise HTTPException(status_code=404, detail="Song not in playlist")
    return {"message": "Song removed from playlist"}


@app.get("/playlist/{id}/songs", response_model=list[SongID], tags=["Playlists"])
def get_playlist_songs(id: int, session: SessionDep):
    playlist = get_one_playlist(id, session)
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return get_songs_of_playlist(id, session)