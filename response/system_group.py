from typing import List, Optional, Any
from pydantic import BaseModel


class SystemGroupImage(BaseModel):
    mimetype: Optional[str]
    imageURL: Optional[str]
    fileName: Optional[str]
    uuid: Optional[str] = ""
    attributes: Optional[str]
    extendedAttributes: List[Any]


class SystemGroupResponse(BaseModel):
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

    images: Optional[str] = ""

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
