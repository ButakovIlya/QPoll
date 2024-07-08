from rest_framework.exceptions import APIException

class MissingFieldException(APIException):
    status_code = 400
    default_code = 'missing_field'

    def __init__(self, field_name, detail=None):
        if detail is None:
            detail = f"Поле '{field_name}' требуется передать в теле запроса."
        self.detail = detail

    def __str__(self):
        return self.detail


class MissingParameterException(APIException):
    status_code = 400
    default_code = 'missing_parameter'

    def __init__(self, field_name, detail=None):
        if detail is None:
            detail = f"Поле '{field_name}' требуется передать в параметрах запроса."
        self.detail = detail

    def __str__(self):
        return self.detail
    
class ObjectNotFoundException(APIException):
    status_code = 404
    default_code = 'object_not_found'

    def __init__(self, model=None, detail=None):
        if detail is None:
            detail = f"Объект модели '{model}' не найден."
        self.detail = detail

    def __str__(self):
        return self.detail
    
class ObjectAlreadyExistsException(APIException):
    status_code = 400
    default_code = 'profile_already_exists'

    def __init__(self, detail=None):
        if detail is None:
            detail = 'Объект данной модели уже существует.'
        self.detail = detail
    

class UniqueIdException(APIException):
    status_code = 400
    default_code = 'id_exists'

    def __init__(self, model=None, detail=None):
        if detail is None:
            detail = f'Id в модели {model} уже занят.'
        self.detail = detail
    
    

class AccessDeniedException(APIException):
    status_code = 403 
    default_detail = 'У Вас нет доступа к данному ресурсу.'
    default_code = 'access_denied'


class UserHasParticipatedException(APIException):
    status_code = 403 
    default_detail = 'Вы уже принимали участие в этом опросе.'
    default_code = 'user_has_participated'
    default_message = 'Вы уже принимали участие в этом опросе.'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_message
        super().__init__(detail, code)


class WrongFieldTypeException(APIException):
    status_code = 400
    default_code = 'wrong_field_type'

    def __init__(self, field_name=None, expected_type=None, detail=None):
        if detail is None:
            detail = f"Поле '{field_name}' должно быть типа '{expected_type}'."
        self.detail = detail



class InvalidFieldException(APIException):
    status_code = 400
    default_code = 'invalid_field'

    def __init__(self, field=None, detail=None):
        if detail is None:
            detail = f"Поле '{field}' введено некорректно"
        self.detail = detail


class BadImageException(APIException):
    status_code = 403
    default_code = 'bad_image'

    def __init__(self, field_name, expected_type, detail=None):
        if detail is None:
            detail = f"Поле '{field_name}' должно быть типа '{expected_type}'."
        self.detail = detail



class WrongPasswordException(APIException):
    status_code = 401
    default_code = 'wrong_password_or_login'

    def __init__(self, detail=None):
        if detail is None:
            detail = f"Неверный логин или пароль!"
        self.detail = detail

    def __str__(self):
        return self.detail
    

class PollAnsweringException(APIException):
    status_code = 400
    default_code = 'poll_answering'

    def __init__(self, detail=None):
        if not detail:
            detail = f"Ошибка при ответе на опрос"
        self.detail = detail

    def __str__(self):
        return self.detail
    

class TooManyInstancesException(APIException):
    status_code = 403
    default_code = 'too_many_instances'

    def __init__(self, model=None, limit=None, detail=None):
        if not detail:
            detail = f"Слишком много объектов модели '{model}'."
            if limit:
                detail += f"Максимально допустимое количество = {limit}"
        self.detail = detail

    def __str__(self):
        return self.detail
    

class MyValidationError(APIException):
    status_code = 400
    default_code = 'validation_error'

    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return self.detail
    
class MyCustomException(APIException):
    status_code = 400
    default_code = 'MyCustomException'

    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return self.detail
    

class PollValidationException(APIException):
    status_code = 202 
    default_detail = 'Ошибка валидации опроса при выходе в продакшн'
    default_code = 'PollValidationException'

    def __init__(self, detail=default_detail):
        self.detail = {'message':f"{detail}", 'severity': 'error'}


class InstanceNotFoundException(APIException):
    status_code = 404
    default_code = 'instance_not_found'

    def __init__(self, model=None, detail=None):
        if detail is None:
            detail = f"Объект модели '{model}' не найден."
        self.detail = detail

    def __str__(self):
        return self.detail