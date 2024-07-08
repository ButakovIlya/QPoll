from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('send_reset_code/', send_reset_code, name='send_reset_code'),
    path('check_reset_code/', check_reset_code, name='check_reset_code'),
    path('reset_password/', reset_password, name='reset_password'),

    path('send_email_confirmation_code/', send_email_confirmation_code, name='send_email_confirmation_code'),
    path('confirm_email/', confirm_email, name='confirm_email'),

    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
