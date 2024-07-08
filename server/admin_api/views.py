from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.db.models import Q
from django.db import transaction
from django.core.cache import cache

from api.exсeptions import *
from api.serializers import PollSerializer, SupportRequestSerializer, StudyGroupSerializer
from api.models import Poll, UserRole, StudyGroup
from api.permissions import IsOwnerOrReadOnly
from api.utils import get_data_or_400, get_parameter_or_400, get_paginated_response, get_object_or_404

from .serializers import *
from .models import *

from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User, AnonymousUser

from login.serializers import *

@api_view(['GET', 'POST', 'DELETE', 'PATCH', 'PUT'])
@permission_classes([IsAdminUser])
@transaction.atomic
def users(request):
    try:
        if request.method == 'GET':
            user_id = request.GET.get('user_id', None)

            if user_id:
                user = Profile.objects.filter(user_id=user_id).select_related('role').first()
                if not user:
                    raise ObjectNotFoundException('Profile')
                serializer = ProfileSerializer(user)
            else:
                role = request.GET.get('role', None)
                is_banned = bool(request.GET.get('is_paused', None))
                name_surname_patronymic = request.GET.get('name_surname_patronymic', None)
                order_by = request.GET.get('order_by', None)


                filters = Q()
                if role:
                    filters &= Q(role__role=role)
                if is_banned:
                    filters &= Q(is_banned=is_banned)
                if name_surname_patronymic:
                    filters &= (
                        Q(name__icontains=name_surname_patronymic) or
                        Q(surname__icontains=name_surname_patronymic) or
                        Q(patronymic__icontains=name_surname_patronymic)
                    )
                if not order_by or not order_by in ['user_id', '-user_id', 'name', '-name', 'email', '-email',
                                                    'surname', '-surname', 'patronymic', '-patronymic',
                                                    'joining_date', '-joining_date', 'is_banned', '-is_banned',]:
                    order_by = '-joining_date'

                                    
                users = Profile.objects.filter(filters).order_by(order_by).select_related('role')
                pagination_data = get_paginated_response(request, users, ProfileSerializer)
                return Response(pagination_data)
    

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            user_id = get_parameter_or_400(request.GET, 'user_id')

            user = Profile.objects.filter(user_id=user_id).first()
            if not user:
                raise ObjectNotFoundException('Profile')
            
            serializer = ProfileSerializer(user, data=request.data, partial=True)
    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':   
            data = request.data

            request_type = get_parameter_or_400(request.GET, 'request_type')
            user_id = get_parameter_or_400(request.GET, 'user_id')
            
            user = Profile.objects.filter(user_id=user_id).first()
            if not user:
                raise ObjectNotFoundException(model='Profile')
            
            if request_type == 'change_role':
                role_name = get_data_or_400(data, 'role_name')
                
                role = UserRole.objects.filter(role=role_name).first()
                if not role:
                    raise ObjectNotFoundException(model='UserRole')
                
                user.role = role
                if role.role == 'Админ':
                    user.user.is_staff = 1
                else:
                    user.user.is_staff = 0

                user.save()

                serializer = ProfileSerializer(user)

                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                return Response("Неверный тип запроса к PUT", status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user_id = get_parameter_or_400(request.GET, 'user_id')

            user = User.objects.filter(user_id=user_id).first()
            if not user:
                raise ObjectNotFoundException('User')
            
            user_data = user
            user.delete()
            return Response(f"Пользователь {user_data} успешно удален.", status=status.HTTP_204_NO_CONTENT)
      

    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)
    
    except Exception as ex:
        return Response(f"Внутренняя ошибка сервера в admin users: {ex}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([IsAdminUser])
@transaction.atomic
def polls(request):
    try:
        if request.method == 'GET':
            poll_id = request.GET.get('poll_id', None)

            if poll_id:
                filters = Q(poll_id=poll_id)
                poll = Poll.my_manager.get_one(filters).first()
                if not poll:
                    raise ObjectNotFoundException('Poll')
                serializer = PollSerializer(poll)
            else:
                filters = Q()
                polls = Poll.my_manager.get_all(filters)
                polls = get_paginated_response(request, polls, PollSerializer)

                return Response(polls)
    

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')

            poll = Poll.objects.filter(poll_id=poll_id).first()
            if not poll:
                raise ObjectNotFoundException('Poll')
            
            serializer = ProfileSerializer(poll, data=request.data, partial=True)
    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':   
            data = request.data
            request_type = get_parameter_or_400(request.GET, 'request_type')
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
                
            poll = Poll.objects.filter(poll_id=poll_id).first()
            if not poll:
                raise ObjectNotFoundException(model='Poll')

            else:
                return Response("Неверный тип запроса к PUT", status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')

            poll = Poll.objects.filter(poll_id=poll_id).first()
            if not poll:
                raise ObjectNotFoundException('Poll')
            
            poll_data = poll
            poll.delete()
            return Response(f"{poll_data} успешно удален.", status=status.HTTP_204_NO_CONTENT)
      

    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)
    
    except Exception as ex:
        return Response(f"Внутренняя ошибка сервера в admin polls: {ex}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
# удаление опросов, юзеры, изменение роли, бан


@api_view(['GET', 'POST', 'PUT' 'DELETE'])
@permission_classes([IsAdminUser])
@transaction.atomic
def support_request(request):
    try:
        if request.method == 'GET':
            ticket_id = request.GET.get('ticket_id', None)

            if ticket_id:
                ticket = (
                    SupportRequest.objects
                        .filter(id=ticket_id)
                        .select_related('author', 'type')
                        .first()
                    )
                if not ticket:
                    raise ObjectNotFoundException(model='SupportRequest')
                
                serializer = SupportRequestSerializer(ticket)
                return Response(serializer.data)
            
            else:
                ticket_type = request.GET.get('ticket_type', None)
                name = request.GET.get('name', None)
                is_seen = request.GET.get('is_seen', None)
                is_closed = request.GET.get('is_closed', None)
                author_id = request.GET.get('author_id', None)

                filters = Q()
                if ticket_type:
                    ticket_type = SupportRequestType.objects.filter(type=ticket_type).first()
                    if not ticket_type:
                        raise ObjectNotFoundException(model='SupportRequestType')
                    filters &= Q(type=ticket_type)
                if name:
                    filters &= Q(name__icontains=name)
                if is_seen:
                    filters &= Q(is_seen=is_seen)
                if is_closed:
                    filters &= Q(is_closed=is_closed)
                if author_id:
                    filters &= Q(author__user_id=author_id)

                all_tickets = (
                    SupportRequest.objects
                        .filter(filters)
                        .select_related('author', 'type')
                        .order_by('-created_date')
                )
                all_tickets = get_paginated_response(request, all_tickets, SupportRequestSerializer)
                return Response(all_tickets)

        elif request.method == 'PATCH':
            data = request.data

            ticket_id = get_parameter_or_400(request.GET, 'ticket_id')

            ticket = SupportRequest.objects.filter(id=ticket_id).first()
            if not ticket:
                raise ObjectNotFoundException(model='SupportRequest')
    
            serializer = PollSerializer(instance=ticket, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
            
        elif request.method == 'DELETE':
            ticket_id = get_parameter_or_400(request.GET, 'ticket_id')

            ticket = (
                SupportRequest.objects
                    .filter(id=ticket_id)
                ).first()

            if not ticket:
                raise ObjectNotFoundException(model='SupportRequest')

            ticket.delete()

            return Response({'message':f"{ticket} успешно удален"}, status=status.HTTP_204_NO_CONTENT)
    
    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в adnmin_api support_request: {ex}"},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)  



@api_view(['GET', 'PATCH', 'PUT'])
@permission_classes([IsAdminUser])
@transaction.atomic
def project_settings(request):
    try:
        if request.method == 'GET':

            settings = Settings.objects.first()
            if not settings:
                raise ObjectNotFoundException(model='Settings')
                        
            
            serializer = ProjectSettingsSerializer(settings)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            data = request.data

            settings = Settings.objects.first()
            if not settings:
                raise ObjectNotFoundException(model='Settings')
    
            serializer = ProjectSettingsSerializer(instance=settings, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

        elif request.method == 'PUT':
            data = request.data

            settings = Settings.objects.first()
            if not settings:
                raise ObjectNotFoundException(model='Settings')
            
            is_under_maintenance = data.get('is_under_maintenance', None)
            if isinstance(is_under_maintenance, None):
                raise MissingFieldException('is_under_maintenance')\
                
            serializer = ProjectSettingsSerializer(instance=settings, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                cache.set('is_under_maintenance', is_under_maintenance, 60 * 60 * 24)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      
            
    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)
    
    except Exception as ex:
        return Response({'message':f"Внутренняя ошибка сервера в admin project_settings: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([IsAdminUser])
@transaction.atomic
def study_group(request):
    try:
        if request.method == 'GET':
            study_group_name = request.GET.get('study_group_name', None)

            if study_group_name:
                study_group = StudyGroup.objects.filter(name=study_group_name).first()
                if not study_group:
                    raise ObjectNotFoundException('StudyGroup')
                serializer = StudyGroupSerializer(study_group)
            else:
                study_groups = StudyGroup.objects.all().order_by('-id')
                study_groups = get_paginated_response(request, study_groups, StudyGroupSerializer)

                return Response(study_groups)
    

            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            data = request.data
            study_group_name = get_parameter_or_400(request.GET, 'study_group_name')

            study_group = StudyGroup.objects.filter(name=study_group_name).first()
            if not study_group:
                raise ObjectNotFoundException('StudyGroup')
            
            new_study_group_name = data.get('name', None)
            if new_study_group_name:
                if not new_study_group_name == study_group_name:
                    study_group = StudyGroup.objects.filter(name=study_group_name).exists()
                    if study_group:
                        raise ObjectAlreadyExistsException(detail='Группа с таким названием уже есть.')


            serializer = StudyGroupSerializer(study_group, data=data, partial=True)
    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'PUT':
            data = request.data
            study_group_name = get_parameter_or_400(request.GET, 'study_group_name')
                
            study_group = StudyGroup.objects.filter(name=study_group_name).first()
            if not study_group:
                raise ObjectNotFoundException(model='StudyGroup')

            else:
                return Response("Неверный тип запроса к PUT", status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            study_group_name = get_parameter_or_400(request.GET, 'study_group_name')

            study_group = StudyGroup.objects.filter(name=study_group_name).first()
            if not study_group:
                raise ObjectNotFoundException('StudyGroup')
            
            study_group_data = study_group
            study_group.delete()
            return Response(f"{study_group_data} успешно удалена.", status=status.HTTP_204_NO_CONTENT)
      

    except APIException as api_exception:
        return Response({'message':f"{api_exception}"}, api_exception.status_code)
    
    except Exception as ex:
        return Response(f"Внутренняя ошибка сервера в admin study_group: {ex}",
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 





# class SupportRequest(CRUDapi):
#     model = SupportRequest
#     serializer_class = SupportRequestSerializer
#     lookup_field = 'id'
#     lookup_url_kwarg = 'ticket_id'



