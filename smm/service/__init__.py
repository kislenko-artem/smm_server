from datetime import datetime


def class_to_dict(item) -> dict:
    data = item.__dict__
    for key in data:
        if isinstance(data[key], datetime):
            data[key] = data[key].isoformat()
        if isinstance(data[key], list):
            data[key] = list_to_dict(data[key])
        if hasattr(data[key], "__annotations__"):
            data[key] = class_to_dict(data[key])
    return data


def list_to_dict(obj: list) -> list:
    r_data = []
    for item in obj:
        data = class_to_dict(item)
        r_data.append(data)

    return r_data
