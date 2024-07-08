from django.core.cache import cache
from django.shortcuts import render
from rest_framework.response import Response
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from admin_api.models import Settings


class MaintenanceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        is_under_maintenance = cache.get('is_under_maintenance', None)

        if is_under_maintenance is None:
            settings = Settings.objects.first()
            is_under_maintenance = settings.is_under_maintenance if settings else False
            cache.set('is_under_maintenance', is_under_maintenance, 60 * 60 * 24)

        if is_under_maintenance:
            return render(request, 'maintenance.html', status=503)


class BannedUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_authenticator = JWTAuthentication()
        try:
            user, _ = jwt_authenticator.authenticate(request)
        except Exception as e:
            user = AnonymousUser()
        
        if not isinstance(user, AnonymousUser):
            is_user_banned = cache.get(f'is_{user.id}_banned', None)
            if is_user_banned is None:
                is_user_banned = user.profile.is_banned
                cache.set(f'is_{user.id}_banned', is_user_banned, 60 * 60 * 24)

            if is_user_banned:
                return render(request, 'banned_user.html', status=503)

