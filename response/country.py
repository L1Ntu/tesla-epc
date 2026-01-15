from typing import List, Any
from pydantic import BaseModel


class Locale(BaseModel):
    localeCode: str
    countryDisplayName: str
    languageCode: str
    languageName: str
    languageDisplayName: str


class TimeZone(BaseModel):
    id: int
    dotNetName: str
    linuxName: str
    displayName: str
    utcOffSetMinutes: int


class CountryResponse(BaseModel):
    name: str
    localizedName: str
    code: str
    currencyCode: str
    currencyDecimals: int
    region: str
    isCountryOnboarded: bool
    defaultEntityCode: str|Any
    states: List[dict]
    locales: List[Locale]
    timeZones: List[TimeZone]
