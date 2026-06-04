from sqlmodel import SQLModel, Field


class ArtistBase(SQLModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    is_active: bool = Field(default=True)
    image_url: str | None = Field(default=None, max_length=500)


class ArtistID(ArtistBase, table=True):
    id: int | None = Field(default=None, primary_key=True, gt=0)