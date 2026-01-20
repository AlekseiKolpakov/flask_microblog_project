def success(data: dict | None = None, status: int = 200):
    response = {"result": True}
    if data is not None:
        response.update(data)
    return response, status


def error(error_type: str, message: str, status: int = 400):
    return {
        "result": False,
        "error_type": error_type,
        "error_message": message,
    }, status
