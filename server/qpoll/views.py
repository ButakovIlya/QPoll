import qrcode
import base64
import json
from io import BytesIO
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django_otp.oath import TOTP
from django_otp.util import random_hex

from django_otp.plugins.otp_totp.models import TOTPDevice

def generate_qr_code(user):
    # Генерация секретного ключа (вам возможно потребуется сохранить его для пользователя)
    secret_key = bytes.fromhex(random_hex(20))  # Преобразование в байты
    # Создание экземпляра TOTP
    totp_instance = TOTP(key=secret_key, step=30)
    # Получение TOTP URI
    uri = "otpauth://totp/{issuer}:{name}?secret={secret}&issuer={issuer}".format(
        issuer="example",  # Замените "example" на ваш домен или название вашего сервиса
        name=user.email,
        secret=secret_key.hex(),  # Преобразование байтов в шестнадцатеричную строку
    )

    # Создание QR-кода
    img = qrcode.make(uri)
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue(), secret_key


@api_view(['GET'])
def qr_code_view(request):
    qr_code_bytes, secret_key = generate_qr_code(request.user)
    qr_code_base64 = base64.b64encode(qr_code_bytes).decode('utf-8')
    return Response({'qr_code': qr_code_base64, 'secret_key': secret_key.hex()})  # Преобразование ключа обратно в строку для передачи в ответе


def verify_user_totp(token, user):
    # Предположим, у пользователя уже настроено TOTP устройство
    device = user.totpdevice_set.first()  # Получаем TOTP устройство пользователя
    print(device)
    if device is not None:
        # Проверка OTP, отправленного пользователем
        verified = device.verify_token(token)
        if verified:
            return True
    return False

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model()

class VerifyTOTPView(APIView):
    permission_classes = [IsAuthenticated]  # Требуется аутентификация

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        verified = verify_user_totp(token, user)
        
        if verified:
            return Response({'success': 'OTP verified successfully'})
        else:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

def create_totp_device(user, secret_key, name='default'):
    # Удалить существующие TOTP устройства для пользователя (опционально)
    TOTPDevice.objects.filter(user=user).delete()

    # Создать новое TOTP устройство для пользователя
    device = TOTPDevice.objects.create(
        user=user,
        name=name,
        key=secret_key,  # 16-40 символов в HEX
        step=30,         # Промежуток времени генерации токена (секунды)
        digits=6,        # Количество цифр в OTP
        tolerance=1,     # Допуск в количестве шагов
        drift=0,
        last_t=0,
    )
    return device

