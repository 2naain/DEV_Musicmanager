from sqlmodel import SQLModel, Field


class PlaylistSong(SQLModel, table=True):
    playlist_id: int | None = Field(default=None, foreign_key="playlistid.id", primary_key=True)
    song_id: int | None = Field(default=None, foreign_key="songid.id", primary_key=True)