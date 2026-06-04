from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from models.song import SongBase, SongID, SongUpdate


async def createSong_db(song: SongBase, session: Session):
    new_song = SongID.model_validate(song)
    session.add(new_song)
    session.commit()
    session.refresh(new_song)
    return new_song


async def show_all_songs_db(session: Session):
    return session.exec(select(SongID).where(SongID.is_active == True)).all()


async def find_one_song_db(id: int, session: Session):
    try:
        return session.get_one(SongID, id)
    except NoResultFound:
        return None


async def update_one_song_db(id: int, new_song: SongUpdate, session: Session):
    song = await find_one_song_db(id, session)
    if song is None:
        return None
    song_update = new_song.model_dump(exclude_unset=True)
    song.sqlmodel_update(song_update)
    session.add(song)
    session.commit()
    session.refresh(song)
    return song


def kill_one_song_db(id: int, session: Session):
    try:
        song = session.get_one(SongID, id)
        song.is_active = False
        session.add(song)
        session.commit()
        session.refresh(song)
        return song
    except NoResultFound:
        return None