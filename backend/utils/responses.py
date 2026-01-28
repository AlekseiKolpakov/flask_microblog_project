def success(data: dict | None = None, status: int = 200):
    """
    Формирует успешный ответ API.

    Используется всеми эндпоинтами при корректном выполнении запроса.

    :param data: Дополнительные данные ответа (опционально)
    :param status: HTTP-статус ответа (по умолчанию 200)
    :return: Кортеж (response_dict, status_code)
    """
    response = {"result": True}
    if data is not None:
        response.update(data)
    return response, status


def error(error_type: str, message: str, status: int = 400):
    """
    Формирует ответ API с ошибкой.

    Используется для всех ошибок в бизнес-логике и HTTP-ошибок,
    чтобы поддерживать единый формат ответа.

    Формат соответствует требованиям ТЗ:
    {
        "result": false,
        "error_type": str,
        "error_message": str
    }

    :param error_type: Тип ошибки (auth_error, validation_error и т.д.)
    :param message: Читаемое человеком описание ошибки
    :param status: HTTP-статус ответа
    :return: Кортеж (response_dict, status_code)
    """
    return {
        "result": False,
        "error_type": error_type,
        "error_message": message,
    }, status
