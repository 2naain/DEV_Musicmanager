from models.song_genres import SongGenre
from sqlmodel import SQLModel, Field


class SongBase(SQLModel):
    title: str | None = Field(default=None, min_length=2, max_length=100)
    genre: SongGenre | None = Field(default=None)
    duration: int | None = Field(default=None, gt=0, le=10000)
    artist_id: int | None = Field(default=None, gt=0)
    in_playlist: bool = Field(default=False)
    is_active: bool = Field(default=True)
    image_url: str | None = Field(default=None, max_length=500)


class SongID(SongBase, table=True):
    id: int | None = Field(default=None, primary_key=True, gt=0)


class SongUpdate(SongBase):
    title: str | None = Field(None, exclude=True)
    genre: SongGenre = Field(None, exclude=True)
    artist_id: int | None = Field(None, exclude=True)
    in_playlist: bool = Field(None, exclude=True)
    duration: int | None = Field(default=None, gt=0, le=600)