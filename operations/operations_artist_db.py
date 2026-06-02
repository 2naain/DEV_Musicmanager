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