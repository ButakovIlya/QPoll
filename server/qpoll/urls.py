from django.contrib import admin
from django.urls import path, include
from django_otp.admin import OTPAdminSite
# from django.contrib.auth.models import User
# from django_otp.plugins.otp_totp.models import TOTPDevice
# from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

from api.models import *
from .views import *

# class OTPAdmin(OTPAdminSite):
#     pass


# admin.site = OTPAdmin(name='OTPAdmin')
# admin.site.register(User)
# admin.site.register(TOTPDevice, TOTPDeviceAdmin)

# admin.site.register(UserRole)
# admin.site.register(Profile)
# admin.site.register(PollType)
# admin.site.register(Poll)
# admin.site.register(AnswerOption)
# admin.site.register(PollAnswer)
# admin.site.register(PollQuestion)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr_code_view/', qr_code_view),
    # path('answer_survey/', answer_survey),
    path('verify-totp/', VerifyTOTPView.as_view(), name='verify-totp'),
    path('api/', include('api.urls')),
    path('admin_api/', include('admin_api.urls')),
    path('login/', include('login.urls')),

]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # Другие URL-шаблоны вашего приложения
    ]


# Добавляем URL-шаблоны для медиа-файлов и статических файлов
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
