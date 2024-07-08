from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render

from .permissions import *
from .exсeptions import *
from .serializers import *
from .models import *
from .utils import *
from .pollvoting import *

from admin_api.models import Settings

from qpoll.settings import w3, contract

import os

import logging
logger = logging.getLogger('debug') 

from .generics import CRUDapi

class MyProfile(CRUDapi):
    model = Profile
    serializer_class = GetProfileSerializer
    mini_serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'user_id'
    lookup_url_kwarg = 'user_id'
    order_by = 'user_id'


@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def my_profile(request):
    try:
        current_user = request.user
        current_profile = Profile.objects.get(user=current_user)

        if request.method == 'GET':
            current_user_profile = Profile.objects.filter(user=current_user).select_related('role').first()

            if not current_user_profile:
                raise ObjectNotFoundException('Profile')


            profile_serializer = GetProfileSerializer(current_user_profile)

            return Response(profile_serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            current_user_profile = Profile.objects.filter(user=current_user).exists()
            request.data['user'] = current_user.id
            if current_user_profile:
                return Response("Профиль данного пользователя уже существует.", status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = ProfileSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    data = serializer_errors_wrapper(serializer.errors)
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)      

        elif request.method == 'PATCH':
            current_user_profile = Profile.objects.filter(user=current_user).first()
            if not current_profile:
                raise ObjectNotFoundException('Profile')
            
            serializer = ProfileSerializer(current_user_profile, data=request.data, partial=True)
    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)     

        elif request.method == 'DELETE':
            current_user_profile = Profile.objects.filter(user=current_user).first()
            if not current_profile:
                raise ObjectNotFoundException('Profile')
            
            current_user_profile.delete()
            return Response(f"Профиль успешно удален.", status=status.HTTP_204_NO_CONTENT)
      

    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)
    
    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_profile: {ex}")
        return Response(f"Внутренняя ошибка сервера в my_profile: {ex}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class StudyGroupAPI(CRUDapi):
    model = StudyGroup
    serializer_class = StudyGroupSerializer
    permission_classes = [AllowAny]
    lookup_field = 'name'
    lookup_url_kwarg = 'study_group_name'
    order_by = 'id'

    http_method_names = ['GET']


@api_view(['GET', 'POST', 'DELETE', 'PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def my_poll(request):
    try:
        current_user = request.user
        my_profile = get_object_or_404(Profile, user=current_user)
        # my_profile = get_object_or_404(Profile, user__id=1)
        
        if request.method == 'GET':
            poll_id = request.GET.get('poll_id', None)

            if poll_id:
                detailed = int(request.GET.get('detailed', True))
                if detailed:
                    filters = Q(author=my_profile, poll_id=poll_id)
                    poll = Poll.my_manager.get_one_with_answers(filters).first()
                    if not poll:
                        raise ObjectNotFoundException(model='Poll')
                
                    serializer = PollSerializer(poll, context={'profile': my_profile})
                else:
                    filters = Q(author=my_profile, poll_id=poll_id)
                    poll = Poll.my_manager.get_one_mini(filters).first()
                    if not poll:
                        raise ObjectNotFoundException(model='Poll')
                
                    serializer = MiniPollSerializer(poll, context={'profile': my_profile})

                return Response(serializer.data)
            
            else:
                poll_type = request.GET.get('poll_type', None)
                name = request.GET.get('name', None)
                is_anonymous = request.GET.get('is_anonymous', None)
                is_paused = request.GET.get('is_paused', False)
                is_closed = request.GET.get('is_closed', False)

                filters = Q(author=my_profile)
                if poll_type:
                    poll_type = PollType.objects.filter(name=poll_type).first()
                    if not poll_type:
                        raise ObjectNotFoundException(model='PollType')
                    filters &= Q(poll_type=poll_type)
                if name:
                    filters &= Q(name__icontains=name)
                if is_anonymous:
                    filters &= Q(is_anonymous=is_anonymous)

                filters &= Q(is_paused=is_paused)
                filters &= Q(is_closed=is_closed)

                polls = Poll.my_manager.get_all(filters)

                pagination_data = get_paginated_response(request, polls, MiniPollSerializer)
                return Response(pagination_data)

        elif request.method == 'POST':
            # вынести в настройки колво ограничений
            if not my_profile.user.is_staff:
                max_users_polls_quantity = Settings.objects.all().first().max_users_polls_quantity
                if my_profile.my_polls.count() > max_users_polls_quantity:
                    raise TooManyInstancesException(detail=f"Вы не можете создавать более {max_users_polls_quantity} опросов.")

            data = request.data.copy()
            poll_id = get_data_or_400(data, 'poll_id')
            data['poll_id'] = poll_id 
            
            poll_type = get_data_or_400(data, 'poll_type')
            poll_type = get_object_or_404(PollType, name=poll_type)
                       
            data['poll_type'] = poll_type.id
            data['author'] = my_profile


            serializer = BasePollSerializer(data=data)
            if serializer.is_valid():
                poll = serializer.save()
                if poll.poll_type.name == 'Анонимный':
                    if is_web3_connected(w3):
                        poll_data = {
                            'poll_id': poll.poll_id,
                            'poll_type': 'Анонимный',
                        }
                        createPoll(w3, contract, poll_data)
                    else:
                        raise MyCustomException(detail="is_web3_connected не подключился")
                elif poll.poll_type.name == 'Быстрый':
                    auth_fields = [
                        {'poll': poll.id, 'name': 'ФИО', 'is_main': True, 'is_required': True},
                        {'poll': poll.id, 'name': 'Группа', 'is_main': False, 'is_required': False},
                        {'poll': poll.id, 'name': 'Номер студенческого билета', 'is_main': False, 'is_required': False},
                    ]
                    auth_fields_serializer = PollAuthFieldSerializer(data=auth_fields, many=True)
                    if auth_fields_serializer.is_valid():
                        auth_fields_serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)     

        elif request.method == 'PATCH':
            data = request.data

            poll_id = get_parameter_or_400(request.GET, 'poll_id')  

            poll = Poll.objects.filter(poll_id=poll_id, author=my_profile).first()
            if not poll:
                raise ObjectNotFoundException(model='Poll')
    
            serializer = PollSerializer(instance=poll, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)         

        elif request.method == 'PUT':
            data = request.data

            request_type = get_parameter_or_400(request.GET, 'request_type')
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
                
            if request_type == 'edit_allowed_groups':
                poll = get_object_or_404(Poll, poll_id=poll_id, author=my_profile)
                action = get_data_or_400(data, 'action')

                if action in ['add_group', 'remove_group']:
                    study_group_name = get_data_or_400(data, 'study_group_name')
                    study_group = get_object_or_404(StudyGroup, name=study_group_name)
                    
                    if action == 'add_group':
                        poll.allowed_groups.add(study_group)

                    elif action == 'remove_group':
                        poll.allowed_groups.remove(study_group)
                
                elif action == 'remove_all_groups':
                    poll.allowed_groups.clear()

                allowed_groups = poll.allowed_groups.all()
                serializer = StudyGroupSerializer(allowed_groups, many=True) 

                return Response(serializer.data)

            elif request_type == 'change_questions_order':
                poll = (
                    Poll.objects.filter(poll_id=poll_id, author=my_profile)
                        # .prefetch_related('questions')
                        .first()    
                )
                if not poll:
                    raise ObjectNotFoundException(model='Poll')
                # poll_questions = poll.questions
                
                # В БУДУЩЕМ ВОЗМОЖНО НУЖНО БУДЕТ ПЕРЕБИРАТЬ ТОЛЬКО СВЯЗАННЫЕ ВОПРОСЫ А НЕ ДЕЛАТЬ ЗАПРОС К БД 

                new_questions = []
                questions_data = data['questions_data']
                question_ids = list(questions_data.keys())
                questions = PollQuestion.objects.filter(id__in=map(int, question_ids))
                for question_number, question in enumerate(questions.all(), start=1):
                    if not question:
                        raise ObjectNotFoundException(model='AnswerOption')

                    question.order_id = question_number
                    new_questions.append(question)

                PollQuestion.objects.bulk_update(new_questions, ['order_id'])

                serializer = PollQuestionSerializer(new_questions, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)
            
            elif request_type == 'clone_poll':
                new_poll_id = get_data_or_400(data, 'new_poll_id')

                poll = Poll.objects.filter(poll_id=new_poll_id).exists()
                if poll:
                    raise InvalidFieldException(detail='Данный poll_id уже занят.')
                
                poll_to_clone = Poll.objects.filter(poll_id=poll_id).prefetch_related(
                                Prefetch('questions', queryset=PollQuestion.objects.prefetch_related(
                                    'answer_options'
                                ).all())
                            ).first()
                if not poll_to_clone:
                    raise ObjectNotFoundException(model='Poll')

                cloned_poll = clone_poll(poll_to_clone, new_poll_id)
                cloned_poll = (
                        Poll.objects
                            .filter(poll_id=cloned_poll.poll_id)
                            .select_related('author', 'poll_type')
                            .prefetch_related(
                            Prefetch('questions', queryset=PollQuestion.objects.prefetch_related(
                                    'answer_options'
                            ).all()))
                            .first()
                    )
                
                serializer = PollSerializer(cloned_poll)
                return Response(serializer.data)

            elif request_type == 'delete_image':
                image_path = None
                poll = get_object_or_404(Poll, poll_id=poll_id)
                
                if poll.image:
                    image_path = poll.image.path
                poll.image = None
                poll.save()
                if os.path.exists(image_path):
                    os.remove(image_path)
                serializer = PollSerializer(poll)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif request_type == 'deploy_to_production':
                poll = (
                    Poll.objects.filter(
                        Q(author=my_profile) and Q(poll_id=poll_id))
                        .select_related('author', 'poll_type')
                        .prefetch_related(
                        Prefetch('questions', queryset=PollQuestion.objects.prefetch_related(
                                'answer_options'
                        ).all()))
                        .first()
                    )

                if not poll:
                    raise ObjectNotFoundException(model='Poll')
                
                try:
                    if is_poll_valid(poll):
                        poll.is_in_production = True
                        poll.save()

                        return Response({'message':f"Опрос успешно опубликован", 'severity': 'success'}, status=status.HTTP_200_OK)
                
                except PollValidationException as exception:
                    return Response(exception.detail, exception.status_code)

            else:
                return Response("Неверный тип запроса к PUT", status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            data = request.data

            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            
            poll = Poll.objects.filter(poll_id=poll_id, author=my_profile).first()
            if not poll:
                raise ObjectNotFoundException(model='Poll')
   
            poll.poll_setts.delete()
            poll.delete()

            current_user_profile = Profile.objects.filter(user=current_user).first()

            if not current_user_profile:
                raise ObjectNotFoundException('Profile')

            return Response({'message':f"Опрос успешно удален"}, status=status.HTTP_204_NO_CONTENT)
    
    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)
    
    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_poll: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в my_poll: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def my_quick_poll_voting_auth_forms(request):
    try:
        current_user = request.user
        my_profile = get_object_or_404(Profile, user=current_user)
        # my_profile = get_object_or_404(Profile, user__id=1)

        if request.method == 'GET':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')

            # poll = Poll.my_manager.get_one(Q(poll_id=poll_id) & Q(author=my_profile)).first()
            poll = (
                Poll.objects.filter(Q(poll_id=poll_id) & Q(author=my_profile))
                .prefetch_related('auth_fields')
                .first()
            )
            if not poll:
                raise ObjectNotFoundException(model='Poll')
            
            voting_form_id = request.GET.get('voting_form_id', None)
            if voting_form_id:
                voting_form = get_object_from_object_or_404(poll.auth_fields, id=voting_form_id)
                serializer = PollAuthFieldSerializer(voting_form)

                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                voting_forms = poll.auth_fields.all()
                serializer = PollAuthFieldSerializer(voting_forms, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            data = request.data.copy()
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll = (
                Poll.objects.filter(Q(poll_id=poll_id) & Q(author=my_profile))
                .prefetch_related('auth_fields')
                .first()
            )
            if not poll:
                raise ObjectNotFoundException(model='Poll')
            
            if poll.auth_fields.count() > 5:
                raise TooManyInstancesException(model='PollAuthField', limit=5)

            data['poll'] = poll.id
            serializer = PollAuthFieldSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)   

        elif request.method == 'PATCH':
            data = request.data.copy()
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll = (
                Poll.objects.filter(Q(poll_id=poll_id) & Q(author=my_profile))
                .prefetch_related('auth_fields')
                .first()
            )
            if not poll:
                raise ObjectNotFoundException(model='Poll')

            voting_form_id = get_parameter_or_400(request.GET, 'voting_form_id')
            voting_form = get_object_from_object_or_404(poll.auth_fields, id=voting_form_id)

            serializer = PollAuthFieldSerializer(instance=voting_form, data=data, partial=True)
            is_valid, data = is_serializer_valid(serializer)
            if is_valid:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll = (
                Poll.objects.filter(Q(poll_id=poll_id) & Q(author=my_profile))
                .prefetch_related('auth_fields')
                .first()
            )
            if not poll:
                raise ObjectNotFoundException(model='Poll')
            
            voting_form_id = get_parameter_or_400(request.GET, 'voting_form_id')
            voting_form = get_object_from_object_or_404(poll.auth_fields, id=voting_form_id)
            
            voting_form.delete()

            return Response({'message': 'Поле успешно удалено.'}, status=status.HTTP_204_NO_CONTENT)


    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)
    
    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_quick_poll_voting_auth_forms: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в my_quick_poll_voting_auth_forms: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def my_poll_settings(request):
    try:
        current_user = request.user
        my_profile = get_object_or_404(Profile, user=current_user)

        if request.method == 'GET':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')

            poll = Poll.objects.filter(
                    Q(poll_id=poll_id)
                ).select_related('poll_setts').first()
            if not poll:
                raise ObjectNotFoundException(model='Poll')
    
            poll_setts = poll.poll_setts
           
            serializer = PollSettingsSerializer(poll_setts)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            data = request.data

            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            
            poll = Poll.objects.filter(
                    Q(poll_id=poll_id)
                ).select_related('poll_setts').first()
            if not poll:
                raise ObjectNotFoundException(model='Poll')
    
            poll_setts = poll.poll_setts
            serializer = PollSettingsSerializer(instance=poll_setts, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)   

    
    except PollValidationException as exception:
        return Response(exception.detail, exception.status_code)
    
    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)
    
    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_poll_settings: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в my_poll_settings: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_poll_stats(request):
    try:
        current_user = request.user
        my_profile = get_object_or_404(Profile, user=current_user)
        # my_profile = get_object_or_404(Profile, user__id=1)

        if not my_profile:
            raise ObjectNotFoundException(model='Profile')

        if request.method == 'GET':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')

            poll = Poll.my_manager.get_one_with_answers(Q(poll_id=poll_id, author=my_profile)).first()
            if not poll:
                raise ObjectNotFoundException('Poll')
            
            stats = calculate_my_poll_stats(poll, PollStatsSerializer)
            send_poll_stats(poll.id, stats)
            # send_poll_user_votes(poll.id, answers)

            return Response(stats)


    except APIException as api_exception:
        return Response({'message': f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_poll_stats: {ex}")
        return Response({'message': f"Внутренняя ошибка сервера в my_poll_stats: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_quick_poll_poll_user_answers(request):
    try:
        current_user = request.user
        my_profile = get_object_or_404(Profile, user=current_user)
        # my_profile = get_object_or_404(Profile, user__id=1)

        if not my_profile:
            raise ObjectNotFoundException(model='Profile')

        poll_id = get_parameter_or_400(request.GET, 'poll_id')
        poll = Poll.my_manager.get_one_quick_with_answers(Q(author=my_profile, poll_id=poll_id)).first()
        
        if request.method == 'GET':
            poll_answer_group_id = request.GET.get('poll_answer_group_id', None)
            
            if poll_answer_group_id:
                answer = (
                    poll.user_answers.filter(Q(poll__poll_id=poll_id) & Q(id=poll_answer_group_id))
                    .first()
                )
                if not answer:
                    raise ObjectNotFoundException(detail="Данный пользователь еще не принимал участие в опросе")
        
                context = {'poll': poll}
                answer = QuickPollAnswerGroupSerializer(answer, context=context)
                pagination_data['results'] = {
                    'poll_data': PollSerializer(poll).data,
                    'answers': pagination_data['results']
                }
                return Response(answer.data)
            
            else:
                answers = (
                    poll.user_answers.all()
                    .order_by('-voting_date')
                )
                context = {'poll': poll}
                pagination_data = get_paginated_response(request, answers, QuickPollAnswerGroupSerializer, context=context)
                pagination_data['results'] = {
                    'poll_data': PollSerializer(poll).data,
                    'answers': pagination_data['results']
                }
                return Response(pagination_data)
        
    except APIException as api_exception:
        return Response({'message': f"{api_exception.detail}"}, api_exception.status_code)
    
    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_quick_poll_poll_user_answers: {ex}")
        return Response({'message': f"Внутренняя ошибка сервера в my_quick_poll_poll_user_answers: {ex}"},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'POST', 'DELETE', 'PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def my_poll_question(request):
    try:
        current_user = request.user

        if request.method == 'GET':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')

            poll_question_id = request.GET.get('poll_question_id', None)
            poll = (
                Poll.objects
                    .filter(Q(author__user=current_user) and Q(poll_id=poll_id))
                    .first()
            )

            if not poll:
                raise ObjectNotFoundException(model='Poll') 
            
            if poll_question_id:
                my_poll_question = (
                    poll.questions.filter(id=poll_question_id)
                        .prefetch_related('answer_options')
                        .first()
                )
                serializer = PollQuestionSerializer(my_poll_question)
            else:
                my_poll_questions = poll.questions.all().prefetch_related('answer_options')
                serializer = PollQuestionSerializer(my_poll_questions, many=True)

                
            return Response(serializer.data)

        elif request.method == 'POST':
            data = request.data.copy()

            poll_id = get_data_or_400(data, 'poll_id')

            poll = Poll.objects.filter(Q(author__user=current_user) and Q(poll_id=poll_id)).first()
            if not poll:
                raise ObjectNotFoundException(model='Poll')
            
            if poll.is_in_production:
                raise AccessDeniedException(detail="Данный опрос находится в продакшене, его нельзя изменять!")

            max_questions_quantity = Settings.objects.all().first().max_questions_quantity
            if poll.questions.count() > max_questions_quantity:
                raise TooManyInstancesException(model='PollQuestion', limit=max_questions_quantity)

            data['poll'] = poll.id
            last_question = poll.questions.order_by('order_id', 'id').last()
            if last_question:
                data['order_id'] = last_question.order_id + 1

            serializer = PollQuestionSerializer(data=data)
            if serializer.is_valid():
                poll_question = serializer.save()

                return Response(f"Вопрос {poll_question} успешно проинициализирован", status=status.HTTP_201_CREATED)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)  
            
        elif request.method == 'PATCH':
            data = request.data

            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll_question_id = get_parameter_or_400(request.GET, 'poll_question_id')

            poll = get_object_or_404(Poll, poll_id=poll_id)
            poll_question = get_object_from_object_or_404(poll.questions, id=poll_question_id)
            
            if poll.is_in_production:
                raise AccessDeniedException(detail="Данный опрос находится в продакшене, его нельзя изменять!")
            
            serializer = PollQuestionSerializer(instance=poll_question, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)  

        elif request.method == 'DELETE':
            data = request.data

            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll_question_id = get_parameter_or_400(request.GET, 'poll_question_id')
            
            poll = get_object_or_404(Poll, poll_id=poll_id)
            poll_question = get_object_from_object_or_404(poll.questions, id=poll_question_id)

            if poll.is_in_production:
                raise AccessDeniedException(detail="Данный опрос находится в продакшене, его нельзя изменять!")
            
            poll_question.delete()

            return Response({'message':"Вопрос опроса успешно удален"}, status=status.HTTP_204_NO_CONTENT)

        elif request.method == 'PUT':
            data = request.data

            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll = get_object_or_404(Poll, poll_id=poll_id)

            if poll.is_in_production:
                raise AccessDeniedException(detail="Данный опрос находится в продакшене, его нельзя изменять!")
            
            poll_question_id = get_parameter_or_400(request.GET, 'poll_question_id')
            poll_question = get_object_from_object_or_404(poll.questions, id=poll_question_id)           
            request_type = get_parameter_or_400(request.GET, 'request_type')

            
            if request_type == 'change_options_order':
                new_options = []

                options_data = get_data_or_400(data, 'options_data')
                options_ids = list(options_data.keys())
                options = AnswerOption.objects.filter(id__in=map(int, options_ids))
                for option_number, option in enumerate(options.all(), start=1):
                    if not option:
                        raise ObjectNotFoundException(model='AnswerOption')

                    option.order_id = option_number
                    new_options.append(option)

                AnswerOption.objects.bulk_update(new_options, ['order_id'])

                serializer = AnswerOptionSerializer(new_options, many=True)

                return Response(serializer.data, status=status.HTTP_200_OK)
            
            elif request_type == 'copy_question':
                if poll.questions.count() > 50:
                    raise TooManyInstancesException(model='PollQuestion', limit=50)
                         
                cloned_question = clone_question(poll_question)
                cloned_question =  (
                    PollQuestion.objects
                        .filter(id=cloned_question.id)
                        .prefetch_related('answer_options')
                        .first()
                )
                serializer = PollQuestionSerializer(cloned_question)
                return Response(serializer.data)

            elif request_type == 'delete_image':
                image_path = None
                if poll_question.image:
                    image_path = poll_question.image.path
                poll_question.image = None
                poll_question.save()
                if os.path.exists(image_path):
                    os.remove(image_path)
                serializer = PollQuestionSerializer(poll_question)
                return Response(serializer.data, status=status.HTTP_200_OK)


    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)
    
    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_poll_question: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в my_poll_question: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET', 'POST', 'DELETE', 'PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def my_poll_question_option(request):
    try:
        current_user = request.user

        if request.method == 'GET':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll_question_id = get_parameter_or_400(request.GET, 'poll_question_id')

            poll = (
                Poll.objects.filter(Q(author__user=current_user) and Q(poll_id=poll_id))
                    .prefetch_related(
                    Prefetch('questions', queryset=PollQuestion.objects.prefetch_related(
                        'answer_options'
                    ).all())
                ).first()
            )
            if not poll:
                raise ObjectNotFoundException(model='Poll')

            poll_question = get_object_from_object_or_404(poll.questions, id=poll_question_id)
            

            question_option_id = request.GET.get('question_option_id', None)
            if question_option_id:
                question_option = poll_question.answer_options.filter(id=poll_question_id).first()
                serializer = PollQuestionOptionSerializer(question_option)
            else:
                question_options = poll_question.answer_options.all().order_by('order_id', 'id')
                serializer = PollQuestionOptionSerializer(question_options, many=True)
 
            
            return Response(serializer.data)

        elif request.method == 'POST':
            data = request.data.copy()

            poll_id = get_data_or_400(data, 'poll_id')
            poll_question_id = get_data_or_400(data, 'poll_question_id')

            poll = (
                Poll.objects.filter(Q(author__user=current_user) and Q(poll_id=poll_id))
                    .prefetch_related(
                    Prefetch('questions', queryset=PollQuestion.objects.prefetch_related(
                        'answer_options'
                    ).all())
                ).first()
            )
            if not poll:
                raise ObjectNotFoundException(model='Poll')
            
            poll_question = get_object_from_object_or_404(poll.questions, id=poll_question_id)

            if poll.is_in_production:
                raise AccessDeniedException(detail="Данный опрос находится в продакшене, его нельзя изменять!")
            
            max_question_options_quantity = Settings.objects.all().first().max_question_options_quantity
            if poll_question.answer_options.count() > max_question_options_quantity:
                raise TooManyInstancesException(model='AnswerOption', limit=max_question_options_quantity)

            data['question'] = poll_question.id

            last_option = poll_question.answer_options.filter(is_free_response=False).order_by('order_id', 'id').last()
            if last_option:
                data['order_id'] = last_option.order_id + 1

            # если свободная форма ответа, то добавляем в самый конец списка опций
            data['is_free_response'] = data.get('is_free_response', False)  
            if data['is_free_response']:
                data['order_id'] = 16

            has_free_option = poll_question.answer_options.filter(is_free_response=True).exists()
            serializer = PollQuestionOptionSerializer(data=data, context={'has_free_option': has_free_option})
            if serializer.is_valid():
                answer_option = serializer.save()
                    
                return Response(f"Вариант ответа {answer_option} успешно проинициализирован", status=status.HTTP_201_CREATED)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)  
            
        elif request.method == 'PATCH':
            data = request.data.copy()

            poll_id = get_data_or_400(data, 'poll_id')
            poll_question_id = get_data_or_400(data, 'poll_question_id')
            question_option_id = get_data_or_400(data, 'question_option_id')
            
            poll = get_object_or_404(Poll, poll_id=poll_id)
            poll_question = get_object_from_object_or_404(poll.questions, id=poll_question_id)
            question_option = get_object_from_object_or_404(poll_question.answer_options, id=question_option_id)
            
            if poll.is_in_production:
                raise AccessDeniedException(detail="Данный опрос находится в продакшене, его нельзя изменять!")


            serializer = PollQuestionOptionSerializer(instance=question_option, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)  

        elif request.method == 'DELETE':
            
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll_question_id = get_parameter_or_400(request.GET, 'poll_question_id')
            question_option_id = get_parameter_or_400(request.GET, 'question_option_id')
            
            poll = get_object_or_404(Poll, poll_id=poll_id)
            
            poll_question = get_object_from_object_or_404(poll.questions, id=poll_question_id)
            
            question_option = poll_question.answer_options.filter(id=question_option_id).first()
            if not question_option:
                raise ObjectNotFoundException(model='AnswerOption')

            if poll.is_in_production:
                raise AccessDeniedException(detail="Данный опрос находится в продакшене, его нельзя изменять!")
            
            question_option.delete()

            return Response({'message':"Вариант ответа успешно удален"}, status=status.HTTP_204_NO_CONTENT)

        elif request.method == 'PUT':
            data = request.data

            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll_question_id = get_data_or_400(data, 'poll_question_id')
            
            poll = get_object_or_404(Poll, poll_id=poll_id)
            poll_question = get_object_from_object_or_404(poll.questions, id=poll_question_id)

            if poll.is_in_production:
                raise AccessDeniedException(detail="Данный опрос находится в продакшене, его нельзя изменять!")
            
            objects_to_update = []

            options_data = data['options_data']
            for order_number, option_data in enumerate(options_data, start=1):
                poll_option = AnswerOption.objects.filter(id=int(option_data['id'])).first()
                if not poll_option:
                    raise ObjectNotFoundException(model='AnswerOption')

                if poll_option.is_free_response:
                    poll_option.order_id = 16
                else:
                    poll_option.order_id = order_number

                objects_to_update.append(poll_option)

            # Выполняем один запрос к базе данных для обновления всех объектов
            AnswerOption.objects.bulk_update(objects_to_update, ['order_id'])

            return Response(status=status.HTTP_200_OK)
            

    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_poll_question_option: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в my_poll_question_option: {ex}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def poll_answer_group(request):
    try:
        current_user = request.user
        my_profile = get_object_or_404(Profile, user=current_user)

        if not my_profile:
            raise ObjectNotFoundException(model='Profile')

        if request.method == 'GET':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            
            my_answer = (
                PollAnswerGroup.objects
                    .filter(Q(profile=my_profile) & Q(poll__poll_id=poll_id))
                    .select_related('profile')
                    .prefetch_related('answers')
                    .first()
            )

            if not my_answer:
                raise ObjectNotFoundException(model='PollAnswerGroup')
 

            poll_answer_group = PollAnswerGroupSerializer(my_answer)
            return Response(poll_answer_group.data)
        
        if request.method == 'POST':
            data = request.data.copy()

            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            
            poll = (
                Poll.objects.filter(poll_id=poll_id)
                .select_related('author', 'poll_type', 'author__user')
                .select_related('poll_setts')
                .first()
            )
            
            if not poll:
                raise ObjectNotFoundException(model='Poll')

            opened_for_voting = poll.opened_for_voting
            if not opened_for_voting:
                start_time_left = poll.start_time_left
                end_time_left = poll.end_time_left
                if start_time_left:
                    raise AccessDeniedException(detail=f'Опрос еще не открылся для прохождения, до начала: {start_time_left}')
                elif not end_time_left:
                    raise AccessDeniedException(detail=f'Опрос уже закрылся для прохождения')


            start_time_left = poll.start_time_left
            if start_time_left:

                if not start_time_left == 0:
                    raise AccessDeniedException(detail='Голосование еще не началось.')


            my_answer = (
                PollAnswerGroup.objects
                    .filter(Q(profile=my_profile) & Q(poll__poll_id=poll_id))
                    .last()
            )
            if my_answer:
                if not poll.is_revote_allowed:
                    if not my_answer.answers.all():
                        raise ObjectAlreadyExistsException(detail='У Вас уже имеется незавершенное прохождение опроса')
                else:
                    PollAnswerGroup.objects.filter(
                        Q(poll=poll) & Q(profile=my_profile)      
                    ).delete()
                    PollParticipantsGroup.objects.filter(
                        Q(poll=poll) & Q(profile=my_profile)      
                    ).delete()
            
            

            data['profile'] = my_profile
            data['poll'] = poll.id
            serializer = PollAnswerGroupSerializer(data=data)
            poll_partic_group = PollParticipantsGroupSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                if poll_partic_group.is_valid():
                    poll_partic_group.save()
                else:
                    raise MyCustomException(detail=poll_partic_group.errors)


                poll_answer_group = (
                    PollAnswerGroup.objects.filter(Q(poll=poll) & Q(profile=my_profile))
                        .prefetch_related('answers')
                        .select_related('poll', 'profile')
                        .first()
                )
                poll_answer_group = PollAnswerGroupSerializer(poll_answer_group)
                return Response({'message':"Вы успешно начали голосование.", 'data':poll_answer_group.data},
                                                                                    status=status.HTTP_201_CREATED)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)  
            
        if request.method == 'DELETE':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            
            my_answer = (
                PollAnswerGroup.objects
                    .filter(Q(profile=my_profile) & Q(poll__poll_id=poll_id))
                    .select_related('profile')
                    .prefetch_related('answers')
                    .first()
            )

            if not my_answer:
                raise ObjectNotFoundException(model='PollAnswerGroup')
 

            my_answer.delete()
            return Response('Вы успешно отменили прохождение.')


    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в poll_answer_group: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в poll_answer_group: {ex}"},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR) 



@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
@permission_classes([AllowAny])
@transaction.atomic
def poll_voting(request):
    try:
        current_user = request.user
        if not isinstance(current_user, AnonymousUser):
            my_profile = get_object_or_404(Profile, user=current_user)
        else:
            my_profile = None

        if request.method == 'GET':
            poll_id = request.GET.get('poll_id', None)

            if poll_id:
                my_answer = PollAnswerGroup.objects.filter(
                    Q(profile=my_profile) & Q(poll__poll_id=poll_id)
                ).select_related('poll').prefetch_related('answers').first()

                poll = Poll.my_manager.get_one(Q(author=my_profile) & Q(poll_id=poll_id)).first()

                if not my_answer:
                    raise ObjectNotFoundException(model='PollAnswerGroup')
                
                my_answer.poll = poll

                serializer = PollVotingResultSerializer(my_answer)
                return Response(serializer.data)
            
            else:
                my_answers = PollAnswerGroup.objects.filter(profile=my_profile)
                serializer = PollVotingResultSerializer(my_answers, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            data = request.data.copy()

            poll_id = get_parameter_or_400(request.GET, 'poll_id')
            poll = Poll.my_manager.get_one_with_answers(Q(poll_id=poll_id, is_in_production=True)).first()
            if not poll:
                raise ObjectNotFoundException(model='Poll')

            answers = get_data_or_400(data, 'answers')

            if not poll.poll_type.name == 'Быстрый':
                check_if_user_is_allowed_to_vote(poll, my_profile)
                    
                # валидация и парсинг ответов
                raw_answers = None
                if poll.poll_type.name == 'Опрос':
                    answers, raw_answers = poll_voting_handler(answers, poll)
                elif poll.poll_type.name == 'Викторина':
                    answers = quizz_voting_handler(answers, poll)
                else:
                    raise MyCustomException(detail="Данного типа опроса не существует")

                unmake_last_answer_latest(poll, my_profile)
                poll_answer_group, answers, tx_hash = save_votes(answers, poll, my_profile, raw_answers)

            
                if tx_hash:
                    poll_answer_group.tx_hash = str(tx_hash)
                    poll_answer_group.save()

            else:
                poll_answer_group_id = get_parameter_or_400(request.GET, 'poll_answer_group_id')
                poll_answer_group = (
                    PollAnswerGroup.objects
                        .filter(id=poll_answer_group_id)
                        .prefetch_related('answers')
                        .first()
                )

                if not poll_answer_group:
                    raise ObjectNotFoundException(detail='Вы еще не начали прохождение.')
                  
                # quick_voting_form_id = get_parameter_or_400(request.GET, 'quick_voting_form_id')
                # quick_voting_form = get_object_or_404(QuickVotingForm, id=quick_voting_form_id)
                quick_voting_form = poll_answer_group.quick_voting_form
                answers, _ = poll_voting_handler(answers, poll, is_full=False)
                poll_answer_group, answers, tx_hash = save_votes(answers, poll, my_profile, None, 
                                                                 poll_answer_group=poll_answer_group,
                                                                 poll_participation_group=None,
                                                                 quick_voting_form=quick_voting_form )


            if not poll.poll_type.name == 'Быстрый':
                my_answer = PollAnswerGroup.objects.filter(
                        Q(profile=my_profile) & Q(poll__poll_id=poll_id)
                    ).select_related('profile').prefetch_related('answers').first()
            else:
                my_answer = PollAnswerGroup.objects.filter(
                        Q(id=poll_answer_group_id)
                    ).prefetch_related('answers').first()
                my_answer.is_finished = True
                my_answer.save()

                
            if not my_answer:
                raise ObjectNotFoundException(model='PollAnswerGroup')
            
            my_answer.poll = poll
            serializer = PollVotingResultSerializer(my_answer)

            stats = calculate_my_poll_stats(poll, PollStatsSerializer)
            answers = (
                    PollAnswerGroup.objects
                    .filter(poll=poll)
                    .prefetch_related(
                            models.Prefetch('answers', queryset=PollAnswer.objects.all().select_related('answer_option'))
                        )
                    .filter(is_finished=True, is_latest=True)
                    .order_by('-voting_date')
                )

            auth_field_answers = (
                poll.auth_field_answers
                .select_related('auth_field', 'quick_voting_form', 'quick_voting_form__poll_answer_group')
                .all()
            )

            auth_field_answers_dict = {}
            for answer in auth_field_answers:
                quick_voting_form_id = answer.quick_voting_form.id
                if quick_voting_form_id not in auth_field_answers_dict:
                    auth_field_answers_dict[quick_voting_form_id] = []
                auth_field_answers_dict[quick_voting_form_id].append(answer)

            context = {
                'poll': poll,
                'poll_type': 'Быстрый',
                'auth_field_answers_dict': auth_field_answers_dict
            }

            result = {}
            answers = MyPollUsersAnswersSerializer(answers, context=context, many=True).data
            result['results'] = {
                'poll_data': PollSerializer(poll).data,
                'answers': answers
            }
            
            send_poll_stats(poll.poll_id, stats)
            send_poll_user_votes(poll.id, result)

            return Response({'message':"Вы успешно проголосовали", 'data':serializer.data}, status=status.HTTP_200_OK)
    
        elif request.method == 'DELETE':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')
           
            poll = (
                Poll.objects
                    .filter(Q(author__user=current_user) and Q(poll_id=poll_id))
                    .prefetch_related('user_answers')
                ).first()

            if not poll:
                raise ObjectNotFoundException(model='Poll')

            if not poll.has_user_participated_in(my_profile):
                raise AccessDeniedException(detail="Вы еще не принимали участие в этом опросе.")

            if not poll.can_user_vote(my_profile):
                raise AccessDeniedException(detail="В данном опросе недоступно повторное голосование.")
            

            answers_to_delete = poll.user_answers.filter(profile=my_profile).first()

            # Удаляем все найденные ответы
            if answers_to_delete:
                answers_to_delete.delete()


            return Response({'message':f"Ваш голос в опросе успешно отменен"}, status=status.HTTP_204_NO_CONTENT)
    
    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в poll_voting: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в poll_voting: {ex}"},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)  



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@transaction.atomic
def poll_voting_started(request):
    try:
        current_user = request.user
        if not isinstance(current_user, AnonymousUser):
            my_profile = get_object_or_404(Profile, user=current_user)
        else:
            my_profile = None

        if request.method == 'GET':
            poll_id = request.GET.get('poll_id', None)
            
            if poll_id:
                poll = get_object_or_404(Poll, poll_id=poll_id)
                if not poll.poll_type.name == 'Быстрый':
                    latest_answer = PollAnswerGroup.objects.filter(
                        Q(poll__poll_id=poll_id) & Q(profile=my_profile) & Q(is_latest=True)     
                    ).prefetch_related('answers').first()
                else:
                    poll_answer_group_id = get_parameter_or_400(request.GET, 'poll_answer_group_id')
                    latest_answer = (
                        PollAnswerGroup.objects
                            .filter(id=poll_answer_group_id)
                            .prefetch_related('answers')
                            .first()
                    )

                if latest_answer:
                    if not latest_answer.is_finished:
                        if latest_answer.voting_time_left == 0:
                            serializer = PollAnswerGroupSerializer(latest_answer)
                            return Response({'message':'Время на ответ вышло.', 'data': serializer.data})
                        else:
                            serializer = PollAnswerGroupSerializer(latest_answer)
                            return Response({'message':'У вас уже есть незавершенное голосование.', 'data': serializer.data})
                    
                return Response({'message':'У вас нет активного голосования.', 'data': None})
                
                        
            else:
                my_answers = PollAnswerGroup.objects.filter(profile=my_profile)
                serializer = PollVotingResultSerializer(my_answers, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            data = request.data.copy()

            poll_id = get_parameter_or_400(request.GET, 'poll_id')
           
            poll = Poll.my_manager.get_one_with_answers(Q(poll_id=poll_id, is_in_production=True)).first()

            if not poll:
                raise ObjectNotFoundException(model='Poll')

            if not poll.poll_type.name == 'Быстрый':
                check_if_user_is_allowed_to_vote(poll, my_profile)
                
                latest_answer = PollAnswerGroup.objects.filter(
                    Q(poll=poll) & Q(profile=my_profile) & Q(is_latest=True)     
                ).first()
                if latest_answer:
                    if not latest_answer.is_finished:
                        if not latest_answer.voting_time_left == 0:
                            active_voting = PollAnswerGroupSerializer(latest_answer).data
                            return Response({'message':'У вас уже есть незавершенное голосование.', 'data': active_voting})
                        else:
                            active_voting = PollAnswerGroupSerializer(latest_answer).data
                            return Response({'message':'Время на ответ вышло.', 'data': active_voting})

                unmake_last_answer_latest(poll, my_profile)
                poll_participant_group_data = {
                    'profile': my_profile,
                    'poll': poll.id,
                    'is_latest': True,
                }
                serializer = PollParticipantsGroupSerializer(data=poll_participant_group_data)
                if serializer.is_valid():
                    poll_participant_group = serializer.save()
                else:
                    data = serializer_errors_wrapper(serializer.errors)
                    return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)      

                poll_answer_group_data = {
                    'profile': my_profile,
                    'poll': poll.id,
                    'is_finished': False,
                    'is_latest': True,
                }
            else:
                auth_data = get_data_or_400(data, 'auth_data')
                quick_voting_form_data = {
                    'poll': poll.id
                }
                quick_voting_form_id = None
                serializer = QuickVotingFormSerializer(data=quick_voting_form_data)
                if serializer.is_valid():
                    quick_voting_form = serializer.save()
                    quick_voting_form_id = quick_voting_form.id
                else:
                    data = serializer_errors_wrapper(serializer.errors)
                    return Response({'message': data}, status=status.HTTP_400_BAD_REQUEST)   
                new_auth_fields, student_id = validate_auth_data_2(auth_data, poll, quick_voting_form)
                created_auth_fields = PollAuthFieldAnswer.objects.bulk_create(new_auth_fields)

                poll_answer_group_data = {
                    'profile': None,
                    'quick_voting_form': quick_voting_form.id,
                    'poll': poll.id,
                    'is_finished': False,
                    'is_latest': True,
                }
            
            serializer = PollAnswerGroupSerializer(data=poll_answer_group_data)
            if serializer.is_valid():
                unmake_last_quick_answer_latest(student_id, quick_voting_form_id)  
                poll_answer_group = serializer.save()           
                return Response({'message':"Вы успешно начали голосование", 'data':serializer.data}, status=status.HTTP_200_OK)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST) 

    
    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в poll_voting_started: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в poll_voting_started: {ex}"},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    

@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic
def poll_voting_ended(request):
    try:
        data = request.data.copy()

        current_user = request.user
        if not isinstance(current_user, AnonymousUser):
            my_profile = get_object_or_404(Profile, user=current_user)
        else:
            my_profile = None

        poll_id = get_parameter_or_400(request.GET, 'poll_id')
        poll = Poll.my_manager.get_one_with_answers(Q(poll_id=poll_id, is_in_production=True)).first()
        if not poll:
            raise ObjectNotFoundException(model='Poll')

        if not poll.poll_type.name == 'Быстрый':
            poll_answer_group = PollAnswerGroup.objects.filter(poll=poll, profile=my_profile,
                                                            is_finished=False).first()
        else:
            poll_answer_group_id = get_parameter_or_400(request.GET, 'poll_answer_group_id')
            poll_answer_group = (
                PollAnswerGroup.objects
                    .filter(id=poll_answer_group_id)
                    .prefetch_related('answers')
                    .first()
            )

        if not poll_answer_group:
            raise ObjectNotFoundException(detail='Вы еще не начали прохождение.')
        else:
            poll_answer_group.is_finished = True
            poll_answer_group.voting_end_date = datetime.now()
            poll_answer_group.save()
            
        if not poll.poll_type.name == 'Быстрый':
            poll_participation_group = PollParticipantsGroup.objects.filter(poll=poll, profile=my_profile,
                                                                            is_latest=True).first()
            if not poll_participation_group:
                raise ObjectNotFoundException(detail='Вы еще не начали прохождение.')
        else:
            poll_participation_group=None
            
        answers = data.get('answers', [])
        if poll.poll_type.name == 'Быстрый':
            # quick_voting_form_id = get_parameter_or_400(request.GET, 'quick_voting_form_id')
            quick_voting_form = poll_answer_group.quick_voting_form
        else:
            quick_voting_form = None
        # валидация и парсинг ответов
        raw_answers = None
        if poll.poll_type.name == 'Опрос':
            answers, raw_answers = poll_voting_handler(answers, poll, is_full=False)
        if poll.poll_type.name == 'Быстрый':
            answers, raw_answers = poll_voting_handler(answers, poll, is_full=False)

        elif poll.poll_type.name == 'Викторина':
            answers = quizz_voting_handler(answers, poll, is_full=False)
        else:
            raise MyCustomException(detail="Данного типа опроса не существует")


        _, answers, _ = save_votes(answers, poll, my_profile, raw_answers,
                                                poll_answer_group=poll_answer_group,
                                                poll_participation_group=poll_participation_group,
                                                quick_voting_form=quick_voting_form)

        if not poll.poll_type.name == 'Быстрый':
            my_answer = PollAnswerGroup.objects.filter(
                    Q(profile=my_profile) & Q(poll__poll_id=poll_id)
                ).select_related('profile').prefetch_related('answers').first()
            if not my_answer:
                raise ObjectNotFoundException(model='PollAnswerGroup')
        else:
            poll_answer_group_id = get_parameter_or_400(request.GET, 'poll_answer_group_id')
            my_answer = PollAnswerGroup.objects.filter(
                    Q(id=poll_answer_group_id)
                ).prefetch_related('answers').first()
            if not my_answer:
                raise ObjectNotFoundException(model='PollAnswerGroup')

        my_answer.poll = poll
        serializer = PollVotingResultSerializer(my_answer)

        stats = calculate_my_poll_stats(poll, PollStatsSerializer)
        send_poll_stats(poll.id, stats)
        send_poll_user_votes(poll.id, answers)

        return Response({'message':"Вы успешно проголосовали", 'data':serializer.data}, status=status.HTTP_200_OK) 

    
    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в poll_voting_ended: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в poll_voting_ended: {ex}"},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PollAPI(CRUDapi):
    model = Poll
    serializer_class = PollSerializer
    mini_serializer_class = MiniPollSerializer
    permission_classes = [AllowAny]
    lookup_field = 'poll_id'
    lookup_url_kwarg = 'poll_id'
    order_by = '-created_date'
    filter_fields = ['poll_type', 'name', 'is_anonymous', 'is_paused', 'is_closed']

    model_type_model = PollType
    model_type_model_field = 'poll_type'
    model_type_model_url_kwarg  = 'poll_type'

    # http_method_names = ['GET']
    # сделать наследование всех PollAPI
    # добавь варьирование в зависимости от poll_id

    queryset = Poll.my_manager.get_all()


class PollForMeAPI(PollAPI):
    queryset = Poll.my_manager.get_all_avaliable_for_voting()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def polls_for_me(request):
    try:
        current_user = request.user
        my_profile = get_object_or_404(Profile, user=current_user)
        # my_profile = get_object_or_404(Profile, user__id=1)

        if request.method == 'GET':
            poll_type = request.GET.get('poll_type', None)
            name = request.GET.get('name', None)
            is_anonymous = request.GET.get('is_anonymous', None)

            filters = Q(is_in_production=True)
            if poll_type:
                poll_type = PollType.objects.filter(name=poll_type).first()
                if not poll_type:
                    raise ObjectNotFoundException(model='PollType')
                filters &= Q(poll_type=poll_type)
            if name:
                filters &= Q(name__icontains=name)
            if is_anonymous:
                filters &= Q(is_anonymous=is_anonymous)


            polls = Poll.my_manager.get_all_avaliable_to_me(filters, my_profile)
            

            context = get_profile_to_context(my_profile)
            pagination_data = get_paginated_response(request, polls, MiniPollSerializer, context=context)
            return Response(pagination_data)

            
    except APIException as api_exception:
            return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)
        
    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в poll_for_me: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в poll_for_me: {ex}"},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def poll_registration(request):
    try:
        current_user = request.user
        my_profile = get_object_or_404(Profile, user=current_user)
        # my_profile = get_object_or_404(Profile, user__id=1)
 
        if request.method == 'GET':
            poll_registration_id = request.GET.get('poll_registration_id', None)

            if poll_registration_id:
                poll_registration = (
                    PollRegistration.objects
                        .filter(Q(user=my_profile) & Q(id=poll_registration_id))
                        .select_related('user__user', 'user', 'user__group')
                        .first()
                )
                if not poll_registration:
                    raise ObjectNotFoundException(model='PollRegistration')
                poll = Poll.my_manager.get_one(Q(poll_id=poll_registration.poll.poll_id)).first()
                poll_registration.poll = poll
                
                serializer = BasePollRegistrationSerializer(poll_registration, context={'profile': my_profile})
                return Response(serializer.data)
            
            else:
                poll_registrations = (
                    PollRegistration.objects
                        .filter(user=my_profile)
                        .select_related('user__user', 'user__group', 'poll')
                        .order_by('-registration_time')
                )

                context = get_profile_to_context(my_profile)
                pagination_data = get_paginated_response(request, poll_registrations, MiniPollRegistrationSerializer, context=context)
                return Response(pagination_data)

        if request.method == 'POST':
            poll_id = get_parameter_or_400(request.GET, 'poll_id') 
            poll = get_object_or_404(Poll, poll_id=poll_id)

            opened_for_registration = poll.opened_for_registration
            if opened_for_registration:
                if not poll.is_user_in_allowed_groups() == False:
                    if not poll.is_user_registrated(my_profile):
                        poll.registrated_users.add(my_profile)
                    else:
                        raise AccessDeniedException(detail='Вы уже зарегестрированы на данный опрос.')
                else:
                    raise AccessDeniedException(detail="Вы не принадлежите группе, которым разрешено учавствовать в опросе.")
            elif opened_for_registration is False:
                raise AccessDeniedException(detail='Регистрация на опрос уже завершена.')
            else:
                raise AccessDeniedException(detail='Регистрация на опрос не требуется.')

                    
            return Response('Вы были успешно зарегестрированы на опрос.')
        
        if request.method == 'DELETE':
            poll_id = get_parameter_or_400(request.GET, 'poll_id') 

            poll = get_object_or_404(Poll, poll_id=poll_id)

            if poll.is_user_registrated(my_profile):
                poll.registrated_users.remove(my_profile)
            else:
                raise AccessDeniedException(detail='Вы еще не зарегестрировались на данный опрос.')
        
            return Response('Регистрация на опрос успешно отменена.')

    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)
        
    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в poll_registration: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в poll_registration: {ex}"},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def my_poll_users_votes(request):
    try:
        current_user = request.user
        my_profile = get_object_or_404(Profile, user=current_user)
        # my_profile = get_object_or_404(Profile, user__id=1)

        if not my_profile:
            raise ObjectNotFoundException(model='Profile')

        if request.method == 'GET':
            poll_id = get_parameter_or_400(request.GET, 'poll_id')

            poll = Poll.my_manager.get_one(Q(poll_id=poll_id, author=my_profile)).first()
            if not poll:
                raise ObjectNotFoundException('Poll')

            user_id = request.GET.get('user_id', None)

            if user_id:
                answers = (
                    poll.user_answers.filter(profile__user_id=user_id)
                    .prefetch_related(
                            models.Prefetch('answers', queryset=PollAnswer.objects.all().select_related('answer_option'))
                        )
                    .order_by('-voting_date')      
                )
            else:
                answers = (
                    poll.user_answers
                    .prefetch_related(
                            models.Prefetch('answers', queryset=PollAnswer.objects.all().select_related('answer_option'))
                        )
                    .filter(is_finished=True, is_latest=True)
                    .order_by('-voting_date')
                )

            auth_field_answers = (
                poll.auth_field_answers
                .select_related('auth_field', 'quick_voting_form', 'quick_voting_form__poll_answer_group')
                .all()
            )

            auth_field_answers_dict = {}
            for answer in auth_field_answers:
                quick_voting_form_id = answer.quick_voting_form.id
                if quick_voting_form_id not in auth_field_answers_dict:
                    auth_field_answers_dict[quick_voting_form_id] = []
                auth_field_answers_dict[quick_voting_form_id].append(answer)

            context = {
                'poll': poll,
                'poll_type': 'Быстрый',
                'auth_field_answers_dict': auth_field_answers_dict
            }

            # paginated_result = get_paginated_response(
            #     request, answers, MyPollUsersAnswersSerializer, context=context
            # )
            result = {}
            answers = MyPollUsersAnswersSerializer(answers, context=context, many=True).data
            result['results'] = {
                'poll_data': PollSerializer(poll).data,
                'answers': answers
            }

            send_poll_user_votes(poll.id, answers)

            return Response(result)
        
    except APIException as api_exception:
        return Response({'message': f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_poll_users_votes: {ex}")
        return Response({'message': f"Внутренняя ошибка сервера в my_poll_users_votes: {ex}"},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def my_support_requests(request):
    current_user = request.user
    my_profile = get_object_or_404(Profile, user=current_user)

    if not my_profile:
        raise ObjectNotFoundException(model='Profile')
    
    try:
        if request.method == 'GET':
            ticket_id = request.GET.get('ticket_id', None)

            if ticket_id:
                ticket = (
                    SupportRequest.objects
                        .filter(Q(id=ticket_id) & Q(author=my_profile))
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

                filters = Q(author=my_profile)
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

        elif request.method == 'POST':
            data = request.data.copy()

            ticket_type = get_data_or_400(data, 'ticket_type')
            
            ticket_type = SupportRequestType.objects.filter(type=ticket_type).first()
            if not ticket_type:
                raise ObjectNotFoundException(model='SupportRequestType')
            data['type'] = ticket_type.id
            data['author'] = my_profile.user_id
            
            ticket_exists = (
                    SupportRequest.objects
                        .filter(Q(author=my_profile))
                        .exists()
                    )
            if ticket_exists:
                raise AccessDeniedException(detail='У Вас есть еще не рассмотренное обращение, ожидайте ответа')
    
            serializer = SupportRequestBaseSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                data = serializer_errors_wrapper(serializer.errors)
                return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)     
      
        elif request.method == 'DELETE':
            ticket_id = get_parameter_or_400(request.GET, 'ticket_id')

            ticket = (
                SupportRequest.objects
                    .filter(Q(id=ticket_id) & Q(author=my_profile))
                ).first()

            if not ticket:
                raise ObjectNotFoundException(model='SupportRequest')

            ticket.delete()

            return Response({'message':f"{ticket} успешно отменена"}, status=status.HTTP_204_NO_CONTENT)
    
    except APIException as api_exception:
        return Response({'message':f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_support_requests: {ex}")
        return Response({'message':f"Внутренняя ошибка сервера в my_support_requests: {ex}"},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)  


@api_view(['GET'])
def index(request):

    return Response(200)

def room(request, room_name):
    return render(request, "api/room.html", {"room_name": room_name})

