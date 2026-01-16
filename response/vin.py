from typing import Optional, Any
from pydantic import BaseModel


class CatalogUserSetting(BaseModel):
    catalogModelID: int
    catalogModelName: Optional[str]
    generation: Optional[str]
    countryCode: Optional[str]
    userType: Optional[str]
    canView: bool
    canBuy: bool
    showPrice: bool
    showPartImage: bool
    showRepairProcedure: bool


class VinResponse(BaseModel):
    id: int
    name: str
    catalogModelId: int
    catalogModelName: str
    catalogModelTitle: str
    countryCode: str
    catalogModelTypeId: int
    catalogModelTypeDescription: str
    localizedCatalogModelTypeDescription: str
    generation: str
    startDate: str
    endDate: Optional[str]
    isExternal: bool
    displayType: Optional[str]
    pageFlow: Optional[str]
    restrictedPermissionID: Optional[int]
    externalReference: str
    catalogUserSetting: CatalogUserSetting
    catalogUserSettings: Any
