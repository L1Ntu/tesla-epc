from typing import List, Optional, Any
from pydantic import BaseModel


class SystemGroupImage(BaseModel):
    mimetype: str
    imageURL: str
    fileName: str
    uuid: str
    attributes: Optional[str] = None
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


class SubcategoryResponse(BaseModel):
    id: int
    title: str
    titleOriginal: str
    categoryId: int
    additionalAttribute: int
    displayOrder: Optional[int]
    externalReference: str
    partSource: int
    category: Optional[Any]

    systemGroups: List[SystemGroup]
