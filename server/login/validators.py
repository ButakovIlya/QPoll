from rest_framework.exceptions import ValidationError
import re
from datetime import date

def validate_password(value):
    if len(value) < 8:
        raise ValidationError("Пароль должен содержать не менее 8 символов.")
    if len(value) > 50:
        raise ValidationError("Пароль должен содержать не более 50 символов.")


def validate_name(value):
    if not re.match("^[а-яА-Я-]+$", value):
        raise ValidationError("Имя должно содержать только буквы на русском языке.")
    if not 1 <= len(value) <= 50:
        raise ValidationError("Имя должно содержать от 1 до 50 символов.")


def validate_surname(value):
    if not re.match("^[а-яА-Я-]+$", value):
        raise ValidationError("Фамилия должна содержать только буквы на русском языке.")
    if not 1 <= len(value) <= 50:
        raise ValidationError("Фамилия должна содержать от 1 до 50 символов.")


def validate_patronymic(value):
    if value:
        if not re.match("^[а-яА-Я-]+$", value):
            raise ValidationError("Отчество должно содержать только буквы на русском языке.")
        if not 1 <= len(value) <= 50:
            raise ValidationError("Отчество должно содержать от 1 до 50 символов.")


def validate_sex(value):
    if value not in ['Ж', 'М']:
        raise ValidationError("Пол должен быть 'М' или 'Ж'.")


def validate_number(value):
    if not re.match(r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$', value):
        raise ValidationError("Номер телефона должен быть в формате +7 (012) 345-67-89.")

    

def validate_birthdate(value):
    if not isinstance(value, date):
        raise ValidationError("Неверный формат даты.")
    
    if value > date.today():
        raise ValidationError("Дата рождения не может быть в будущем.")

    age = date.today().year - value.year - ((date.today().month, date.today().day) < (value.month, value.day))
    if age < 14:
        raise ValidationError("Вам должно быть больше 14 лет для регистрации.")


def validate_email_address(value):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        raise ValidationError("Введите корректный адрес электронной почты.")
