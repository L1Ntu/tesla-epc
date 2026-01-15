from typing import Optional, List
from pydantic import BaseModel


class CatalogUserSetting(BaseModel):
    catalogModelID: int
    catalogModelName: Optional[str]
    generation: Optional[str]
    countryCode: Optional[str]
    userType: str
    canView: bool
    canBuy: bool
    showPrice: bool
    showPartImage: bool
    showRepairProcedure: bool


class CatalogResponse(BaseModel):
    id: int
    name: str
    catalogModelId: int
    catalogModelName: str
    catalogModelTitle: str
    countryCode: str
    catalogModelTypeId: int
    catalogModelTypeDescription: str
    localizedCatalogModelTypeDescription: str
    generation: Optional[str]
    startDate: str
    endDate: Optional[str]
    isExternal: bool
    displayType: Optional[int]
    pageFlow: Optional[int]
    restrictedPermissionID: Optional[str]
    externalReference: str

    catalogUserSetting: CatalogUserSetting
    catalogUserSettings: List[CatalogUserSetting]