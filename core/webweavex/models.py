from pydantic import BaseModel, Field


class Link(BaseModel):
  url: str
  text: str | None = None


class Metadata(BaseModel):
  title: str | None = None
  meta: dict[str, str] = Field(default_factory=dict)


class PageResult(BaseModel):
  url: str
  status: int | None = None
  html: str | None = None
  links: list[Link] = Field(default_factory=list)
  metadata: Metadata = Field(default_factory=Metadata)
