from __future__ import annotations

from datetime import date, datetime
from typing import Optional, List, Any

from pydantic import BaseModel, HttpUrl, field_validator


class NalogModel(BaseModel):
    ERROR: Optional[str] = None
    ERRORS: Optional[Any] = None

    @staticmethod
    def get_csv_delimiter():
        return ";"

    @staticmethod
    def ignore_fields() -> list[str]:
        return ["ERROR", "ERRORS"]

    @classmethod
    def get_headers(cls) -> str:
        headers = []
        for column in cls.model_fields.keys():
            if column in Organization.ignore_fields():
                continue

            headers.append(column)

        return cls.get_csv_delimiter().join(headers)

    def get_csv(self) -> str:
        values = []
        for column in self.model_fields.keys():
            if column in Organization.ignore_fields():
                continue

            value = getattr(self, column)
            values.append(value if value is not None else "")
        return self.get_csv_delimiter().join(map(str, values))


class SearchRequest(NalogModel):
    id: Optional[str] = None
    captchaRequired: Optional[bool] = None


# 🔹 Организации (UL)
class Organization(NalogModel):
    inn: str
    predo: Optional[str] = None
    pr_liq: Optional[str] = None
    dtreg: Optional[date] = None
    dtogrn: Optional[date] = None
    okved2: Optional[str] = None
    ogrn: str
    yearcode: Optional[str] = None
    sulst_name_ex: Optional[str] = None
    okved2name: Optional[str] = None
    regionname: Optional[str] = None
    invalid: Optional[str] = None
    sulst_ex: Optional[str] = None
    periodcode: Optional[str] = None
    namep: str
    okopf12: Optional[str] = None
    puchdocurl: Optional[HttpUrl] = None
    rsmppdf: Optional[HttpUrl] = None
    token: str
    egrulurl: Optional[str] = None
    bourl: Optional[HttpUrl] = None

    @field_validator("dtreg", "dtogrn", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%d.%m.%Y").date()
            except ValueError:
                raise ValueError(f"Invalid date format: {value}")
        return value


class ULResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[Organization]
    rowCount: Optional[int] = None


# 🔹 Индивидуальные предприниматели (IP)
class IndividualEntrepreneur(NalogModel):
    inn: str
    ogrnip: str
    name: str
    dtreg: Optional[date]
    okved: Optional[str]
    regionname: Optional[str]
    token: str


class IPResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[IndividualEntrepreneur]


# 🔹 Участники ЮЛ (Uchr)
class Participant(NalogModel):
    inn: Optional[str]
    ul_cnt: Optional[int]  # Количество участий в ЮЛ
    name: str
    type: Optional[str]
    kind: Optional[str]
    token: str


class UchrResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[Participant]
    rowCount: Optional[int]


# 🔹 Управляющие (Upr)
class UpravlenecResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[Participant]
    rowCount: Optional[int]


# 🔹 Дисквалифицированные лица (RDL)
class DisqualifiedPerson(NalogModel):
    name: str
    inn: Optional[str]
    date: Optional[date]
    reason: Optional[str]
    token: str


class RDLResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[DisqualifiedPerson]


# 🔹 Ограничения участия в ЮЛ (OGRFL)
class Restriction(NalogModel):
    name: str
    inn: Optional[str]
    ogrn: str
    reason: Optional[str]
    token: str


class OGRFLResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[Restriction]


# 🔹 Поиск по адресам (ADDR)
class AddressData(NalogModel):
    address: str
    region: Optional[str]


class AddressSearchResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[AddressData]  # Теперь объект, а не строка


# 🔹 Документы ЮЛ (DOCUL)
class DocumentUL(NalogModel):
    ogrn: str
    name: str
    form: Optional[str]
    date: Optional[date]
    token: str


class DOCULResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[DocumentUL]


# 🔹 Документы ИП (DOCIP)
class DocumentIP(NalogModel):
    ogrnip: str
    name: str
    form: Optional[str]
    date: Optional[date]
    token: str


class DOCIPResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[DocumentIP]


# 🔹 Ограничения участия ЮЛ (OGRUL)
class OGRULResult(NalogModel):
    hasMore: bool
    page: int
    pageSize: int
    data: List[Restriction]


# 🔹 Итоговая модель, объединяющая все разделы
class SearchResult(NalogModel):
    ul: Optional[ULResult] = None
    ip: Optional[IPResult] = None
    uchr: Optional[UchrResult] = None
    upr: Optional[UpravlenecResult] = None
    rdl: Optional[RDLResult] = None
    ogrfl: Optional[OGRFLResult] = None
    addr: Optional[AddressSearchResult] = None
    docul: Optional[DOCULResult] = None
    docip: Optional[DOCIPResult] = None
    ogrul: Optional[OGRULResult] = None
