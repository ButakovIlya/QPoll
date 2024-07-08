import imghdr

def check_file(file):
    file_type = imghdr.what(file)
    if not file_type:
        return False, "Неподдерживаемый формат файла."
    
    # Проверяем, является ли файл изображением
    if file_type not in ['jpeg', 'png', 'gif', 'bmp', 'pdf']:
        return False, "Неподдерживаемый формат файла."

    # Проверяем размер файла
    if file.size > 100 * 1024 * 1024: 
        return False, "Первышен допустимый размер файла."

    return True, "ОК"

from copy import deepcopy


from django.db import transaction
from .models import Poll, PollQuestion, AnswerOption


def clone_poll(poll, new_poll_id):
    with transaction.atomic():

        cloned_poll = deepcopy(poll)
        cloned_poll.id = None
        cloned_poll.image = None
        cloned_poll.poll_id = new_poll_id
        cloned_poll.is_in_production = False
        if cloned_poll.name:
            cloned_poll.name = cloned_poll.name + " (копия)"

        cloned_poll_setts = deepcopy(poll.poll_setts)
        cloned_poll_setts.id = None
        cloned_poll_setts.save()
        cloned_poll.poll_setts = cloned_poll_setts
        cloned_poll.save()
        
        new_questions = []
        for question in poll.questions.all():
            new_question = deepcopy(question)
            new_question.id = None
            new_question.image = None
            new_questions.append(new_question)

        # Bulk create новых вопросов
        cloned_poll.questions.add(*new_questions)
        new_questions = PollQuestion.objects.bulk_create(new_questions)
        
        
        cloned_poll = (
                    Poll.objects
                        .filter(poll_id=cloned_poll.poll_id)
                        .prefetch_related('questions')
                        .first()
                )   
        answer_options_to_create = []
        cloned_poll_questions = cloned_poll.questions.all()
        for i, question in enumerate(poll.questions.all(), 0):
            new_question = cloned_poll_questions[i]

            answer_options_to_add = []
            for answer_option in question.answer_options.all():
                new_answer_option = deepcopy(answer_option)
                new_answer_option.id = None
                new_answer_option.image = None
                answer_options_to_create.append(new_answer_option)
                answer_options_to_add.append(new_answer_option)

            new_question.answer_options.add(*answer_options_to_add)
            
        answer_options_to_create = AnswerOption.objects.bulk_create(answer_options_to_create)

                
    return cloned_poll



def clone_question(question):
    cloned_question = deepcopy(question)
    cloned_question.id = None
    if cloned_question.name:
        cloned_question.name = cloned_question.name + " (копия)"
    cloned_question.image = None
    cloned_question.save()
    

    new_answer_options = []
    for answer_option in question.answer_options.all():
        new_answer_option = deepcopy(answer_option)
        new_answer_option.id = None
        new_answer_option.image = None
        new_answer_options.append(new_answer_option)

    cloned_question.answer_options.add(*new_answer_options)
            
    new_answer_options = AnswerOption.objects.bulk_create(new_answer_options)
    return cloned_question


from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from qrcode import QRCode, constants
from qpoll.settings import SERVER_URL


# def generate_poll_qr(poll):
#     # Генерация QR-кода на основе poll_id
#         qr = QRCode(
#             version=1,
#             error_correction=constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#         if poll.poll_type.name in ['Опрос', 'Викторина', 'Анонимный']:
#             qr.add_data(SERVER_URL + 'conduct-poll/'+ str(poll.poll_id))
#         elif poll.poll_type.name in ['Быстрый']:
#             qr.add_data(SERVER_URL + 'quick-conduct-poll/'+ str(poll.poll_id))

#         qr.make(fit=True)
        
#         # Создание изображения QR-кода
#         qr_image = qr.make_image(fill_color="black", back_color="white")
        
#         # Сохранение изображения в памяти
#         qr_image_buffer = BytesIO()
#         qr_image.save(qr_image_buffer, format="PNG")
        
#         # Создание объекта InMemoryUploadedFile для изображения QR-кода
#         qr_image_file = InMemoryUploadedFile(
#             qr_image_buffer,
#             None,
#             f'qrcode_poll_{poll.poll_id}.png',
#             'image/png',
#             qr_image.tell,
#             None
#         )
        
#         # Сохранение изображения QR-кода в поле qrcode
#         poll.qrcode.save(f'qrcode_poll_{poll.poll_id}.png', qr_image_file)
        
#         return poll


from base64 import b64encode

def get_qrcode_img_bytes(qrcode_path):
    with open(qrcode_path, 'rb') as f:
        qr_image_bytes = f.read()
        
        qr_image_base64 = b64encode(qr_image_bytes).decode()
        return qr_image_base64


from rest_framework.pagination import PageNumberPagination

def get_paginated_response(request, objects, serializer, context=None):
    paginator = PageNumberPagination()
    paginator.page_size = int(request.GET.get('page_size', 10))
    page = int(request.GET.get('page', 1))
    objects = paginator.paginate_queryset(objects, request)
    paginator.page.number = page
    total_items = paginator.page.paginator.count
    total_pages = paginator.page.paginator.num_pages

    if not context:
        serializer = serializer(objects, many=True)
    else:
        serializer = serializer(objects, many=True, context=context)

    pagination_data = {
        'total_items': total_items,
        'total_pages': total_pages,
        'results': serializer.data 
    }
    return pagination_data


def is_web3_connected(w3):
    if w3.is_connected():
        w3.eth.contract()
        return True
    else:
        return False



def createPoll(w3, contract, poll_data):
    try:
        accounts = w3.eth.accounts

        poll_id = poll_data['poll_id']
        poll_type = poll_data['poll_type']

        contract.functions.createPoll(poll_id, poll_type).transact({
                'from': accounts[0],
                'gasPrice': "20000000000",
                'gas': "210000"
            })
        
        # polls = contract.functions.getAllPolls().call()
        # print("Available Polls:", polls)

        return True
    
    except Exception as ex:
        return False


def addQuestionToPoll(w3, contract, poll_data):
    try:
        accounts = w3.eth.accounts

        poll_id = poll_data['poll_id']
        question_id = int(poll_data['question_id'])

        contract.functions.addQuestionToPoll(poll_id, question_id).transact({
                'from': accounts[0],
                'gasPrice': "20000000000",
                'gas': "210000"
            })
        
        polls = contract.functions.getAllPolls().call()
        # print("Available Polls:", polls)

        return True
    
    except Exception as ex:
        return False
    

def addAnswerToQuestion(w3, contract, poll_data):
    try:
        accounts = w3.eth.accounts

        poll_id = poll_data['poll_id']
        question_id = int(poll_data['question_id'])
        option_id = int(poll_data['option_id'])


        contract.functions.addAnswerToQuestion(poll_id, question_id, option_id).transact({
                'from': accounts[0],
                'gasPrice': "20000000000",
                'gas': "210000"
            })
        
        # polls = contract.functions.getAllPolls().call()
        # print("Available Polls:", polls)

        return True
    
    except Exception as ex:
        return False
    

def PollVoting(w3, contract, poll_data):
    try:
        accounts = w3.eth.accounts

        poll_id = poll_data['poll_id']
        answers = poll_data['answers']

        tx_hash = contract.functions.vote(poll_id, answers).transact({
                'from': accounts[0],
                'gasPrice': "20000000000",
                'gas': "210000"
            })
        
        # receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        # tx_hash_str = tx_hash.hex()

        # polls = contract.functions.getAllPolls().call()

        return tx_hash
    
    except Exception as ex:
        return False



def serializer_errors_wrapper(errors):
    try:
        all_errors = errors.items()
        if isinstance(all_errors, list):
            data = []
            for error in list(all_errors):
                data.append({
                    'field': error[0],
                    'error': error[1][0],
                })
            return data
        else:
            all_errors =  list(all_errors)
            data = {
                'field': all_errors[0][0],
                'error': all_errors[0][1][0]
            }
            return data
        
    except Exception:
        return errors
    
from .exсeptions import MissingFieldException, MissingParameterException, ObjectNotFoundException, AccessDeniedException

def get_data_or_400(data, data_field_name):
    data_field = data.get(data_field_name, None)
    if not data_field:
        raise MissingFieldException(data_field_name)
    
    return data_field

def get_parameter_or_400(request_get, parameter_field_name):
    parameter_field = request_get.get(parameter_field_name, None)
    if not parameter_field:
        raise MissingParameterException(parameter_field_name)
    
    return parameter_field


def get_object_or_404(model, **kwargs):
    object = model.objects.filter(**kwargs).first()
    if not object:
        raise ObjectNotFoundException(model.__name__)
    
    return object
    

def get_object_from_object_or_404(main_object, **kwargs):
    object = main_object.filter(**kwargs).first()
    if not object:
        raise ObjectNotFoundException(detail=f"Связанный объект из объекта '{main_object}' не найден.")
    
    return object

def get_profile_to_context(my_profile=None):
    if my_profile:
        context = {'profile': my_profile}
    else:
        context = None

    return context

def is_serializer_valid(serializer):
    if serializer.is_valid():
        serializer.save()
        return True, serializer.data
    else:
        data = serializer_errors_wrapper(serializer.errors)
        return False, data

from django.db.models import Q
from .models import PollAnswerGroup, PollParticipantsGroup

def unmake_last_answer_latest(poll, my_profile):
    to_ummake_latest = PollAnswerGroup.objects.filter(
                        Q(poll=poll) & Q(profile=my_profile) & Q(is_latest=True)
                    ).first()
    if to_ummake_latest:
        to_ummake_latest.is_latest = False
        to_ummake_latest.save()
    to_ummake_latest = PollParticipantsGroup.objects.filter(
        Q(poll=poll) & Q(profile=my_profile) & Q(is_latest=True) 
    ).first()
    if to_ummake_latest:
        to_ummake_latest.is_latest = False
        to_ummake_latest.save()

def has_user_participated_in_poll_too_many_times(poll, my_profile):
    poll_max_revotes_quantity = poll.poll_setts.max_revotes_quantity
    if not poll_max_revotes_quantity == 0:
        return poll.user_participations.filter(profile=my_profile).count() >= poll_max_revotes_quantity
    elif poll_max_revotes_quantity == None:
        return False
    else:
        return True


        
        
def check_if_user_is_allowed_to_vote(poll, user_profile):
    if not poll.opened_for_voting:
        raise AccessDeniedException(detail='Голосование еще не началось или уже завершилось')

    if poll.is_registration_demanded and not poll.is_user_registrated(user_profile):
        raise AccessDeniedException(detail='Вы еще не зарегистрировались на опрос')

    allowed_groups = poll.allowed_groups.all()
    if allowed_groups:
        if not user_profile.group in allowed_groups:
            raise AccessDeniedException(detail='Вы не принадлежите группе, которая может проходить данный опрос.')

    if poll.has_user_participated_in(user_profile):
        if not poll.is_revote_allowed:
            raise AccessDeniedException(detail="Вы уже принимали участие в этом опросе.")
        if has_user_participated_in_poll_too_many_times(poll, user_profile):
            raise AccessDeniedException(detail="Вы достигли предела максимального количества прохождений опроса.")
        
    return True


from .models import PollAuthFieldAnswer
from .exсeptions import MyCustomException

def validate_auth_data(auth_data, poll, quick_voting_form):
    new_auth_fields = []
    required_auth_fields = set(auth_field.id for auth_field in poll.auth_fields.all() if auth_field.is_required)

    for auth_field_data in auth_data:
        auth_field_data['poll'] = poll
        auth_field_data['quick_voting_form'] = quick_voting_form
        auth_field_id = auth_field_data.get('auth_field')
        auth_field_instance = next((auth_field for auth_field in poll.auth_fields.all() if auth_field.id == auth_field_id), None)
        
        auth_field_data['auth_field'] = auth_field_instance
        new_auth_field = PollAuthFieldAnswer(**auth_field_data)
        new_auth_fields.append(new_auth_field)

    new_auth_field_ids = set(auth_field.auth_field.id for auth_field in new_auth_fields if not auth_field.answer == None)
    if not required_auth_fields.issubset(new_auth_field_ids):
        difference = list(required_auth_fields.difference(new_auth_field_ids))
        raise MyCustomException(detail=f'Были переданы не все обяательные поля индентификации: {difference}')

    
    return new_auth_fields


def validate_auth_data_2(auth_data, poll, quick_voting_form):
    new_auth_fields = []
    student_id = None

    for auth_field_data in auth_data:
        auth_field_data['poll'] = poll
        auth_field_data['quick_voting_form'] = quick_voting_form
        auth_field_name = auth_field_data.get('auth_field_name')
        auth_field_instance = next((auth_field for auth_field in poll.auth_fields.all() if auth_field.name == auth_field_name), None)

        answer = auth_field_data.get('answer', None)
        
        if answer:
            if auth_field_name in ['Номер студенческого билета', 'Группа']:
                auth_field_data['answer'] = answer.upper()
            
            if auth_field_name == 'Номер студенческого билета':
                auth_field_data['answer'] = auth_field_data['answer'].replace(' ', '')
                student_id = auth_field_data.get('answer', None)

        auth_field_data['auth_field'] = auth_field_instance
        auth_field_data.pop('auth_field_name')
        new_auth_field = PollAuthFieldAnswer(**auth_field_data)
        new_auth_fields.append(new_auth_field)

    return new_auth_fields, student_id




from .models import PollAuthFieldAnswer, PollAnswerGroup

def unmake_last_quick_answer_latest(student_id, quick_voting_form_id):
    if student_id:
        poll_auth_field_answer = PollAuthFieldAnswer.objects.filter(Q(answer=student_id) & ~Q(quick_voting_form__id=quick_voting_form_id))
        if poll_auth_field_answer and hasattr(poll_auth_field_answer.latest('id'), 'quick_voting_form'):
            quick_voting_form = poll_auth_field_answer.latest('id').quick_voting_form
            pollanswergroup = quick_voting_form.poll_answer_group
            if pollanswergroup:
                pollanswergroup.is_latest = False
                pollanswergroup.save()
            else:
                pass
    

from django.db.models import Q, Prefetch, ExpressionWrapper, FloatField, Value, IntegerField
from django.db.models import Count, Case, When, F, Sum, Subquery, OuterRef, Max
from django.db.models.functions import Coalesce
from django.db import transaction

def calculate_my_poll_stats(poll, PollStatsSerializer):
    poll_members_quantity = poll.user_answers.count()

    poll_user_answers = (
        poll.all_answers
        .filter(poll_answer_group__poll=poll, poll_answer_group__is_latest=True, poll_answer_group__is_finished=True)
        .select_related('question', 'answer_option', 'poll_answer_group__profile')
    )
    # print(poll_user_answers)

    possible_question_points_count = (
        AnswerOption.objects
        .filter(question__poll=poll)
        .values('question_id')
        .annotate(
            correct_options_quantity=Sum(
                Case(
                    When(is_correct=True, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
    )

    question_statistics = (
        poll_user_answers
        .filter(poll_answer_group__poll=poll)
        .values('poll_answer_group__id', 'question_id')
        .annotate(
            quantity=Count('poll_answer_group__id', distinct=True),
            correct_answers_quantity = Count(Case(
                When(points=1, then=1),
                default=0
            )),
            incorrect_answers_quantity=Count(Case(
                When(points=0, then=1),
                default=None
            )),
            possible_question_points_count=Subquery(
                possible_question_points_count.filter(question_id=OuterRef('question_id'))
                                                        .values('correct_options_quantity')[:1]
            ),
            correct_percentage=ExpressionWrapper(
                100 * (F('correct_answers_quantity') - F('incorrect_answers_quantity')) 
                / F('possible_question_points_count'),
                output_field=FloatField()
            ),
        )
    ) 

    questions_percentage = (
        question_statistics
        .values('question_id')
        .annotate(
            answers_quantity=Count('poll_answer_group__id', distinct=True),
            answer_percentage=F('answers_quantity') / Value(poll_members_quantity) * 100,
            correct_percentage=ExpressionWrapper((F('correct_percentage') / F('answers_quantity')),
                output_field=FloatField()
            ),
        )
    )  
    # print(questions_percentage)

    poll_statistics = (
        questions_percentage
        .aggregate(
            total_questions=Count('question_id'),
            total_participants=Max('answers_quantity'),
            average_correct_percentage=Coalesce(
                Sum('correct_percentage') / Count('question_id'),
                Value(0),
                output_field=FloatField()
            ),
        )
    )
    # print(poll_statistics)

    options_answers_count = (
        poll_user_answers
        .filter(poll_answer_group__poll=poll)
        .values('answer_option')
        .annotate(
            quantity=Count('poll_answer_group__id', distinct=True),
        )
    )

    if poll.poll_type.name in ['Опрос', 'Викторина', 'Анонимный']:
        free_answers = (
            poll_user_answers
            .filter(
                poll_answer_group__poll__poll_id=poll.poll_id,
                text__isnull=False
            )
            .values(
                'text',
                'question_id',
                user_id=F('poll_answer_group__profile__user_id'),
                profile_name=F('poll_answer_group__profile__name'),
                profile_surname=F('poll_answer_group__profile__surname')
            )
        )
    elif poll.poll_type.name in ['Быстрый']:
        free_answers = (
            poll_user_answers
            .filter(
                poll_answer_group__poll__poll_id=poll.poll_id,
                text__isnull=False
            )
            .values(
                'text',
                'question_id',
                user_id=F('poll_answer_group__profile__user_id'),
                profile_name=F('poll_answer_group__profile__name'),
                profile_surname=F('poll_answer_group__profile__surname'),
                profile_patronymic=F('poll_answer_group__profile__patronymic'),
                is_auth_field_main=F('poll_answer_group__quick_voting_form__auth_field_answers__auth_field__is_main'),
                auth_field_name=F('poll_answer_group__quick_voting_form__auth_field_answers__auth_field__name'),
                auth_field_answer=F('poll_answer_group__quick_voting_form__auth_field_answers__answer'),
            )
            .filter(
                is_auth_field_main=True
            )
        )

    context = {
        'poll_statistics': poll_statistics,
        'question_statistics': question_statistics,
        'questions_percentage': questions_percentage,
        'options_answers_count': options_answers_count,
        'free_answers': free_answers
    }


    stats = PollStatsSerializer(poll, context=context)
    return stats.data


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_poll_stats(poll_id, stats):
    channel_layer = get_channel_layer()
    group_name = f"poll_{poll_id}".replace('-', '')

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_message",
            'content':'my_poll_stats',
            "message": {'data': stats}  
        }
    )

def send_poll_user_votes(poll_id, votes):
    channel_layer = get_channel_layer()
    group_name = f"poll_{poll_id}".replace('-', '')

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_message",
            'content':'my_poll_users_votes',
            "message": {'data': votes}  
        }
    )