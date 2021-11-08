import functools
from common.consts import PRODUCT_CODE_TO_NAME


def translated_names(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        items = f(*args, **kwargs)
        if items:
            items = convertCodestoNames(items)
        return items
    return wrapper


def convertCodestoNames(items):
    new_res = {}
    for k, v in items.items():
        if k in PRODUCT_CODE_TO_NAME:
            new_res[PRODUCT_CODE_TO_NAME[k]] = v
        else:
            new_res[k] = v
    return new_res
