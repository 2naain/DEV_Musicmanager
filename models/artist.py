from sqlmodel import SQLModel, Field


class ArtistBase(SQLModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    image_url: str | None = Field(default=None, max_length=500)
    is_active: bool = Field(default=True)


class ArtistID(ArtistBase, table=True):
    id: int | None = Field(default=None, primary_key=True, gt=0)

class ArtistUpdate(ArtistBase):
    name: str | None = Field(default=None)
    image_url: str | None = Field(default=None)
    is_active: bool | None = Field(default=None)