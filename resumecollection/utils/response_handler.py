def validation_exception_handler(validation_exception):
    data = {}
    for key in validation_exception.detail.keys():
        data[key] = "".join(str(validation_exception.detail.get(key)))
    return {"errors": data}
