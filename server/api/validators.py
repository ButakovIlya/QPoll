from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from .exсeptions import PollValidationException
from api.utils import check_file

from datetime import datetime, timedelta

import re

class BaseValidator:

    def name(value, chars=None):
        if not chars:
            if len(value) > 200:
                raise ValidationError("Название должно содержать менее 200 символов.")
        else:
            if len(value) > chars:
                raise ValidationError(f"Название должно содержать менее {chars} символов.")
        
    def info(value, chars=None):
        if value:
            if not chars:
                if len(value) > 500:
                    raise ValidationError("Описание должно содержать не более 500 символов.")
            else:
                if len(value) > chars:
                    raise ValidationError("Описание должно содержать не более 500 символов.")

    def description(value, chars=None):
        if value and not value == "":
            if value and len(value) > 1000:
                raise ValidationError("Описание должно содержать менее 1000 символов.")

    def image(image):    
        is_img_ok, details = check_file(image)

        if not is_img_ok:
            raise ValidationError(detail=details)
        
    def quantity(value):
        if value < 0:
            raise ValidationError("Количество должно быть положительным числом.")



class ProfileValidator(BaseValidator):

    def name(value):
        if len(value) > 50:
            raise ValidationError("Имя должно содержать менее 50 символов.")

    def surname(value):
        if len(value) > 50:
            raise ValidationError("Фимилия должна содержать менее 50 символов.")
        
    def patronymic(value):
        if len(value) > 50:
            raise ValidationError("Отчество должно содержать менее 50 символов.")
        
    def number(value):
        pass
        # if not is_number_valid(value):
        #     raise ValidationError(f"Номер телефона '{value}' введен некорректно.")
            
    def email(value):
        if not is_email_valid(value):
            raise ValidationError(f"Почта '{value}' введена некорректно.")

    def sex(value):
        if not value in ['М', 'Ж']:
            raise ValidationError(f"Пол '{value}' введен некорректно. Ожидается 'М' или 'Ж'.")

    def joining_date(value):
        from datetime import datetime
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValidationError(f"Дата '{value}' введена некорректно. Ожидается 'YYYY-MM-DD'.")


class PollValidator(BaseValidator):

    def name(value):
        if len(value) > 150:
            raise ValidationError("Название должно содержать менее 150 символов.")

    def duration(value):
        pass
        
    def is_in_production(value):
        if value:
            if value == False:
                raise ValidationError("Нельзя убрать опрос из продакшена, можно только удалить сам опрос.")

class BasePollSettingsValidator(BaseValidator):

    def max_revotes_quantity(value, num=None):
        if num:
            if value > num:
                raise ValidationError(f"Количество повторных голосований не может превышать {num}")
        else:
            if value > 5:
                raise ValidationError(f"Количество повторных голосований ответа не может быть более {10}")
            
    def completion_time(value):
        if value >= timedelta(hours=24):
            raise ValidationError("Время прохождения опроса не может превышать 24 часа.")
        
    def duration(value):
        if value >= timedelta(hours=24):
            raise ValidationError("Длительность не может превышать 24 часа.")
    
    def start_time(value):
        current_time = datetime.now(value.tzinfo)
        if value + timedelta(minutes=10) < current_time:
            raise ValidationError("Время начала не может быть раньше текущего времени более чем на 10 минут.")
        
    def end_time(value):
        current_time = datetime.now(value.tzinfo)
        if value < current_time:
            raise ValidationError("Время окончания не может быть раньше текущего времени.")



def is_number_valid(value):
    pattern = r'^(\+7|8)[\d]{10}$'
    if re.match(pattern, value):
        return True
    return False

def is_email_valid(value):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, value):
        return True
    return False


class BaseReleaseValidator():
    def __init__(self, instance, poll=None) -> None:
            self.instance = instance
            self.poll = poll

    def validate(self):
        methods = [method for method in dir(self) if callable(getattr(self, method)) and method.startswith('validate_')]
        for method_name in methods:
            getattr(self, method_name)()
        
        return True

class ReleasePollValidator(BaseReleaseValidator):

    def validate_name(self, max_len=None, min_len=None):
        value = getattr(self.instance, "name", None)
        
        if not value:
            raise PollValidationException(f"Заголовок текущего опроса не должен быть пустым.")
        

        if not min_len:
            if len(value) < 5:
                raise PollValidationException(f"Заголовок текущего опроса должен содержать не менее 5 символов.")
        else:
            if len(value) < min_len:
                raise PollValidationException(f"Заголовок текущего опроса должен содержать более {min_len - 1} символов.")
            
        if not max_len:
            if len(value) > 150:
                raise PollValidationException(f"Заголовок текущего опроса должен содержать менее 150 символов.")
        else:
            if len(value) > max_len:
                raise PollValidationException(f"Заголовок текущего опроса должен содержать менее {max_len} символов.")


class ReleaseQuestionValidator(BaseReleaseValidator):

    def validate_name(self, max_len=None, min_len=None):
        value = getattr(self.instance, "name", None)

        if not value:
            raise PollValidationException(f"Текст вопроса №{self.instance.order_id} не должен быть пустым.")

        if not min_len:
            if len(value) < 5:
                raise PollValidationException(f"Текст вопроса №{self.instance.order_id} должен содержать не менее 5 символов.")
        else:
            if len(value) < min_len:
                raise PollValidationException(f"Текст вопроса №{self.instance.order_id} должен содержать более {min_len - 1} символов.")
            
        if not max_len:
            if len(value) > 150:
                raise PollValidationException(f"Текст вопроса №{self.instance.order_id} должен содержать менее 150 символов.")
        else:
            if len(value) > max_len:
                raise PollValidationException(f"Текст вопроса №{self.instance.order_id} должен содержать менее {max_len} символов.")
            

class ReleaseOptionValidator(BaseReleaseValidator):

    def validate_name(self, max_len=None, min_len=None):
        value = getattr(self.instance, "name", None)
        is_free_response = getattr(self.instance, "is_free_response", False)

        if not value and not is_free_response:
            raise PollValidationException(f"Текст варианта ответа №{self.instance.order_id} вопроса №{self.instance.question.order_id} не должен быть пустым.")
        
        if not is_free_response:
            if not min_len:
                if len(value) < 1:
                    raise PollValidationException(f"Текст варианта ответа №{self.instance.order_id} вопроса №{self.instance.question.order_id} должен содержать не менее 1 символа.")
            else:
                if len(value) < min_len:
                    raise PollValidationException(f"Текст варианта ответа №{self.instance.order_id} вопроса №{self.instance.question.order_id} должен содержать более {min_len - 1} символов.")
                
            if not max_len:
                if len(value) > 150:
                    raise PollValidationException(f"Текст варианта ответа №{self.instance.order_id} вопроса №{self.instance.question.order_id} должен содержать менее 150 символов.")
            else:
                if len(value) > max_len:
                    raise PollValidationException(f"Текст варианта ответа №{self.instance.order_id} вопроса №{self.instance.question.order_id} должен содержать менее {max_len} символов.")
            

class ReleasePollSettingsValidator(BaseReleaseValidator):
        
    def validate_completion_time(self):
        value = getattr(self.instance, 'completion_time', None)
        if value:
            if self.instance.completion_time < timedelta(minutes=1):
                raise PollValidationException(f"Прохождение опроса не может длиться меньше 1 минуты")
            
            if self.instance.completion_time > timedelta(days=1):
                raise PollValidationException(f"Прохождение опроса не может длиться дольше 1 дня")
    
    def validate_start_time(self):
        value = getattr(self.instance, 'start_time', None)
        if value:
            if self.instance.start_time + timedelta(hours=1) < datetime.now():
                raise PollValidationException(f"Начало опроса должно быть не более чем на час раньше текущего времени")
            
            if self.instance.start_time > datetime.now() + timedelta(weeks=1):
                raise PollValidationException(f"Прохождение опроса не может быть запланировано больше чем на неделю заранее")
            
            end_time =  getattr(self.instance, 'end_time', None)
            if end_time:
                if self.instance.start_time + timedelta(minutes=1) > self.instance.end_time:
                    raise PollValidationException(f"Время начала опроса должно быть на минимум минуту меньше времени окончания")

    def validate_end_time(self):
        value = getattr(self.instance, 'end_time', None)
        if value:
            if self.instance.end_time + timedelta(minutes=5) < datetime.now():
                raise PollValidationException(f"Окончание опроса должно на 5 минут позже текущего времени")
            
            if self.instance.end_time > datetime.now() + timedelta(weeks=2):
                raise PollValidationException(f"Окончание опроса не может быть запланировано больше чем на 2 недели заранее")
            
            start_time =  getattr(self.instance, 'start_time', None)
            if start_time:
                if self.instance.start_time + timedelta(minutes=1) > self.instance.end_time:
                    raise PollValidationException(f"Время окончания опроса должно быть на минимум минуту позже времени начала")

    def validate_registration_start_time(self):
        registration_start_time = getattr(self.instance, 'registration_start_time', None)
        start_time = getattr(self.instance, 'start_time', None)
        if registration_start_time:
            if not start_time:
                raise PollValidationException(f"При указании времени начала регистрации на опрос, необходимо указать время начала опроса")

            if registration_start_time + timedelta(minutes=15) >= start_time:
                raise PollValidationException(f"Регистрация на опрос должна быть минимум на 15 минут раньше начала опроса")
            
            if registration_start_time + timedelta(weeks=1) < datetime.now():
                raise PollValidationException(f"Регистрация на опрос не может быть запланирована больше чем на неделю заранее")
            
            registration_end_time = getattr(self.instance, 'registration_end_time', None)
            if registration_end_time:
                if registration_start_time + timedelta(minutes=15) >= registration_end_time:
                    raise PollValidationException(f"Время начала регистрации на опрос должно быть минимум на 15 минут меньше времени окончания регистрации")

    def validate_registration_time(self):
        registration_end_time = getattr(self.instance, 'registration_end_time', None)
        start_time = getattr(self.instance, 'start_time', None)
        if registration_end_time:
            if not start_time:
                raise PollValidationException(f"При указании времени окончания регистрации на опрос, необходимо указать время начала опроса")
            
            if registration_end_time + timedelta(minutes=5) >= start_time:
                raise PollValidationException(f"Окончание регистрации на опрос должна быть минимум на 5 минут раньше начала опроса")
              
            if registration_end_time > datetime.now() + timedelta(weeks=1):
                raise PollValidationException(f"Окончание регистрации на опрос не может быть запланировано больше чем на неделю заранее")
            
            registration_start_time =  getattr(self.instance, 'registration_start_time', None)
            if registration_start_time:
                if registration_start_time + timedelta(minutes=10) > registration_end_time:
                    raise PollValidationException(f"Окончание регистрации на опрос должна быть минимум на 10 минут раньше начала регистрации")
                
        
def is_poll_valid(poll):
    poll_validator = ReleasePollValidator(poll)
    poll_validator.validate()

    all_questions = poll.questions.all()
    if len(all_questions) == 0:
        raise PollValidationException(f"Текущий опрос должен содержать хотя бы 1 вопрос.")
    
    for question in all_questions:
        poll_question_validator = ReleaseQuestionValidator(question)
        poll_question_validator.validate()
        
        all_options = question.answer_options.all()
        if len(all_options) == 0:
            raise PollValidationException(f"Вопрос №{question.order_id} должен содержать хотя бы 1 вариант ответа.")
    
        if question.is_free:
            if len(all_options) > 1:
                raise PollValidationException(f"Вопрос №{question.order_id} является свободным и должен содержать 1 вариант ответа.")

        free_options_quantity = len([option for option in all_options if option.is_free_response == True])
        if free_options_quantity > 1:
            raise PollValidationException(f"Вопрос №{question.order_id} не может содержать более 1 свободного ответа.")

        for option in all_options:
            poll_option_validator = ReleaseOptionValidator(option)
            poll_option_validator.validate()

        if poll.poll_type.name == 'Викторина':
            has_correct_option = [option for option in all_options if option.is_correct]
            if not has_correct_option:
                raise PollValidationException(f"Вопрос №{question.order_id} должен содержать хотя бы 1 верный вариант ответа.")

    if poll.poll_type.name == 'Быстрый':
        if [auth_field for auth_field in poll.auth_fields.all() if (auth_field.name == None or auth_field.name == '')]:
            raise PollValidationException(f"Содержание полей авторизации не может быть пустым.")
        
        if not len([auth_field for auth_field in poll.auth_fields.all() if auth_field.is_main == True]) == 1:
            raise PollValidationException(f"Должно быть ровно 1 обязательное поле авторизации.")


    poll_setts_validator = ReleasePollSettingsValidator(poll.poll_setts, poll)
    poll_setts_validator.validate()

    return True


