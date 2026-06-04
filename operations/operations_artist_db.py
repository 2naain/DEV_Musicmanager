from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from models.artist import ArtistBase, ArtistID, ArtistUpdate


def createArtist(artist: ArtistBase, session: Session):
    new_artist = ArtistID.model_validate(artist)
    session.add(new_artist)
    session.commit()
    session.refresh(new_artist)
    return new_artist


def findArtist(id: int, session: Session):
    try:
        artist = session.get_one(ArtistID, id)
        if not artist.is_active:
            return None
        return artist
    except NoResultFound:
        return None


def findAllArtists(session: Session, q: str = None):
    query = select(ArtistID).where(ArtistID.is_active == True)
    if q:
        query = query.where(ArtistID.name.ilike(f"%{q}%"))
    return session.exec(query).all()


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
    artist.is_active = False
    session.add(artist)
    session.commit()
    session.refresh(artist)
    return artist