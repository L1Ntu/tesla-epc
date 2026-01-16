import json

import requests
from fastapi import FastAPI, HTTPException, Request
from response.country import CountryResponse
from response.catalog import CatalogResponse
from response.category import CategoryResponse
from response.subcategory import SubcategoryResponse
from response.system_group import SystemGroupResponse
from response.system_group_part import SystemGroupPartResponse
from response.vin import VinResponse
from models.country import CountryModel
from models.catalog import CatalogModel
from models.category import CategoryModel
from models.subcategory import SubcategoryModel
from models.system_group import SystemGroupModel
from models.system_group_part import SystemGroupPartModel

app = FastAPI(
    title="Tesla EPC API",
    version="2026.1.0",
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}}
)


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
        response.append(CategoryResponse(**data))

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


@app.get('/system-group/{subcategory_id}', response_model=list[SystemGroupResponse])
async def get_group(subcategory_id: int):
    response = []
    rows = SystemGroupModel.get_by_subcategory(subcategory_id)
    if len(rows) == 0:
        raise HTTPException(404)
    for row in rows:
        data = json.loads(row["data"])
        response.append(SystemGroupResponse(**data))

    return response


@app.get('/system-group-part/{group_id}', response_model=SystemGroupPartResponse)
async def get_system_group_part(group_id: int):
    system_group = SystemGroupPartModel.get_by_id(group_id)
    if system_group is None:
        raise HTTPException(404)

    data = json.loads(system_group["data"])
    print(json.dumps(data, indent=2))
    return SystemGroupPartResponse(**data)
