from sqlmodel import SQLModel, Field


class PlaylistBase(SQLModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)
    image_url: str | None = Field(default=None, max_length=500)


class PlaylistID(PlaylistBase, table=True):
    id: int | None = Field(default=None, primary_key=True)