from sqlalchemy.exc import NoResultFound
from sqlmodel import Session

from models.artist import ArtistBase, ArtistID


def createArtist(artist: ArtistBase, session: Session):
    new_artist = ArtistID.model_validate(artist)
    session.add(new_artist)
    session.commit()
    session.refresh(new_artist)
    return new_artist


def findArtist(id: int, session: Session):
    try:
        return session.get_one(ArtistID, id)
    except NoResultFound:
        return None


def findAllArtists(session: Session):
    from sqlmodel import select
    return session.exec(select(ArtistID)).all()


def updateArtist(id: int, new_data: ArtistBase, session: Session):
    artist = findArtist(id, session)
    if artist is None:
        return None
    update = new_data.model_dump(exclude_unset=True)
    artist.sqlmodel_update(update)
    session.add(artist)
    session.commit()
    session.refresh(artist)
    return artist


def deleteArtist(id: int, session: Session):
    artist = findArtist(id, session)
    if artist is None:
        return None
    session.delete(artist)
    session.commit()
    return artist