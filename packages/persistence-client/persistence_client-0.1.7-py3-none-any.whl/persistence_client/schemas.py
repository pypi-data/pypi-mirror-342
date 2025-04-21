from pydantic import BaseModel


class I18n(BaseModel):
    kz: str
    ru: str
    en: str

class DataColumn(BaseModel):
    title: I18n

class DataSchema(BaseModel):
    id: str
    title: I18n
    columns: list[DataColumn]

class DataRow(BaseModel):
    hash: str
    bin_iin: str | None = None
    fio: str | None = None
    title: str | None = None
    data: list[str | int | float]
    data_schema: DataSchema
