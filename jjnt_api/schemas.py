from pydantic import BaseModel as BaseSchema


class Indicator(BaseSchema):
    id: str
    abbreviation: str
    name: str
    default_source_id: str

    class Config:
        orm_mode = True


class Category(BaseSchema):
    id: str
    name: str
    icon: str
    indicators: list[Indicator]

    class Config:
        orm_mode = True


class IndicatorDetail(BaseSchema):
    id: str
    abbreviation: str
    name: str
    description: str
    unit: str
    ascOrdering: bool
    defaultSourceId: str


class SourceDetail(BaseSchema):
    id: str
    name: str
    description: str
    url: str
    indicatorUrl: str


class DataTable(BaseSchema):
    id: str
    country: dict[str, str]
    year: int
    value: float


class Option(BaseSchema):
    id: str
    label: str
