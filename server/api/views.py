from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import AnonymousUser

from .permissions import *
from .exсeptions import *
from .serializers import *
from .models import *
from .utils import *
from .pollvoting import *

from admin_api.models import Settings

import os

import logging
logger = logging.getLogger('debug') 

from .generics import CRUDapi

class MyProfileAPI(CRUDapi):
    model = Profile
    serializer_class = ProfileSerializer
    mini_serializer_class = GetProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'user_id'
    lookup_url_kwarg = 'user_id'
    order_by = 'user_id'
     

    def get(self, request, *args, **kwargs):
        my_profile =  Profile.objects.filter(user_id=self.request.user.id).first()
        return Response(self.get_serializer(my_profile).data)

    def patch(self, request, *args, **kwargs):
        my_profile = get_object_or_404(Profile, user_id=self.request.user.id)
        serializer = ProfileSerializer(my_profile, data=self.request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            data = serializer_errors_wrapper(serializer.errors)
            return Response({'message':data}, status=status.HTTP_400_BAD_REQUEST)


class StudyGroupAPI(CRUDapi):
    model = StudyGroup
    serializer_class = StudyGroupSerializer
    permission_classes = [AllowAny]
    lookup_field = 'name'
    lookup_url_kwarg = 'study_group_name'
    order_by = 'id'


class MyPollAPI(CRUDapi):
    model = Poll
    serializer_class = PollSerializer
    base_serializer_class = BasePollSerializer
    mini_serializer_class = MiniPollSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'poll_id'
    lookup_url_kwarg = 'poll_id'
    order_by = '-created_date'

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    author_field = 'author'
    max_instances = Settings.objects.first().max_users_polls_quantity

    def get_queryset(self):
        if self.request.query_params.get(self.lookup_url_kwarg):
            if not int(self.request.GET.get('detailed', True)):
                return Poll.my_manager.get_one(Q(author=self.get_profile()))
            else:
                return Poll.my_manager.get_one_with_answers(Q(author=self.get_profile()))
            
        return Poll.my_manager.get_all(Q(author=self.get_profile()))
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        data = request.data.copy() 
        data['author'] = self.get_profile().user_id
        poll_type = get_data_or_400(data, 'poll_type')
        poll_type = get_object_or_404(PollType, name=poll_type)
        data['poll_type'] = poll_type.id

        return super().post(request, *args, **kwargs, data=data)
    
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        data = request.data

        request_type = get_parameter_or_400(request.GET, 'request_type')
        poll_id = get_parameter_or_400(request.GET, 'poll_id')
            
        if request_type == 'edit_allowed_groups':
            poll = self.get_object()
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
                Poll.objects.filter(poll_id=poll_id, author=self.get_profile())
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
                    Q(author=self.get_profile()) and Q(poll_id=poll_id))
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


class MyQuickPollVotingAuthFormsAPI(CRUDapi):
    model = PollAuthField
    serializer_class = PollAuthFieldSerializer
    base_serializer_class = BasePollAuthFieldSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'auth_field_id'
    demanded_url_kwargs = ['poll_id']
    order_by = 'id'

    http_method_names = ['get', 'post', 'patch', 'delete']

    author_field = 'poll.author'

    def get_queryset(self):
        poll_id = self.request.query_params.get('poll_id')
        return PollAuthField.objects.filter(poll_id=poll_id)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        poll_id = self.request.query_params.get('poll_id')
        data = self.request.data.copy()
        data['poll'] = poll_id
        return super().post(request, *args, **kwargs, data=data)


class MyPollSettingsAPI(CRUDapi):
    model = PollSettings
    serializer_class = PollSettingsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'poll_id'
    lookup_url_kwarg = 'poll_id'
    demanded_url_kwargs = ['poll_id']
    order_by = 'poll_id'

    queryset = PollSettings.objects.all()
    
    http_method_names = ['get', 'patch']

    author_field = 'poll.author'


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
            send_poll_stats(poll.poll_id, stats)
            # send_poll_user_votes(poll.poll_id, answers)

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


class MyPollQuestionAPI(CRUDapi):
    model = PollQuestion
    serializer_class = PollQuestionSerializer
    base_serializer_class = PollQuestionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'poll_question_id'
    demanded_url_kwargs = ['poll_id']
    order_by = 'order_id'
    
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    author_field = 'poll.author'
    max_instances = Settings.objects.first().max_questions_quantity

    def get_queryset(self):
        poll_id = get_parameter_or_400(self.request.query_params, 'poll_id') 
        return PollQuestion.objects.filter(poll_id=poll_id, poll__author=self.get_profile()).prefetch_related('answer_options')
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs, use_pagination=False)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
            
        data = request.data.copy()
        poll_id = get_parameter_or_400(request.GET, 'poll_id') 
        data['poll'] = poll_id
        return super().post(request, *args, **kwargs, data=data)
    
    @transaction.atomic
    def put(self, request, *args, **kwargs):
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

        return super().put(request, *args, **kwargs)


class MyPollQuestionOptionAPI(CRUDapi):
    model = AnswerOption
    serializer_class = PollQuestionOptionSerializer
    base_serializer_class = PollQuestionOptionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'question_option_id'
    demanded_url_kwargs = ['poll_id', 'poll_question_id']
    order_by = 'order_id'   
    
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    author_field = 'question.poll.author'
    max_instances = Settings.objects.first().max_question_options_quantity

    def get_queryset(self):
        poll_id = get_parameter_or_400(self.request.query_params, 'poll_id')
        poll_question_id = get_parameter_or_400(self.request.query_params, 'poll_question_id')
        return AnswerOption.objects.filter(question__poll__poll_id=poll_id, question__poll__author=self.get_profile(), 
                                           question=poll_question_id, )
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs, use_pagination=False)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):

        data = request.data.copy()
        poll_question_id = get_parameter_or_400(self.request.query_params, 'poll_question_id') 
        data['question'] = poll_question_id
        return super().post(request, *args, **kwargs, data=data)
    
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        data = request.data
        return super().patch(request, *args, **kwargs)
  

class MyPollAnswerGroupAPI(CRUDapi):
    model = PollAnswerGroup
    serializer_class = PollAnswerGroupSerializer
    base_serializer_class = PollAnswerGroupSerializer
    permission_classes = [IsAuthenticated]
    demanded_url_kwargs = ['poll_id']
    lookup_field = 'id'
    lookup_url_kwarg = 'poll_answer_group_id'
    order_by = '-created_date'

    author_field = 'poll.author'

    def get_queryset(self):
        poll_id = self.request.query_params.get('poll_id')
        return (
            self.model.objects
                .filter(poll_id=poll_id)
                .select_related('profile')
                .prefetch_related('answers')
        )
    

@api_view(['GET', 'POST', 'DELETE'])
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
            send_poll_user_votes(poll.poll_id, result)

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
                    'poll': poll.poll_id,
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
                    'poll': poll.poll_id,
                    'is_finished': False,
                    'is_latest': True,
                }
            else:
                auth_data = get_data_or_400(data, 'auth_data')
                quick_voting_form_data = {
                    'poll': poll.poll_id
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
                    'poll': poll.poll_id,
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
        send_poll_stats(poll.poll_id, stats)
        send_poll_user_votes(poll.poll_id, answers)

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
    def get(self, request, *args, **kwargs):
        self.queryset = Poll.my_manager.get_all_avaliable_to_me(user_profile=self.get_profile())
        return super().get(request, *args, **kwargs)



class PollRegistrationApi(CRUDapi):
    model = PollRegistration
    serializer_class = BasePollRegistrationSerializer
    mini_serializer_class = MiniPollRegistrationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'poll_registration_id'
    order_by = '-registration_time'
    
    def get(self, request, *args, **kwargs):
        self.validate_demanded_url_kwarg()
        
        poll_registration_id = request.GET.get('poll_registration_id', None)
        
        if poll_registration_id:
            poll_registration = (
                PollRegistration.objects
                    .filter(Q(user=self.get_profile()) & Q(id=poll_registration_id))
                    .select_related('user__user', 'user', 'user__group')
                    .first()
            )
            if not poll_registration:
                raise ObjectNotFoundException(model='PollRegistration')
            poll = Poll.my_manager.get_one(Q(poll_id=poll_registration.poll.poll_id)).first()
            poll_registration.poll = poll
            
            serializer = self.serializer_class(poll_registration, context={'profile': self.get_profile()})
            return Response(serializer.data)
        
        else:
            poll_registrations = (
                PollRegistration.objects
                    .filter(user=self.get_profile())
                    .select_related('user__user', 'user__group', 'poll')
                    .order_by(self.order_by)
            )

            context = self.get_profile_to_context()
            pagination_data = self.__get_paginated_response(request, poll_registrations, self.mini_serializer_class, context=context)
            return Response(pagination_data)



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
                'poll_type': poll.poll_type.name,
                'auth_field_answers_dict': auth_field_answers_dict
            }


            result = {}
            answers = MyPollUsersAnswersSerializer(answers, context=context, many=True).data
            result['results'] = {
                'poll_data': PollSerializer(poll).data,
                'answers': answers
            }

            send_poll_user_votes(poll.poll_id, answers)

            return Response(result)
        
    except APIException as api_exception:
        return Response({'message': f"{api_exception.detail}"}, api_exception.status_code)

    except Exception as ex:
        logger.error(f"Внутренняя ошибка сервера в my_poll_users_votes: {ex}")
        return Response({'message': f"Внутренняя ошибка сервера в my_poll_users_votes: {ex}"},
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MySupportRequestsAPI(CRUDapi):
    model = SupportRequest
    serializer_class = SupportRequestSerializer
    base_serializer_class = SupportRequestBaseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'ticket_id'
    order_by = '-created_date'


    model_type_model = SupportRequestType
    model_type_model_field = 'type'
    model_type_model_url_kwarg  = 'ticket_type'


    def get_queryset(self):
        return SupportRequest.objects.filter(author=self.get_profile()) 
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            if self.get_queryset().count() > Settings.objects.first().max_users_tickets_quantity:
                raise AccessDeniedException(detail='Вы превысили лимит по созданным обращениям в поддержку.')
            
        data = request.data.copy()
        data['author'] = self.get_profile()
        data['type'] = get_object_or_404(SupportRequestType, type=get_data_or_400(data, 'ticket_type')).id
        return super().post(request, *args, **kwargs, data=data)
