from typing import List, Optional, Any
from pydantic import BaseModel


class SystemGroupImage(BaseModel):
    mimetype: Optional[str]
    imageURL: Optional[str]
    fileName: Optional[str]
    uuid: Optional[str] = ''
    attributes: Optional[str]
    extendedAttributes: List[Any]


class Part(BaseModel):
    partId: int
    title: str
    annotation: str
    partNumber: str
    recommendedPartNumber: Optional[str]
    catalogPartNumber: str
    quantity: int
    currencyCode: Optional[str]
    countryCode: Optional[str]
    itemQuantity: int
    catalogQuantity: int
    minimumOrderQuantity: int
    orderMultipleQuantity: int
    notes: Optional[str]
    price: float
    discountTypeID: int
    discountTypeDescription: Optional[str]
    discountPercentage: float
    recommendationType: Optional[str]
    internal: bool
    partRestriction: str
    partRestrictionID: int
    partRestrictionMessage: str
    displayOrder: float
    partSource: int
    recommendedPartSource: int
    hasSuperSession: bool
    partProcurementType: Optional[str]
    partType: str
    partTypeID: int
    validateMaxQuantity: bool
    notAllowedInStockOrder: bool
    partImageCount: int
    hasCoreChargePart: bool
    isCoreCharge: bool
    corePartNumber: Optional[str]
    extendedAttributes: str
    packagingImageUUIDs: List[str]
    partSubTypes: List[Any]
    images: List[Any]
    systemGroupID: int
    hazardMaterialInfo: Optional[Any]
    partCompatibility: Optional[Any]
    pricingNotes: Optional[Any]
    isMOQ: bool
    moqQuantity: int


class SystemGroupPartResponse(BaseModel):
    vin: Optional[str]
    catalogId: int
    catalogExternalReference: str
    catalogName: str
    catalogModelId: int
    catalogModelTypeID: int
    catalogModelName: str
    catalogModelTitle: str
    countryCode: str
    currency: str
    id: int
    titleOriginal: str
    title: str
    subcategoryId: int
    subcategoryExternalReference: str
    subcategoryTitleOriginal: str
    subcategoryTitle: str
    categoryId: int
    categoryExternalReference: str
    categoryTitleOriginal: str
    categoryTitle: str
    images: Optional[Any]
    parts: List[Part]
    showPrice: bool
    partSource: int
    pointOfImpacts: List[Any]
    systemGroupImages: Optional[List[SystemGroupImage]]
    externalReference: str
    canBuy: bool
    generation: str
    showPartImage: bool
    extendedAttributes: Optional[Any]
