import argparse
import requests
import json
import imghdr
import mimetypes
import os
import tqdm
from db import Database
from models.country import CountryModel
from models.catalog import CatalogModel
from models.category import CategoryModel
from models.subcategory import SubcategoryModel
from models.system_group import SystemGroupModel
from models.system_group_part import SystemGroupPartModel
from models.part import PartModel
from models.part_image import PartImageModel
from models.image import ImageModel

db = Database(db_path="tesla.db")


def parse_country() -> None:
    """
    parse countries
    """
    print("-> parsing countries")
    url = "https://epcapi.tesla.com/api/countries"

    response = requests.get(url)
    data = response.json()
    if not data.get("success") or data["success"] is False:
        raise Exception("countries request failed")

    for d in data["responseObject"]:
        CountryModel(code=d["code"], name=d["name"], data=d).save()


def parse_catalog() -> None:
    """
    parse catalogs
    """
    print("-> parsing catalog")
    url = "https://epcapi.tesla.com/api/catalogs?countryCode="
    codes = db.fetchall("SELECT code FROM country")
    for row in codes:
        cc = row["code"]
        print(f"  - country = {row['code']}")
        response = requests.get(f"{url}{cc}")
        data = response.json()
        if not data.get("success") or data["success"] is False:
            raise Exception("catalog request failed")

        for d in data["responseObject"]:
            CatalogModel(
                id=d["id"],
                name=d["name"],
                description=d["catalogModelTypeDescription"],
                country_code=d["countryCode"],
                reference=d["externalReference"],
                data=d,
            ).save()


def parse_category() -> None:
    """
    parse category/subcategory/system-group
    """
    print("-> parsing category")
    url = "https://epcapi.tesla.com/api/catalogs/{catalog_reference}/categories"

    catalogs = db.fetchall("SELECT id, reference FROM catalog")
    for row in catalogs:
        catalog_id = row["id"]
        catalog_reference = row["reference"]
        print(f" -> parsing catalog_id={catalog_id} reference={catalog_reference}")
        if catalog_id < 88:
            continue

        catalog_url = url
        catalog_url = catalog_url.replace("{catalog_reference}", catalog_reference)

        response = requests.get(catalog_url)
        data = response.json()
        if not data.get("success") or data["success"] is False:
            raise Exception("category request failed")

        for d in data["responseObject"]:
            CategoryModel(
                id=d["id"],
                catalog_id=catalog_id,
                name=d["title"],
                reference=d["externalReference"],
                image=d["image"],
                data=d,
            ).save()

            for sub in d["subCategories"]:
                SubcategoryModel(
                    id=sub["id"],
                    category_id=sub["categoryId"],
                    name=sub["title"],
                    reference=sub["externalReference"],
                    data=sub,
                ).save()

                for group in sub["systemGroups"]:
                    SystemGroupModel(
                        id=group["id"],
                        subcategory_id=group["subcategoryId"],
                        is_parsed=0,
                        name=group["title"],
                        reference=group["externalReference"],
                        data=group,
                    ).save()


def parse_group() -> None:
    """
    parse system-group
    """
    print("-> parse group")
    groups = SystemGroupModel.get_not_parsed(limit=1000)
    for group in groups:
        try:
            group_id = group["group_id"]
            print(f"-> parsing group {group_id}")
            url = "https://epcapi.tesla.com/api/catalogs/{catalog}/systemgroups/{group}"
            url = url.replace("{catalog}", group["catalog_reference"])
            url = url.replace("{group}", group["group_reference"])

            response = requests.get(url)
            data = response.json()

            if not data.get("success") or data["success"] is False:
                raise Exception("category request failed")

            SystemGroupPartModel(
                group_id=group_id, is_parsed=0, data=data["responseObject"]
            ).save()
            SystemGroupModel.set_parsed(group["group_id"])
        except requests.JSONDecodeError:
            continue


def parse_part():
    print("->parse part")
    parts = SystemGroupPartModel.get_not_parsed(limit=10000)
    for item in parts:
        data = json.loads(item["data"])
        catalog_ref = data["catalogExternalReference"]
        group_ref = data["externalReference"]

        for p in data["parts"]:
            part_id = p["partId"]
            part_number = p["partNumber"]
            catalog_number = p["catalogPartNumber"]
            name = p["title"]
            images = []

            if part_number == "N/A":
                continue

            for uuid in p["packagingImageUUIDs"]:
                images.append(
                    {
                        "part_id": part_id,
                        "uuid": uuid,
                        "url": f"https://epcapi.tesla.com/api/catalogs/{catalog_ref}/systemGroups/{group_ref}/partImage?partNumber={part_number}&imageUUID={uuid}",
                    }
                )

            if not PartModel.isset_part(part_id):
                PartModel(
                    id=part_id,
                    part_number=part_number,
                    catalog_number=catalog_number,
                    name=name,
                ).save()
                for image in images:
                    PartImageModel(
                        part_id=part_id,
                        is_parsed=0,
                        uuid=image["uuid"],
                        url=image["url"],
                    ).save()
            else:
                print(f"part_id={part_id} already exists")

        SystemGroupPartModel.set_parsed(item["group_id"])


def parse_category_image():
    """
    category image
    only one per category, some of them not exists
    :return:
    """
    data = CategoryModel.get_for_image()
    pbar = tqdm.tqdm(data)
    for d in pbar:
        try:
            uuid = str(d["reference"]).lower()
            url = d["image"]
            pbar.set_description(f"processing image {uuid}")

            exist_path = os.path.join("image", "category", f"{uuid}.jpeg")
            if os.path.exists(exist_path):
                continue

            response = requests.get(url)
            response.raise_for_status()
            image_data = identify_image(response, uuid, False)

            if not image_data:
                raise Exception("error")
            path = os.path.join("image", "category", image_data["filename"])
            with open(path, "wb") as f:
                f.write(response.content)
                ImageModel(
                    entity="category", uuid=uuid, ext=image_data["extension"], mimetype=image_data["mimetype"],
                    size=image_data["size"], name=image_data["filename"]
                ).save()
        except KeyboardInterrupt:
            exit(0)
        except requests.RequestException:
            if not response.status_code == 404:
                print(f"error while parsing {uuid}, response code = {response.status_code}")


def parse_group_image() -> None:
    """
    parse group images
    usually 2 images per group: svg + png
    :return:
    """
    data = SystemGroupModel.get_for_image()
    pbar = tqdm.tqdm(data)
    for d in pbar:
        try:
            uuid = str(d["reference"]).lower()
            j = json.loads(d["data"])
            images = j["systemGroupImages"]

            exist_path = os.path.join("image", "group", f"{uuid}.svg")
            if os.path.exists(exist_path):
                continue

            for image in images:
                url = image["imageURL"]

                response = requests.get(url)
                response.raise_for_status()
                image_data = identify_image(response, uuid, image["mimetype"] == "image/svg+xml")

                if not image_data:
                    raise Exception(f"not an image, uuid = {uuid}, url = {url}")
                path = os.path.join("image", "group", image_data["filename"])
                with open(path, "wb") as f:
                    f.write(response.content)
                    ImageModel(
                        entity="group", uuid=uuid, ext=image_data["extension"], mimetype=image_data["mimetype"],
                        size=image_data["size"], name=image_data["filename"]
                    ).save()
        except KeyboardInterrupt:
            exit(0)
        except requests.RequestException:
            print(f"error parsing {uuid}")


def identify_image(response: requests.Response, uuid: str, is_svg: bool) -> dict | bool:
    """
    identifies if given content is valid image
    :param response:
    :param uuid:
    :param is_svg:
    :return:
    """
    content = response.content
    size = len(response.content)

    if is_svg:
        return {
            "mimetype": "image/svg+xml",
            "size": size,
            "extension": "svg",
            "filename": f"{uuid}.svg"
        }

    image_type = imghdr.what(None, content)
    if not image_type:
        return False

    mimetype = mimetypes.types_map.get(f".{image_type}", f"image/{image_type}")
    extension = image_type

    return {
        "mimetype": mimetype,
        "size": size,
        "extension": extension,
        "filename": f"{uuid}.{extension}"
    }


def init_db():
    CountryModel.create_table()
    CatalogModel.create_table()
    CategoryModel.create_table()
    SubcategoryModel.create_table()
    SystemGroupModel.create_table()
    SystemGroupPartModel.create_table()
    PartModel.create_table()
    PartImageModel.create_table()
    ImageModel.create_table()


def main():
    init_db()

    usage = """
    python3 main.py --action ACTION
    ACTION must be in same sequence as above and be one of:
     1. country
     2. catalog
     3. category
     4. group
     5. part
     6. category_image
     7. group_image
     8. part_image
    """

    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("--action", required=True,
                        choices=["country", "catalog", "category", "group", "part", "category_image", "group_image"])
    args = parser.parse_args()

    match args.action:
        case "country":
            parse_country()
        case "catalog":
            parse_catalog()
        case "category":
            parse_category()
        case "group":
            parse_group()
        case "part":
            parse_part()
        case "category_image":
            parse_category_image()
        case "group_image":
            parse_group_image()


if __name__ == "__main__":
    main()
