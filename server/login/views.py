from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers

from .serializers import UserSerializer, PasswordChangeSerializer
from api.exсeptions import InvalidFieldException, MissingFieldException
from api.serializers import ProfileSerializer
from .serializers import *
from .utils import *
from api.models import *
from api.utils import serializer_errors_wrapper


@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def register(request):
    try:
        data = request.data.copy()
        email = data.get('email', None)
        if not email:
            raise MissingFieldException(field_name='email')
        
        number = data.get('number', None)
        if not number:
            raise MissingFieldException(field_name='number')
        
        password = data.get('password', None)
        if not password:
            raise MissingFieldException(field_name='password')
        
        check_email = User.objects.filter(email=email).exists()

        if not check_email:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    user = serializer.save()
                    data['user'] = user.id
                    data['email'] = email
                    data['role'] = 2

                    serializer = ProfileSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        error_messages = serializer_errors_wrapper(serializer.errors)
                        user.delete()
                        return Response({'message': error_messages}, status=status.HTTP_400_BAD_REQUEST)
                    

                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)
                    
                    return Response({'access_token': access_token, 'refresh_token': refresh_token, 'user_data': {'email': user.email, 'username': user.username}})
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message':'Данная почта уже занята'}, status=status.HTTP_400_BAD_REQUEST)
        

    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)

    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в register: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    data = request.data
    try:
        email = data.get('email', None)
        password = data.get('password', None)
        if not email:
            raise MissingFieldException(field_name='email')
        if not password:
            raise MissingFieldException(field_name='password')

        user = User.objects.filter(email=email).first()
        if not user:
            raise ObjectNotFoundException(model='User')
            
        if not user.check_password(password):
            raise WrongPasswordException()
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({'access_token': access_token, 'refresh_token': refresh_token, 'user_data': {'email': user.email, 'username': user.username}})
   
    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)

    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в login: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh_token', None)
        if not refresh_token:
            raise MissingFieldException(field_name='refresh_token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Вы были успешно разлогинены."})
            except TokenError:
                return Response({'message': 'Токен уже в черном списке или недействителен.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Вы были успешно разлогинены."})

    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)
    
    except Exception as ex:
        return Response({'message': f"Внутренняя ошибка сервера в logout: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def change_password(request):
    try:
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not user.check_password(old_password):
                return Response({'message': "Введен неверный пароль."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({'access_token': access_token, 'refresh_token': refresh_token, 'user_data': {'email': user.email, 'username': user.username}})
        else:
            error_messages = serializer_errors_wrapper(serializer.errors)
            return Response({'message': error_messages}, status=status.HTTP_400_BAD_REQUEST)
        
    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)

    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в change_password: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_reset_code(request):
    try:
        email = request.data.get('email', None)
        if not email:
            raise MissingFieldException(field_name='email')
            
        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            raise ObjectNotFoundException(model='User')


        # Проверяем, был ли уже отправлен код сброса пароля для данного пользователя
        if check_reset_code_in_cache(email):
            reset_code_times, remaining_time = check_reset_code_times_in_cache(email)
            if reset_code_times > 1:
                if remaining_time is not None:
                    remaining_seconds = int(remaining_time)
                    return Response({'message':f'Код сброса пароля уже отправлен. Повторная отправка будет доступна через {remaining_seconds} секунд.',
                                     'seconds_left': remaining_seconds})
                return Response({'message':'Код сброса пароля уже отправлен. Попробуйте позже.'})

        reset_code = generate_random_code()
        store_reset_code_in_cache(email, reset_code)
        send_reset_code_email(email, reset_code)
        return Response({'message':'Код сброса пароля отправлен на почту. Действителен в течение 5 минут.'})


        
    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)

    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в change_password: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def check_reset_code(request):
    try:
        email = request.data.get('email', None)
        if not email:
            raise MissingFieldException(field_name='email')

        reset_code = request.data.get('reset_code', None)
        if not reset_code:
            raise MissingFieldException(field_name='reset_code')
         
        if '-' in reset_code:
            reset_code = reset_code.replace('-', '')

        user_exists = User.objects.filter(email=email).exists()
        if not user_exists:
            raise ObjectNotFoundException(model='User')


        stored_code = check_reset_code_in_cache(email)[0]

        if stored_code and int(stored_code) == int(reset_code):
            reset_token_key = f'reset_token:{email}'
            reset_token = generate_random_token()
            cache.set(reset_token_key, reset_token, timeout=300)
            return Response({'message': 'Код верный, введите новый пароль.',
                                'reset_token': reset_token})
        else:
            return Response('Неверный код, повторите попытку позже.', status=status.HTTP_400_BAD_REQUEST)

        
    except APIException as api_exception:
            return Response({'message':f"{api_exception}"}, api_exception.status_code)

    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в check_reset_code: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    try:
        reset_token = request.data.get('reset_token')
        if not reset_token:
            raise MissingFieldException(field_name='reset_token')
        email = request.data.get('email')
        if not email:
            raise MissingFieldException(field_name='email')
        user = User.objects.filter(email=email).first()
        if not user:
            raise ObjectNotFoundException(model='User')
        
        new_password = request.data.get('new_password')
        if not new_password:
            raise MissingFieldException(field_name='new_password')

        if reset_token == get_reset_code_from_cache(email):
            password_serializer = PasswordCheckSerializer(data=request.data)
            if not password_serializer.is_valid():
                error_messages = serializer_errors_wrapper(password_serializer.errors)
                return Response({'message': error_messages}, status=status.HTTP_400_BAD_REQUEST)
            
            reset_password_after_code_validation(email, new_password)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            return Response({'access_token': access_token, 'refresh_token': refresh_token, 'user_data': {'email': user.email, 'username': user.username}})
                
        else: 
            return Response({'message': 'Неверный токен смены пароля.'}, status=status.HTTP_400_BAD_REQUEST)
        
    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)

    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в reset_password: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def send_email_confirmation_code(request):
    try:
        email = request.user.email
        if not email:
            raise ObjectNotFoundException(model='email')
        
        profile = Profile.objects.filter(user=request.user).first()
        if profile.is_email_confrimed:
            raise MyCustomException(detail='Вы уже подтвердили почту.')
          
        # Проверяем, был ли уже отправлен код подтверждения почты для данного пользователя
        if check_email_confirmation_code_in_cache(email):
            reset_code_times, remaining_time = check_email_confirmation_times_in_cache(email)
            if reset_code_times > 1:
                if remaining_time is not None:
                    remaining_seconds = int(remaining_time)
                    return Response({'message':f'Код подтверждения почты уже отправлен. Повторная отправка будет доступна через {remaining_seconds} секунд.',
                                     'seconds_left': remaining_seconds})
                return Response({'message':'Код подтверждения почты уже отправлен. Попробуйте позже.'})

        reset_code = generate_random_code()
        store_email_confirmation_code_in_cache(email, reset_code)
        send_email_confirmation_code_email(email, reset_code)
        return Response({'message':'Код подтверждения почты отправлен на почту. Действителен в течение 5 минут.'})

    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)

    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в send_email_confirmation_code: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_email(request):
    try:
        email = request.user.email
        if not email:
            raise ObjectNotFoundException(model='email')

        email_confirmation_code = request.data.get('email_confirmation_code', None)
        if not email_confirmation_code:
            raise MissingFieldException(field_name='email_confirmation_code')
         
        if '-' in email_confirmation_code:
            email_confirmation_code = email_confirmation_code.replace('-', '')

        stored_code = check_email_confirmation_code_in_cache(email)[0]

        if stored_code and int(stored_code) == int(email_confirmation_code):
            Profile.objects.filter(user=request.user).update(is_email_confrimed=True)
            return Response({'message': 'Ваша почта успешно подтверждена.'})
        else:
            return Response({'message': 'Неверный код, повторите попытку позже.'}, status=status.HTTP_400_BAD_REQUEST)

        
    except APIException as api_exception:
            return Response({'message':f"{api_exception}"}, api_exception.status_code)

    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в check_email_confirmation_code: {ex}"},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

class EmailTokenObtainPairSerializer(serializers.Serializer):
    default_error_messages = {
        'no_active_account': 'No active account found with the given email address.'
    }

    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        help_text='User\'s password'
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email, is_active=True)
            except User.DoesNotExist:
                raise serializers.ValidationError(self.error_messages['no_active_account'])

            if user.check_password(password):
                if not user.is_active:
                    raise serializers.ValidationError(self.error_messages['no_active_account'])
                refresh = RefreshToken.for_user(user)
                return {
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                }
            else:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
        
