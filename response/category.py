from typing import List, Optional, Any
from pydantic import BaseModel, Field


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


class Catalog(BaseModel):
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
    displayType: Optional[Any]
    pageFlow: Optional[Any]
    restrictedPermissionID: Optional[Any]
    externalReference: str
    catalogUserSetting: CatalogUserSetting
    catalogUserSettings: List[Any]


class SystemGroupImage(BaseModel):
    mimetype: str
    imageURL: str
    fileName: str
    uuid: Optional[str] = None
    attributes: Optional[str]
    extendedAttributes: List[Any]


class SystemGroup(BaseModel):
    vin: Optional[str]
    catalogId: int
    catalogExternalReference: Optional[str]
    catalogName: Optional[str]
    catalogModelId: int
    catalogModelTypeID: int
    catalogModelName: Optional[str]
    catalogModelTitle: Optional[str]
    countryCode: Optional[str]
    currency: Optional[str]
    id: int
    titleOriginal: str
    title: str
    subcategoryId: int
    subcategoryExternalReference: str
    subcategoryTitleOriginal: str
    subcategoryTitle: str
    categoryId: int
    categoryExternalReference: Optional[str]
    categoryTitleOriginal: Optional[str]
    categoryTitle: Optional[str]
    images: Optional[str]
    parts: List[Any]
    showPrice: bool
    partSource: int
    pointOfImpacts: List[Any]
    systemGroupImages: List[SystemGroupImage]
    externalReference: str
    canBuy: bool
    generation: Optional[str]
    showPartImage: bool
    extendedAttributes: Optional[Any]


class SubCategory(BaseModel):
    id: int
    title: str
    titleOriginal: str
    categoryId: int
    additionalAttribute: int
    displayOrder: Optional[Any]
    externalReference: str
    partSource: int
    category: Optional[Any]
    systemGroups: List[SystemGroup]


class CategoryResponse(BaseModel):
    id: int
    title: str
    titleOriginal: str
    displayOrder: Optional[Any]
    catalogId: int
    catalog: Catalog
    subCategories: List[SubCategory]
    externalReference: str
    extendedAttributes: Optional[Any]
    partSource: int
    image: str
