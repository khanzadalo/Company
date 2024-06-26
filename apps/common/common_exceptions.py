from rest_framework.exceptions import APIException


class OnlyAdmin(APIException):
    status_code = 403
    default_detail = 'только Админы могут менять этот параметр'
    default_code = 'ошибка доступа'


class AlreadyExist(APIException):
    status_code = 400
    default_detail = 'такой пользователь уже есть'
    default_code = 'ошибка доступа'