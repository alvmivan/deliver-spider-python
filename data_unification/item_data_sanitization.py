name_to_type = {
    # required
    "name": str,
    "price": int,
    "url": str,
    # not required but type must match
    "photo": str,
    "details": str,
    "brand": str
}

item_fields = name_to_type.keys()
required_fields = ["name", "price", "url"]


def validate_field(item_dict):
    for field in required_fields:
        if field not in item_dict:
            return False, f"Field {field} is required"
    for field in item_dict:
        if field not in item_fields:
            return False, f"Field {field} is not a valid field"
        if not isinstance(item_dict[field], name_to_type[field]):
            return False, f"Field {field} is not of type {name_to_type[field]}"
    return True, ""


common_weird_characters = ["\u200b", "\u200c", "\u200d", "\u200e", "\u200f", "\u202a", "\u202b", "\u202c", " ", "�", ]
invalid_characters = ["\n", "\t", "\r"]


def sanitize_item(item):
    for key in item.keys():

        # replace weird characters with spaces
        if type(item[key]) == str:
            for weird_character in common_weird_characters:
                if weird_character in item[key]:
                    item[key] = item[key].replace(weird_character, " ")
            for invalid_character in invalid_characters:
                if invalid_character in item[key]:
                    item[key] = item[key].replace(invalid_character, "")
            item[key] = item[key].strip()
            # if there is many spaces, replace them with one space
            while "  " in item[key]:
                item[key] = item[key].replace("  ", " ")

        # remover description y brand si existen como keys
    if "description" in item:
        del item["description"]
    if "brand" in item:
        del item["brand"]

    return item


def test_validate_field():
    item_correcto_01 = {
        "name": "Pintura",
        "price": 100,
        "photo": "https://www.google.com",
        "details": "Pintura de calidad",
        "url": "https://www.google.com",
        "brand": "Marca"
    }

    item_correcto_02 = {
        "name": "Pintura",
        "price": 100,
        "url": "https://www.google.com"
    }

    item_incorrecto_01 = {
        "name": "Pintura",
        "price": 100,
        "photo": "https://www.google.com",
        "details": "Pintura de calidad",
        "brand": "Marca"
    }

    item_incorrecto_02 = {
        "name": "Pintura",
        "price": "100",
        "photo": "https://www.google.com",
        "details": "Pintura de calidad",
        "url": "https://www.google.com",
        "brand": "Marca"
    }
    item_incorrecto_03 = {
        "name": "Pintura",
        "price": 100,
        "photo": "https://www.google.com",
        "details": "Pintura de calidad",
        "url": "https://www.google.com",
        "brand": ["Mar", "Ca"]
    }

    assert validate_field(item_correcto_01) == (True, "")
    assert validate_field(item_correcto_02) == (True, "")
    assert validate_field(item_incorrecto_01) == (False, "Field url is required")
    assert validate_field(item_incorrecto_02) == (False, "Field price is not of type <class 'int'>")
    assert validate_field(item_incorrecto_03) == (False, "Field brand is not of type <class 'str'>")
    print("All investigation_playground passed")


if __name__ == "__main__":
    test_validate_field()
