from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models.playlist import PlaylistBase, PlaylistID
from models.playlist_song import PlaylistSong
from models.song import SongID


def create_playlist(playlist: PlaylistBase, session: Session):
    new_playlist = PlaylistID.model_validate(playlist)
    session.add(new_playlist)
    session.commit()
    session.refresh(new_playlist)
    return new_playlist


def get_all_playlists(session: Session):
    return session.exec(select(PlaylistID)).all()


def get_one_playlist(id: int, session: Session):
    try:
        return session.get_one(PlaylistID, id)
    except NoResultFound:
        return None


def update_playlist(id: int, new_data: PlaylistBase, session: Session):
    playlist = get_one_playlist(id, session)
    if playlist is None:
        return None
    update = new_data.model_dump(exclude_unset=True)
    playlist.sqlmodel_update(update)
    session.add(playlist)
    session.commit()
    session.refresh(playlist)
    return playlist


def delete_playlist(id: int, session: Session):
    playlist = get_one_playlist(id, session)
    if playlist is None:
        return None
    session.delete(playlist)
    session.commit()
    return playlist


def add_song_to_playlist(playlist_id: int, song_id: int, session: Session):
    playlist = get_one_playlist(playlist_id, session)
    if playlist is None:
        return None, "playlist"
    song = session.get(SongID, song_id)
    if song is None:
        return None, "song"
    existing = session.exec(
        select(PlaylistSong).where(
            PlaylistSong.playlist_id == playlist_id,
            PlaylistSong.song_id == song_id
        )
    ).first()
    if existing:
        return None, "duplicate"
    link = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
    session.add(link)
    session.commit()
    return link, None


def remove_song_from_playlist(playlist_id: int, song_id: int, session: Session):
    link = session.exec(
        select(PlaylistSong).where(
            PlaylistSong.playlist_id == playlist_id,
            PlaylistSong.song_id == song_id
        )
    ).first()
    if link is None:
        return None
    session.delete(link)
    session.commit()
    return link


def get_songs_of_playlist(playlist_id: int, session: Session):
    links = session.exec(
        select(PlaylistSong).where(PlaylistSong.playlist_id == playlist_id)
    ).all()
    songs = []
    for link in links:
        song = session.get(SongID, link.song_id)
        if song:
            songs.append(song)
    return songs