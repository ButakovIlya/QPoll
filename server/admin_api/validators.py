

from api.validators import BaseValidator, ValidationError


class BaseProjectSettingsValidator(BaseValidator):

    def max_questions_quantity(value, num=None):
        if num:
            if  not 0 < value < num:
                raise ValidationError(f"Количество вопросов не может превышать {num} и быть меньше 0")
        else:
            if 0 >= value > 100:
                raise ValidationError(f"Количество вопросов не может превышать {100} и быть меньше 0")
            
    def min_questions_quantity(value, num=None):
        if num:
            if not 0 < value > num:
                raise ValidationError(f"Количество вопросов не может быть менее {num}")
        else:
            if not 0 < value > 1:
                raise ValidationError(f"Количество вопросов не может быть меньше {1}")
            
    def max_question_options_quantity(value, num=None):
        if num:
            if value > num:
                raise ValidationError(f"Количество вариантов ответа не может превышать {num}")
        else:
            if value > 100:
                raise ValidationError(f"Количество вариантов ответа не может превышать {100}")
            
    def min_question_options_quantity(value, num=None):
        if num:
            if value < num:
                raise ValidationError(f"Количество вариантов ответа не может превышать {num}")
        else:
            if value < 1:
                raise ValidationError(f"Количество вариантов ответа не может быть меньше {1}")
            
