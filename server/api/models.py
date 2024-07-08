from django.db import models
from django.db.models import Q, BooleanField
from django.db.models import Case, When, Count, OuterRef
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

from .exсeptions import *

import logging
logger = logging.getLogger('debug') 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    email = models.EmailField('Почта', blank=True, null=True)
    name = models.CharField('Имя', max_length=50, blank=True, null=True)
    surname = models.CharField('Фамилия', max_length=50, blank=True, null=True)
    patronymic = models.CharField('Отчество', max_length=50, default='Не указано', null=True)
    sex = models.CharField('Пол', max_length=1, blank=True, null=True)
    number = models.CharField('Номер телефона', max_length=50, blank=True, null=True) 

    joining_date = models.DateField(auto_now_add=True)
    # has_2auf = models.BooleanField(default=False)

    role = models.ForeignKey('UserRole', on_delete=models.RESTRICT, related_name='profiles')
    group = models.ForeignKey('StudyGroup', on_delete=models.RESTRICT, related_name='students', null=True, default=None)
    
    
    is_banned = models.BooleanField('Заблокирован', default=False)
    is_email_confrimed = models.BooleanField('Почта подтверждена', default=False)


    def __str__(self):
        if self.name and self.surname:
            return self.name + ' ' + self.surname
        else: return f"Профиль {self.user.username}"
    

class StudyGroup(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True)

    def __str__(self):
        return f"Учебная группа '{self.name}'"
        
class UserRole(models.Model):
    role = models.CharField('Роль', max_length=50, unique=True)

    def __str__(self):
        return self.role
    

class PollType(models.Model):
    name = models.CharField('Название типа', max_length=50)
    description = models.CharField('Описание', max_length=500, default="", blank=True)

    is_text = models.BooleanField(default=True, null=True)    # текст ли как ответ
    is_free = models.BooleanField(default=False, null=True)    # свободная ли форма ответа
    is_image = models.BooleanField(default=False, null=True)    # фото ли как ответ
    has_multiple_choices = models.BooleanField(default=False) # множественный выбор
    has_correct_answer = models.BooleanField(default=False) # есть ли верные ответы или опрос
    is_anonymous = models.BooleanField(default=False) # анонимное

    def __str__(self):
        return self.name
    

class PollAnswer(models.Model):
    poll_answer_group = models.ForeignKey('PollAnswerGroup', related_name='answers', on_delete=models.CASCADE)
    poll = models.ForeignKey('Poll', related_name='all_answers', on_delete=models.CASCADE, db_index=True)
    question = models.ForeignKey('PollQuestion', on_delete=models.CASCADE)
    answer_option = models.ForeignKey('AnswerOption', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=None, null=True)
    text = models.CharField(max_length=100, default=None, null=True, blank=True)
    image = models.ImageField(verbose_name='Фото ответа', upload_to=f'images/poll_answers/', blank=True, null=True, default=None)

    points = models.PositiveSmallIntegerField(default=None, null=True)

    def __str__(self):
        return f"Ответ на {self.question}"
    

class PollAnswerGroup(models.Model):
    profile = models.ForeignKey(Profile, related_name='answer_groups', on_delete=models.CASCADE, null=True)
    quick_voting_form = models.OneToOneField('QuickVotingForm', related_name='poll_answer_group', on_delete=models.CASCADE, null=True)
    tx_hash = models.CharField(max_length=255, default=None, null=True)

    poll = models.ForeignKey('Poll', related_name='user_answers', on_delete=models.CASCADE)

    voting_date = models.DateTimeField(auto_now_add=True)
    voting_end_date = models.DateTimeField(default=None, null=True)
    is_finished = models.BooleanField(default=True)
    is_latest = models.BooleanField(default=True)

    @property
    def voting_time_left(self):
        completion_time = self.poll.poll_setts.completion_time

        poll_time_left = self.poll.end_time_seconds_left
        if poll_time_left:
            if completion_time:
                time_left = max(((self.voting_date + completion_time) - timezone.now()).total_seconds(), 0)
                return min(time_left, poll_time_left)
            else:
                return poll_time_left
        else:
            if completion_time:
                time_left = max(((self.voting_date + completion_time) - timezone.now()).total_seconds(), 0)
                return time_left

            
        return None            


    def __str__(self):
        return f"Группа ответов на {self.poll} от {self.profile}"


class PollParticipantsGroup(models.Model):
    profile = models.ForeignKey(Profile, related_name='participation_groups', on_delete=models.CASCADE, null=True)
    quick_voting_form = models.ForeignKey('QuickVotingForm', related_name='participation_groups', on_delete=models.CASCADE, null=True)
    poll = models.ForeignKey('Poll', related_name='user_participations', on_delete=models.CASCADE)
    is_latest = models.BooleanField(default=True)

    def __str__(self):
        return f"Группа ответов на {self.poll} от {self.profile}"
    
class AnswerOption(models.Model):
    name = models.CharField(max_length=100, default=None, null=True, blank=True)
    image = models.ImageField(verbose_name='Фото варианта ответа', upload_to=f'images/poll_options/', blank=True, null=True, default=None)
    question = models.ForeignKey('PollQuestion', related_name='answer_options', on_delete=models.CASCADE) # связь с вариантом вопросом

    is_correct = models.BooleanField(default=None, null=True)   # верный ли ответ
    is_text_response = models.BooleanField(default=False, null=True)    # текст ли как ответ
    is_free_response = models.BooleanField(default=False, null=True)    # свободная ли форма ответа
    is_image_response = models.BooleanField(default=False, null=True)    # фото ли как ответ

    order_id = models.PositiveIntegerField(default=1, null=False, blank=False) # порядковый номер в вопросе
    
    def __str__(self):
        if self.is_free_response:
            if not self.is_image_response:
                return f"Свободный вариант ответа '{self.name}'"
            else:
                return f"Свободный вариант ответа с фотографией"
        else:
            if self.name:
                return f"Вариант ответа '{self.name}'"
            else:
                return f"Вариант ответа №{self.id}"


    def delete(self):
        super().delete(keep_parents=False)


class PollQuestion(models.Model):
    name = models.CharField(max_length=250, default=None, null=True, blank=True)
    info = models.CharField(max_length=500, default=None, null=True, blank=True)
    image = models.ImageField(verbose_name='Фото вопроса', upload_to=f'images/poll_questions/', blank=True, null=True, default=None)
    poll = models.ForeignKey('Poll', related_name='questions', on_delete=models.CASCADE) # связь с опросом

    has_correct_answer = models.BooleanField(default=None, null=True)   # есть ли верный ответ
    has_multiple_choices = models.BooleanField(default=False)   # есть ли множенственный выбор
    is_free = models.BooleanField(default=False)   # свободная форма ответа, всего 1 вариант ответа
    is_text = models.BooleanField(default=True)   # текст как ответ
    is_image = models.BooleanField(default=False)   # фото как ответ

    order_id = models.PositiveIntegerField(default=1, null=False, blank=False) # порядковый номер в опросе

    is_required = models.BooleanField(default=True)    # обязателен ли ответ


    def __str__(self):
        if self.name:
            return f"Вопрос №{self.id} '{self.name}'"
        else:
            return f"Вопрос №{self.id}"

    def __repr__(self):
        if self.name:
            return f"Вопрос №{self.id} '{self.name}'"
        else:
            return f"Вопрос №{self.id}"


class MyPollManager(models.Manager):
    
    def __annotate_time(self, queryset):
        """Проверка на доступность опроса по времени"""
        now = timezone.now()
        
        return queryset.annotate(
            is_avaliable_for_voting=Case(
                When(
                    Q(poll_setts__start_time__isnull=False) & 
                    Q(poll_setts__end_time__isnull=False) & 
                    Q(poll_setts__start_time__lte=now) & 
                    Q(poll_setts__end_time__gte=now),
                    then=True,
                ),
                When(
                    Q(poll_setts__start_time__isnull=False) & 
                    Q(poll_setts__end_time__isnull=True) & 
                    Q(poll_setts__start_time__lte=now),
                    then=True,
                ),
                When(
                    Q(poll_setts__start_time__isnull=True) & 
                    Q(poll_setts__end_time__isnull=False) & 
                    Q(poll_setts__end_time__gte=now),
                    then=True,
                ),
                When(
                    Q(poll_setts__start_time__isnull=True) & 
                    Q(poll_setts__end_time__isnull=True),
                    then=True,
                ),
                default=False,
                output_field=BooleanField()
            )
        )
    
    def get_all(self, filters=Q()):
        """Получение всех опросов"""
        objects = (
            super().get_queryset()
            .select_related('author', 'author__user', 'author__group')
            .select_related('poll_type', 'poll_setts')
            .prefetch_related('allowed_groups')
            .prefetch_related('questions')
            .prefetch_related('user_participations')
            .prefetch_related(
                models.Prefetch('user_answers', queryset=PollAnswerGroup.objects.all()
                                                .select_related('profile')))
            .prefetch_related('registrated_users')
            .annotate(
                participants_quantity=Count('user_answers', filter=Q(user_answers__is_latest=True), distinct=True),
                questions_quantity=Count('questions', distinct=True)
            )
            .filter(filters)
            .order_by('-created_date')
        )

        return objects
    
    def get_all_with_answers(self, filters=Q()):
        """Получение всех опросов с ответами"""
        objects = (
            self.get_all(filters)
        )
        
        return objects
    
    def get_all_avaliable_for_voting(self, filters=Q()):
        """Получение всех опросов, доступных для прохождения"""
        filters &= Q(is_in_production=True)
        objects = self.get_all_with_answers(filters)
        objects = self.__annotate_time(objects)
        return objects.filter(Q(is_avaliable_for_voting=True), ~Q(poll_type__name__in=['Быстрый', 'Анонимный']))
    
    def get_all_avaliable_to_me(self, user_profile, filters=Q()):
        """Получение всех опросов доступных мне"""
        filters &= Q(is_in_production=True)
        objects = (
            self.get_all_avaliable_for_voting(filters)
            .annotate(
                check_if_user_registered=models.Case(
                    models.When(
                        is_registration_demanded=False,
                        then=True,
                    ),
                    models.When(
                        is_registration_demanded=True,
                        registrated_users=user_profile,
                        then=True,
                    ),
                    default=False,
                    output_field=models.BooleanField()
                ),
                check_if_user_in_allowed_groups=models.Case(
                    models.When(
                        allowed_groups__isnull=True,
                        then=True,
                    ),
                    models.When(
                        allowed_groups__isnull=False,
                        allowed_groups=user_profile.group,
                        then=True,
                    ),
                    default=False,
                    output_field=models.BooleanField()
                )
            )
            .filter(check_if_user_registered=True, check_if_user_in_allowed_groups=True)
            .order_by('-created_date')   
        )
        
        return objects

    def get_one(self, filters=Q()):
        """Получение опроса по `filters`"""
        object = (
            super().get_queryset()
            .select_related('author', 'author__user', 'author__group')
            .select_related('poll_type', 'poll_setts')
            .prefetch_related('allowed_groups')
            .prefetch_related('auth_fields')
            .prefetch_related(
                models.Prefetch('registrated_users', queryset=Profile.objects.select_related(
                        'group'
                ).all()))
            .prefetch_related(
                models.Prefetch('questions', queryset=PollQuestion.objects.prefetch_related(
                        'answer_options'
                ).all()))
            .annotate(
                participants_quantity=Count('user_participations', filter=Q(user_participations__is_latest=True), distinct=True),
                questions_quantity=Count('questions', distinct=True)
            )
            .filter(filters)    
        )
        
        return object

    def get_one_with_answers(self, filters=Q()):
        """Получение опроса по `filters` с ответами пользователей"""
        object = (
            self.get_one(filters)
            .prefetch_related(
                models.Prefetch('user_answers', queryset=PollAnswerGroup.objects.all()
                                                .select_related('profile', 'profile__user')
                                                .prefetch_related('answers')))
            .annotate(
                participants_quantity=Count('user_answers', filter=Q(user_answers__is_latest=True), distinct=True),
                questions_quantity=Count('questions', distinct=True)
            ) 
        )
        return object
    
    def get_one_quick_with_answers(self, filters=Q()):
        """Получение быстрого опроса по `filters` с формами ответа пользователей"""
        object = (
            self.get_one(filters)
            .prefetch_related(
                models.Prefetch('user_answers', queryset=PollAnswerGroup.objects.all()
                                                    .select_related('profile', 'profile__user', 'quick_voting_form')
                                                    .prefetch_related('answers')
                                                    .prefetch_related(
                                                        models.Prefetch('quick_voting_form__auth_field_answers',
                                                                        queryset=PollAuthFieldAnswer.objects.all()
                                                                        .select_related('auth_field')) 
                                                        )
                                                    )) 
            )
        return object
    
    def get_one_mini(self, filters=Q()):
        """Получение опроса по `filters` без вопросов и вариантов ответа"""
        objects = (
            super().get_queryset()
            .select_related('author', 'author__user', 'author__group')
            .select_related('poll_type', 'poll_setts')
            .prefetch_related('user_participations')
            .prefetch_related('allowed_groups')
            .prefetch_related('questions')
            .annotate(
                participants_quantity=Count('user_participations', filter=Q(user_participations__is_latest=True), distinct=True),
                questions_quantity=Count('questions', distinct=True)
            )
            .filter(filters)    
        )
        
        return objects        


class Poll(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll_id = models.CharField(max_length=100, unique=True, db_index=True) # уникальный id
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='my_polls') # автор опроса
    image = models.ImageField(verbose_name='Фото опроса', upload_to=f'images/poll_images/', blank=True, null=True) # фото 
    name = models.CharField(max_length=150, blank=True, null=True) # имя опроса
    description = models.TextField(blank=True, null=True) # текст начать опрос
    tags = models.TextField(blank=True, null=True) # тэги

    poll_type = models.ForeignKey(PollType, related_name='poll', on_delete=models.RESTRICT, null=True) # тип опроса
    poll_setts = models.OneToOneField('PollSettings', related_name='poll', on_delete=models.CASCADE, null=True) # настройки опроса

    allowed_groups = models.ManyToManyField(StudyGroup, related_name='allowed_polls', blank=True)
    registrated_users = models.ManyToManyField(Profile, related_name='registered_polls', through='PollRegistration', blank=True)

    created_date = models.DateTimeField(auto_now_add=True) # дата создания

    is_anonymous = models.BooleanField(default=False) # анонимное
    is_registration_demanded = models.BooleanField(default=False) # нужна ли регистрация

    is_revote_allowed = models.BooleanField(default=False) # разрешить повторное
    mix_questions = models.BooleanField(default=False) # перемешивать вопросы
    mix_options = models.BooleanField(default=False) # перемешивать варианты ответа
    hide_participants_quantity = models.BooleanField(default=False) # скрыть количество участников
    hide_options_percentage = models.BooleanField(default=False) # скрыть проценты ответов
    request_contact_info = models.BooleanField(default=False) # запрашивать контактные данные
    hide_options_percentage = models.BooleanField(default=False) # добавить теги

    is_paused = models.BooleanField(default=False) # приостановлено
    is_closed = models.BooleanField(default=False) # завершено
    accessible_via_link = models.BooleanField(default=False) # доступна только по ссылке

    is_in_production = models.BooleanField(default=False) # готов к прохождению

    # qr код ссылки на опрос
    qrcode = models.ImageField(verbose_name='Qrcode опроса', upload_to=f'images/poll_qrcodes/', blank=True, null=True) 

    objects = models.Manager()
    my_manager = MyPollManager()

    def __str__(self):
        if self.name:
            return f"Опрос '{self.name}'"
        else:
            return f"Опрос №{self.id}"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            

    def is_user_registrated(self, user_profile):
        if self.is_registration_demanded:
            if user_profile:
                return self.registrated_users.contains(user_profile)
            else:
                return None
        else:
            return None

    def has_user_participated_in(self, user_profile):
        if not user_profile:
            return None
        return self.user_participations.contains(user_profile)
    
    def is_user_in_allowed_groups(self, user_profile):
        allowed_groups = self.allowed_groups.all()
        if allowed_groups:
            if not user_profile:
                return False
            
            return user_profile.group in allowed_groups
        
        return None

    def has_user_started_voting(self, user_profile):
        active_voting = [answer for answer in self.user_answers.all() if answer.profile == user_profile] or None
        if active_voting and not active_voting == []:
            return not active_voting[-1].is_finished
        else:
            return False    
 
    @property
    def opened_for_voting(self):
        try:
            if self.poll_setts:
                start_time = self.poll_setts.start_time
                end_time = self.poll_setts.end_time

                if start_time and end_time:
                    return timezone.now() > start_time and timezone.now() < end_time 
                elif start_time and not end_time:    
                    return timezone.now() > start_time
                elif not start_time and end_time:
                    return timezone.now() < end_time
                else:
                    return True
            else:
                return True
        except Exception:
            return True

    @property
    def start_time_left(self):
        try:
            if self.poll_setts:
                start_time = self.poll_setts.start_time
                
                if start_time:
                    time_left = max((self.poll_setts.start_time - timezone.now()).total_seconds(), 0)
                    return format_time(time_left)

            return None
        except Exception:
            return None

    @property
    def end_time_left(self):
        try:
            if self.poll_setts:
                start_time = self.poll_setts.start_time
                duration = self.poll_setts.duration
                end_time = self.poll_setts.end_time

                if end_time:
                    time_left = max((end_time - timezone.now()).total_seconds(), 0)
                    return format_time(time_left)
                
                elif start_time and duration:
                    time_left = max((start_time + duration - timezone.now()).total_seconds(), 0)
                    return format_time(time_left)
                
                else: return None    
            else: return None
        except Exception:
            return None

    @property
    def end_time_seconds_left(self):
        try:
            if self.poll_setts:
                start_time = self.poll_setts.start_time
                # duration = self.poll_setts.duration
                end_time = self.poll_setts.end_time

                if end_time:
                    time_left = max((end_time - timezone.now()).total_seconds(), 0)
                    return time_left
                
                # elif start_time and duration:
                #     time_left = max((start_time + duration - timezone.now()).total_seconds(), 0)
                #     return time_left
                
                else: return None    
            else: return None
        except Exception:
            return None

    @property
    def start_end_seconds_left(self):
        try:
            if self.poll_setts:
                start_time = self.poll_setts.start_time

                if start_time:
                    time_left = max((start_time - timezone.now()).total_seconds(), 0)
                    return time_left
                else:
                    return None
            else:
                return None
        except Exception:
            return None

    @property
    def opened_for_registration(self):
        try:
            if self.is_registration_demanded:
                reg_start_time = self.poll_setts.registration_start_time
                reg_end_time = self.poll_setts.registration_end_time
                    
                start_time = self.poll_setts.start_time
                end_time = self.poll_setts.end_time

                if start_time or end_time:
                    if reg_start_time and reg_end_time:    
                        return reg_start_time < timezone.now() < reg_end_time
                    elif reg_start_time and not reg_end_time:
                        return reg_start_time < timezone.now() < start_time
                    elif reg_end_time and not reg_start_time:
                        return timezone.now() < reg_end_time
                    else:
                        return timezone.now() < start_time
                else:
                    return None
            else:
                return None
            
        except Exception:
            return None

    @property
    def registration_start_time_left(self):
        try:
            start_time = self.poll_setts.start_time
            reg_start_time = self.poll_setts.registration_start_time
            
            if self.is_registration_demanded:
                if reg_start_time:
                    time_left = max((reg_start_time - timezone.now()).total_seconds(), 0)
                    return format_time(time_left)
                else:
                    return None
            else:
                return None
        except Exception:
            return None

    @property
    def registration_end_time_left(self):
        try:
            start_time = self.poll_setts.start_time
            reg_end_time = self.poll_setts.registration_end_time
            
            if self.is_registration_demanded:
                if reg_end_time:
                    time_left = max((reg_end_time - timezone.now()).total_seconds(), 0)
                    return format_time(time_left)
                else:
                    time_left = max((start_time - timezone.now()).total_seconds(), 0)
                    return format_time(time_left)
            else:
                return None  
        except Exception:
            return None


class QuickVotingForm(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='quick_voting_forms')
    date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     if hasattr(self, 'poll_answer_group'):
    #         return f"Форма авторизции на {self.poll_answer_group}"
    #     else: return super().__str__()


class PollRegistration(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(auto_now_add=True)
    poll_passed = models.BooleanField(default=False)
    passing_date = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"Регистрация {self.user} на {self.poll} от {self.registration_time}"


class PollSettings(models.Model):

    max_revotes_quantity = models.PositiveSmallIntegerField(default=2)

    # настройки времени
    completion_time = models.DurationField(null=True) # время на прохождение
    duration = models.DurationField(null=True) # время с момента start_time в течение которого доступен опрос
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    registration_start_time = models.DateTimeField(null=True)
    registration_end_time = models.DateTimeField(null=True)


    # def __str__(self):
    #     if self.poll:
    #         return f"Настройки {self.poll}"


class PollAuthField(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='auth_fields')
    name = models.CharField(max_length=150, null=True, blank=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    example = models.CharField(max_length=150, null=True, blank=True)

    is_required = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Поле '{self.name}' для авторизции на {self.poll}"


class PollAuthFieldAnswer(models.Model):
    auth_field = models.ForeignKey(PollAuthField, on_delete=models.CASCADE, related_name='answers')
    quick_voting_form = models.ForeignKey(QuickVotingForm, on_delete=models.CASCADE, related_name='auth_field_answers')
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='auth_field_answers')
    answer = models.CharField(max_length=150)

    def __str__(self):
        return f"Ответ '{self.quick_voting_form}' на поле авторизации '{self.auth_field.name}' на {self.poll}"


class SupportRequestType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return f"Тип обращения {self.type}"


class SupportRequest(models.Model):
    text = models.CharField(max_length=1000)
    type = models.ForeignKey(SupportRequestType, related_name='tickets', on_delete=models.CASCADE) 
    author = models.ForeignKey(Profile, related_name='tickets', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    is_seen = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_closed_date = models.DateTimeField(default=None, null=True)

    
    def __str__(self):
        return f"Обращение типа {self.type.type} от {self.author} от {self.created_date}"


def format_time(seconds):
    if seconds is not None:
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
    
        # Форматируем строку
        time_string = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
        return time_string
    
    else: return None


