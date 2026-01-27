import json
import os
import uuid
import requests
from fastapi import FastAPI, HTTPException, Request
from models.image import ImageModel
from response.country import CountryResponse
from response.catalog import CatalogResponse
from response.category import CategoryResponse
from response.subcategory import SubcategoryResponse
from response.system_group import SystemGroupResponse
from response.system_group_part import SystemGroupPartResponse
from response.system_group_part import SystemGroupImage as SystemGroupPartImageResponse
from response.vin import VinResponse
from models.country import CountryModel
from models.catalog import CatalogModel
from models.category import CategoryModel
from models.subcategory import SubcategoryModel
from models.system_group import SystemGroupModel
from models.system_group_part import SystemGroupPartModel
from dotenv import load_dotenv

app = FastAPI(
    title="Tesla EPC API",
    version="2026.1.0",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
)

load_dotenv()
BUCKET = os.getenv("S3_BUCKET")
REGION = os.getenv("AWS_REGION")
NO_IMAGE_PNG_FILE = "no-image.png"
NO_IMAGE_SVG_FILE = "no-image.svg"


@app.get("/vin/{vin}", response_model=VinResponse)
async def get_vin(vin):
    try:
        response = requests.get(f"https://epcapi.tesla.com/api/catalogs?vin={vin}")
        response.raise_for_status()
        content = json.loads(response.text)

        return VinResponse(**content["responseObject"][0])
    except Exception as e:
        raise HTTPException(400, "Catalog not available for this VIN")


@app.get("/country", response_model=list[CountryResponse])
async def get_country():
    response = []
    rows = CountryModel.get_all()
    for row in rows:
        data = json.loads(row["data"])
        response.append(CountryResponse(**data))

    return response


@app.get("/catalog/{country_code}", response_model=list[CatalogResponse])
async def get_catalog(country_code: str):
    response = []
    rows = CatalogModel.get_by_country_code(country_code)
    if len(rows) == 0:
        raise HTTPException(404)
    for row in rows:
        data = json.loads(row["data"])
        response.append(CatalogResponse(**data))
    return response


@app.get("/category/{catalog_id}", response_model=list[CategoryResponse])
async def get_category(catalog_id: int):
    response = []
    rows = CategoryModel.get_by_catalog(catalog_id)
    if len(rows) == 0:
        raise HTTPException(404)
    for row in rows:
        data = json.loads(row["data"])
        model = CategoryResponse(**data)
        db_image = ImageModel.get_image("category", row["reference"])
        if db_image:
            model.image = generate_s3_url(db_image["entity"], db_image["name"])

        response.append(model)

    return response


@app.get("/subcategory/{category_id}", response_model=list[SubcategoryResponse])
async def get_subcategory(category_id: int):
    response = []
    rows = SubcategoryModel.get_by_category(category_id)
    if len(rows) == 0:
        raise HTTPException(404)
    for row in rows:
        data = json.loads(row["data"])
        response.append(SubcategoryResponse(**data))

    return response


@app.get("/system-group/{subcategory_id}", response_model=list[SystemGroupResponse])
async def get_group(subcategory_id: int):
    response = []
    rows = SystemGroupModel.get_by_subcategory(subcategory_id)
    if len(rows) == 0:
        raise HTTPException(404)
    for row in rows:
        data = json.loads(row["data"])
        model = SystemGroupResponse(**data)
        model.images = ""
        for key, image in enumerate(model.systemGroupImages):
            db_image = ImageModel.get_image("group", model.externalReference, None, image.mimetype)
            if not db_image:
                continue

            model.systemGroupImages[key].imageURL = generate_s3_url(db_image["entity"], db_image["name"])

        if len(model.systemGroupImages) == 0:
            model.systemGroupImages = fill_empty_system_group_images()

        response.append(model)

    return response


@app.get("/system-group-part/{group_id}", response_model=SystemGroupPartResponse)
async def get_system_group_part(group_id: int):
    system_group = SystemGroupPartModel.get_by_id(group_id)
    if system_group is None:
        raise HTTPException(404)

    data = json.loads(system_group["data"])
    model = SystemGroupPartResponse(**data)
    for key, image in enumerate(model.systemGroupImages):
        db_image = ImageModel.get_image("group", model.externalReference, None, image.mimetype)
        if not db_image:
            continue

        model.systemGroupImages[key].imageURL = generate_s3_url(db_image["entity"], db_image["name"])

    if len(model.systemGroupImages) == 0:
        model.systemGroupImages = fill_empty_system_group_images()

    return model


def generate_s3_url(entity, key) -> str:
    return f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{entity}/{key}"

def fill_empty_system_group_images() -> list:
    return [
        SystemGroupPartImageResponse(
            mimetype="image/svg+xml",
            imageURL=generate_s3_url("none", "no-image.svg"),
            fileName="no-image.svg",
            uuid=str(uuid.uuid4()),
            attributes="",
            extendedAttributes=[]
        ),
        SystemGroupPartImageResponse(
            mimetype="image/png",
            imageURL=generate_s3_url("none", "no-image.png"),
            fileName="no-image.png",
            uuid=str(uuid.uuid4()),
            attributes="",
            extendedAttributes=[]
        )
    ]
