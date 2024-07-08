import random
import string
import secrets
from django.core.mail import send_mail
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils import timezone
from qpoll.settings import DEFAULT_FROM_EMAIL

def generate_random_code():
    return ''.join(random.choices(string.digits, k=6))


def send_reset_code_email(email, code):
    subject = 'Код для восстановления пароля'
    message = f'Ваш код восстановления: {code}'
    from_email = DEFAULT_FROM_EMAIL 
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def store_reset_code_in_cache(email, code):
    cache_key = f'reset_code:{email}'
    cache.set(cache_key, {'code': code, 'created_at': timezone.now()}, timeout=300)

def check_reset_code_in_cache(email):
    cache_key = f'reset_code:{email}'
    reset_data = cache.get(cache_key)
    if reset_data:
        code = reset_data.get('code')
        created_at = reset_data.get('created_at')
        return code, created_at
    return None, None

def check_reset_code_times_in_cache(email):
    cache_key_times = f'reset_code_times:{email}'
    cache_key_reset = f'reset_code:{email}'

    reset_code_times = cache.get(cache_key_times, 1)

    if reset_code_times < 2:
        cache.set(cache_key_times, reset_code_times + 1, timeout=300)
        remaining_time = None
    elif reset_code_times >= 2:
        reset_code_data = cache.get(cache_key_reset)
        if reset_code_data:
            created_at = reset_code_data.get('created_at')
            time_elapsed = timezone.now() - created_at
            remaining_time = max(0, 300 - time_elapsed.total_seconds())
        else:
            remaining_time = None

    return reset_code_times, remaining_time

          

def get_reset_code_from_cache(email):
    cache_key = f'reset_token:{email}'
    return cache.get(cache_key)


def reset_password_after_code_validation(email, new_password):
    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return True
    except Exception:
        return False
    

def generate_random_token(length=32):
    characters = string.ascii_letters + string.digits

    random_token = ''.join(secrets.choice(characters) for _ in range(length))

    return random_token


def generate_random_digits(length):
    return ''.join(random.choices(string.digits, k=length))

def generate_username(email):
    random_digits = generate_random_digits(6)
    return f"{email}_{random_digits}"


def check_email_confirmation_code_in_cache(email):
    cache_key = f'email_confirmation_code:{email}'
    reset_data = cache.get(cache_key)
    if reset_data:
        code = reset_data.get('code')
        created_at = reset_data.get('created_at')
        return code, created_at
    return None, None

def store_email_confirmation_code_in_cache(email, code):
    cache_key = f'email_confirmation_code:{email}'
    cache.set(cache_key, {'code': code, 'created_at': timezone.now()}, timeout=300)


def check_email_confirmation_times_in_cache(email):
    cache_key_times = f'email_confirmation_code_times:{email}'
    cache_key_reset = f'email_confirmation_code:{email}'

    email_confirmation_times = cache.get(cache_key_times, 1)

    if email_confirmation_times < 2:
        cache.set(cache_key_times, email_confirmation_times + 1, timeout=300)
        remaining_time = None
    elif email_confirmation_times >= 2:
        reset_code_data = cache.get(cache_key_reset)
        if reset_code_data:
            created_at = reset_code_data.get('created_at')
            time_elapsed = timezone.now() - created_at
            remaining_time = max(0, 300 - time_elapsed.total_seconds())
        else:
            remaining_time = None

    return email_confirmation_times, remaining_time

def send_email_confirmation_code_email(email, code):
    subject = 'Код подтверждения почты'
    message = f'Ваш код подтверждения: {code}'
    from_email = DEFAULT_FROM_EMAIL 
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)