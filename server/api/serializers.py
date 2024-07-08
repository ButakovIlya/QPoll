from django.contrib.auth.models import User
from rest_framework import serializers
from functools import partial

from .validators import *
from .models import *
from .exсeptions import *

from login.validators import validate_number

class MiniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']
    

class StudyGroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[BaseValidator.name], required=False)

    class Meta:
        model = StudyGroup
        fields = '__all__'


class GetProfileSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer()
    group = StudyGroupSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_role(self, obj):
        return obj.role.role if obj.role else None


class ProfileSerializer(serializers.ModelSerializer):  

    name = serializers.CharField(validators=[ProfileValidator.name], required=False)
    surname = serializers.CharField(validators=[ProfileValidator.surname], required=False)
    patronymic = serializers.CharField(validators=[ProfileValidator.patronymic], required=False)
    number = serializers.CharField(required=True, validators=[validate_number])  
    email = serializers.CharField(validators=[ProfileValidator.email], required=True)
    sex = serializers.CharField(validators=[ProfileValidator.sex], required=False)
    joining_date = serializers.DateField(validators=[ProfileValidator.joining_date], required=False)

    class Meta:
        model = Profile
        fields = '__all__'




class MiniProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    group = StudyGroupSerializer()

    class Meta:
        model = Profile
        fields = ('name','surname', 'user', 'group')


class MiniPollAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollAnswer
        fields = '__all__'

    profile = MiniProfileSerializer()


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = '__all__' 
        # exclude = ['is_correct']



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollQuestion
        fields = '__all__'

    answer_options = AnswerOptionSerializer(many=True)


class PollTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollType
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class MyProfileSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Profile
        fields = '__all__'





# сериализаторы ответов
        
class PollAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollAnswer
        fields = '__all__'


class PollAnswerGroupSerializer(serializers.ModelSerializer):
    answers = PollAnswerSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = PollAnswerGroup
        fields = '__all__'
    
    voting_time_left = serializers.SerializerMethodField()
    voting_time_left_str = serializers.SerializerMethodField()

    def get_voting_time_left(self, instance):
        return instance.voting_time_left
        
    def get_voting_time_left_str(self, instance):
        return format_time(instance.voting_time_left)
    

    def get_author(self, instance):
        return MiniProfileSerializer(instance=instance.profile).data
    
        


class PollParticipantsGroupSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()


    def get_author(self, instance):
        return MiniProfileSerializer(instance=instance.profile).data
    
        
    class Meta:
        model = PollParticipantsGroup
        fields = '__all__'



class PollVotingResultSerializer(PollAnswerGroupSerializer):
    answers = PollAnswerSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()


    def get_author(self, instance):
        return MiniProfileSerializer(instance=instance.profile).data
    

    def to_representation(self, instance):
        my_answers = serializers.ModelSerializer.to_representation(self, instance)
                
        poll_points = 0
        poll_gained_points = 0

        data = {
                    'questions': PollQuestionSerializer(instance.poll.questions.all(), many=True).data,
                    'result': my_answers,
                    'poll_type': instance.poll.poll_type.name,
                }

        for question in data['questions']: # проходим по всем вопросам 
            question_correct_quantity = 0
            question_gained_quantity = 0
            if question.get('is_answered') is None: # проверка чтобы не занулять вопрос на который дан ответ
                question['is_answered'] = False # если ответ уже дан, то не делаем его False
                question['points'] = 0  # изначально начисляем 0 баллов за каждый
                question['options_quantity'] = 0  # изначально считаем колво верных вариантов ответа
            for answer_option in question['answer_options']: # проходим по всем вариантам ответа 
                if answer_option.get('is_correct') is not None: # проеряем, что у нас викторина
                    if answer_option.get('is_correct') == True:
                        question_correct_quantity += 1

                if answer_option.get('is_answered') is None: # проверка на то что на вариант ответа еще не ответили
                    answer_option['is_chosen'] = False # отмечаем, что вариант ответа изначально не выбран
                    answer_option['text'] = None # отмечаем, что текст для варианта ответа изначально не указан
                    answer_option['points'] = 0 # отмечаем, сколько баллов получили за ответ

                for answer in my_answers['answers']: # проходим по всем моим ответам
                    if answer['answer_option'] == answer_option['id']: # выбираем ответ по совпавшим id
                        question['is_answered'] = True # отмечаем, что вопрос отвечен
                        answer_option['is_chosen'] = True # отмечаем, что вариант ответа был выбран
                        answer_option['text'] = answer.get('text', None) # добавляем текст ответа, если он был дан
                        answer_option['points'] = answer['points'] # начисляем очки, которые получили после проверки правильности

                        if answer_option['points'] is not None: # проверяем что очки вообще есть
                            if answer_option['points'] > 0: # если выбрали верную опцию, то добавляем балл
                                question_gained_quantity += answer_option['points']
                            else:
                                answer_option['points'] = -1 # если выбрали неверную опцию, то убавляем балл
                                question_gained_quantity += answer_option['points']
            

            if question_correct_quantity:
                question['points'] += round(question_gained_quantity / question_correct_quantity, 2) # начисляем очки, которые получили после проверки правильности
                if question['points'] < 0:
                    question['points'] = 0
                poll_gained_points += question['points']
                poll_points += 1

                results = {
                        'total': poll_points,
                        'correct': poll_gained_points,
                        'wrong': poll_points - poll_gained_points,
                        'percentage': round(float(poll_gained_points / poll_points) * 100, 2),
                    }
                
                data['results'] = results

        return data
    

    
    class Meta:
        model = PollAnswerGroup
        fields = '__all__'


# сериализаторы опросов

class PollSettingsSerializer(serializers.ModelSerializer):
    completion_time = serializers.DurationField(validators=[BasePollSettingsValidator.completion_time], required=False, allow_null=True)
    start_time = serializers.DateTimeField(validators=[BasePollSettingsValidator.start_time], required=False, allow_null=True)
    end_time = serializers.DateTimeField(validators=[BasePollSettingsValidator.end_time], required=False, allow_null=True)
    duration = serializers.DurationField(validators=[BasePollSettingsValidator.duration], required=False, allow_null=True)

    max_revotes_quantity = serializers.IntegerField(validators=[partial(BasePollSettingsValidator.max_revotes_quantity, num=10)])

    # если установлена длительноть доступа к опросу, то обнулить end_time
    def set_duration(self, value):
        if value:
            if self.instance.end_time:
                self.instance.end_time = None

    def set_completion_time(self, value):
        if value:
            minutes, seconds = map(int, value.split(':'))
            if not (minutes == 0 and seconds == 0):
                duration_obj = timedelta(minutes=minutes, seconds=seconds)
                self.instance.completion_time = duration_obj
            else:
                self.instance.completion_time = None

    # если установлен end_time, то обнулить duration
    def set_start_time(self, value):
        if not value:
            if self.instance.duration:
                self.instance.duration = None

    # если установлен end_time, то обнулить duration
    def set_end_time(self, value):
        if value:
            if self.instance.duration:
                self.instance.duration = None

    def create(self, validated_data):
        for attr, value in self.initial_data.items():
            setter_name = f"set_{attr}"
            if hasattr(self, setter_name):
                getattr(self, setter_name)(value)

        return super().create(validated_data)  

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        for attr, value in self.initial_data.items():
            setter_name = f"set_{attr}"
            if hasattr(self, setter_name):
                getattr(self, setter_name)(value)
        return instance

    class Meta:
        model = PollSettings
        fields = '__all__'


class BasePollSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[BaseValidator.name], required=False, allow_blank=True)
    description = serializers.CharField(validators=[BaseValidator.description], required=False, allow_blank=True)
    tags = serializers.CharField(validators=[BaseValidator.description], required=False, allow_blank=True)
    duration = serializers.DurationField(validators=[PollValidator.duration], required=False)  
    
    is_in_production = serializers.BooleanField(validators=[PollValidator.is_in_production], required=False)    


    # participants_quantity = serializers.SerializerMethodField()
    # questions_quantity = serializers.SerializerMethodField()
    opened_for_voting = serializers.SerializerMethodField()
    opened_for_registration = serializers.SerializerMethodField()
    has_user_participated_in = serializers.SerializerMethodField()
    is_user_registrated = serializers.SerializerMethodField()
    has_user_started_voting = serializers.SerializerMethodField()

    start_time_left = serializers.SerializerMethodField()
    end_time_left = serializers.SerializerMethodField()
    registration_start_time_left = serializers.SerializerMethodField()
    registration_end_time_left = serializers.SerializerMethodField()

    has_poll_started = serializers.SerializerMethodField()
    has_poll_ended = serializers.SerializerMethodField()
    
    def get_has_poll_started(self, instance):
        start_end_seconds_left = instance.start_end_seconds_left
        if start_end_seconds_left is None:
            return None
        
        if start_end_seconds_left == 0:
            return True
        else:
            return False

    def get_has_poll_ended(self, instance):
        end_time_seconds_left = instance.end_time_seconds_left
        if end_time_seconds_left is None:
            return None
        
        if end_time_seconds_left == 0:
            return True
        else:
            return False
    
    def get_start_time_left(self, instance):
        return instance.start_time_left
    
    def get_end_time_left(self, instance):
        return instance.end_time_left
    
    def get_registration_start_time_left(self, instance):
        return instance.registration_start_time_left
    
    def get_registration_end_time_left(self, instance):
        return instance.registration_end_time_left
    
    def get_participants_quantity(self, instance):
        return instance.participants_quantity

    def get_questions_quantity(self, instance):
        return instance.questions_quantity

    def get_opened_for_voting(self, instance):   
        return instance.opened_for_voting

    def get_opened_for_registration(self, instance):   
        return instance.opened_for_registration
    
    def get_has_user_participated_in(self, instance):
        profile = self.context.get('profile')
        return instance.has_user_participated_in(profile)

    def get_has_user_started_voting(self, instance):
        profile = self.context.get('profile')
        return instance.has_user_started_voting(profile)
    
    def get_is_user_registrated(self, instance):
        profile = self.context.get('profile')
        return instance.is_user_registrated(profile)

    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data):
        poll = super().create(validated_data)
        poll_setts = PollSettings.objects.create()
        # poll = generate_poll_qr(poll)
        poll.poll_setts = poll_setts
        poll.save()

        return poll

class MiniPollSerializer(BasePollSerializer):
    poll_type = PollTypeSerializer(required=True)
    poll_setts = PollSettingsSerializer(required=False)
    author = MiniProfileSerializer()

    allowed_groups = StudyGroupSerializer(many=True, required=False)

    # qrcode_img = serializers.SerializerMethodField()

    is_user_in_allowed_groups = serializers.SerializerMethodField()
    
    def get_is_user_in_allowed_groups(self, instance):
        profile = self.context.get('profile')
        return instance.is_user_in_allowed_groups(user_profile=profile)
    
    # def get_qrcode_img(self, instance):
    #     qrcode_path = instance.qrcode
        
    #     if qrcode_path:
    #         return get_qrcode_img_bytes(qrcode_path.path)

    #     return None

    class Meta:
        model = Poll
        exclude = ['qrcode', 'registrated_users']



class BasePollRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class PollRegistrationSerializer(serializers.ModelSerializer):
    poll = MiniPollSerializer()
    user = MiniProfileSerializer()
    
    class Meta:
        model = PollRegistration
        fields = '__all__'

class MiniPollRegistrationSerializer(serializers.ModelSerializer):
    poll = serializers.SerializerMethodField()
    user = MiniProfileSerializer()
    
    def get_poll(self, instance):
        return str(instance)


    class Meta:
        model = PollRegistration
        fields = '__all__'



class BaseModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = super().create(validated_data)
        if not isinstance(self.initial_data, list):
            for attr, value in self.initial_data.items():
                setter_name = f"set_{attr}"
                if hasattr(self, setter_name):
                    getattr(self, setter_name)(value)
            return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        for attr, value in self.initial_data.items():
            setter_name = f"set_{attr}"
            if hasattr(self, setter_name):
                getattr(self, setter_name)(value)
        return instance
    

class BasePollAuthFieldSerializer(BaseModelSerializer):
    name = serializers.CharField(max_length=50, required=False, allow_null=True)
    description = serializers.CharField(max_length=150, required=False, allow_null=True)
    is_required = serializers.BooleanField(required=True)

    class Meta:
        model = PollAuthField
        fields = '__all__'

    def set_is_main(self, value):
        if value:
            auth_fields = self.instance.poll.auth_fields.all()
            for auth_field in auth_fields:
                if not auth_field.id == self.instance.id:
                    auth_field.is_main = False
                    auth_field.save()


class PollAuthFieldSerializer(BasePollAuthFieldSerializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    is_required = serializers.BooleanField(required=False)


class PollAuthFieldAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollAuthFieldAnswer
        fields = '__all__'


class MiniPollAuthFieldAnswerSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(source='auth_field.name')
    auth_field = PollAuthFieldSerializer()

    class Meta:
        model = PollAuthFieldAnswer
        fields = ['answer', 'auth_field']


class PollSerializer(BasePollSerializer):
    poll_type = PollTypeSerializer(required=True)
    author = MyProfileSerializer(required=True)
    poll_setts = PollSettingsSerializer(required=False)
    questions = QuestionSerializer(many=True, required=False)
    allowed_groups = StudyGroupSerializer(many=True, required=False)
    auth_fields = PollAuthFieldSerializer(many=True, required=False)
    registrated_users = MiniProfileSerializer(many=True, required=False)
   
    image = serializers.ImageField(validators=[BaseValidator.image], required=False)
    
    is_user_in_allowed_groups = serializers.SerializerMethodField()
    
    def get_is_user_in_allowed_groups(self, instance):
        profile = self.context.get('profile')
        return instance.is_user_in_allowed_groups(user_profile=profile)

    # def get_qrcode_img(self, instance):
    #     qrcode_path = instance.qrcode
        
    #     if qrcode_path:
    #         return get_qrcode_img_bytes(qrcode_path.path)

    #     return None

    def set_is_in_production(self, value):
        """Если убрали из продакшена, удаляем все ответы"""
        value = bool(int(value))
        if value == False:
            poll = self.instance
            answers = PollAnswerGroup.objects.filter(poll=poll).delete()
            participants = PollParticipantsGroup.objects.filter(poll=poll).delete()

    def set_is_registration_demanded(self, value):
        """Если убрали регистрацию, удаляем время регистрации"""
        value = bool(int(value))
        if value == False:
            poll_setts = self.instance.poll_setts
            poll_setts.registration_start_time = None
            poll_setts.registration_end_time = None
            poll_setts.save()

    def create(self, validated_data):
        instance = super().create(validated_data)
        for attr, value in self.initial_data.items():
            setter_name = f"set_{attr}"
            if hasattr(self, setter_name):
                getattr(self, setter_name)(value)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        for attr, value in self.initial_data.items():
            setter_name = f"set_{attr}"
            if hasattr(self, setter_name):
                getattr(self, setter_name)(value)
        return instance
    


# сериализаторы воросов

class PollQuestionSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionSerializer(many=True, required=False)
    name = serializers.CharField(validators=[BaseValidator.name], required=False, allow_blank=True)
    info = serializers.CharField(validators=[BaseValidator.info], required=False, allow_blank=True)

    image = serializers.ImageField(validators=[BaseValidator.image], required=False)

    class Meta:
        model = PollQuestion
        fields = '__all__'

    # обнуляем правильность ответов при изменении has_multiple_choices или is_free
    def set_has_multiple_choices(self, value):
        options_to_update = self.instance.answer_options.all()
        new_options = []
        for option in options_to_update:
            option.is_correct = False
            new_options.append(option)
        AnswerOption.objects.bulk_update(new_options, ['is_correct'])

        # if value:
        #     if not self.instance.is_free:
        #         option_to_delete = self.instance.answer_options.filter(is_free_response=True).first()
        #         if option_to_delete:
        #             option_to_delete.delete()

    # если вопрос с открытым вариантом ответа, то создаем вариант ответа с текстом и удаляем остальные
    def set_is_free(self, value):
        if value:
            self.instance.answer_options.all().delete()
            
            if not self.instance.answer_options.filter(is_free_response=True).exists():
                free_option = AnswerOption.objects.create(
                    question=self.instance,
                    is_free_response=True,
                    is_correct=True,
                )
        else:
            if self.instance.is_free:
                free_option = self.instance.answer_options.filter(is_free_response=True).first()
                if free_option:
                    free_option.delete()


    def create(self, validated_data):
        instance = super().create(validated_data)
        for attr, value in self.initial_data.items():
            setter_name = f"set_{attr}"
            if hasattr(self, setter_name):
                getattr(self, setter_name)(value)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        for attr, value in self.initial_data.items():
            setter_name = f"set_{attr}"
            if hasattr(self, setter_name):
                getattr(self, setter_name)(value)
        return instance



# сериализаторы вариантов ответа
        
class PollQuestionOptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[partial(BaseValidator.name, chars=100)], required=False, allow_blank=True)
    info = serializers.CharField(validators=[partial(BaseValidator.info, chars=500)], required=False, allow_blank=True)
    image = serializers.ImageField(validators=[BaseValidator.image], required=False)

    class Meta:
        model = AnswerOption
        fields = '__all__'


    def set_is_correct(self, value):
        question = self.instance.question
        if value:
            # если выбран верным вариант ответа, то делаем неверным свободный вариант ответа
            if not self.instance.is_free_response:
                free_option = question.answer_options.filter(is_free_response=True).first()
                if free_option and free_option.is_correct:
                    free_option.is_correct = False
                    free_option.save()

            # если вопрос с открытым вариантом ответа верный, то обнуляем все остальные варианты ответа
            if self.instance.is_free_response:
                options_to_update = self.instance.question.answer_options.all()
                new_options = []
                for option in options_to_update:
                    if not self.instance.id == option.id:
                        option.is_correct = False
                        new_options.append(option)
                AnswerOption.objects.bulk_update(new_options, ['is_correct'])

            # если у вопроса не множестенный выбор, то надо сделать неверными все варианты ответа
            if not question.has_multiple_choices:
                all_options = question.answer_options.all()
                new_options = []
                for option in all_options:
                    if option.is_correct and not option.id == self.instance.id:
                        option.is_correct = False
                        new_options.append(option)

                AnswerOption.objects.bulk_update(new_options, ['is_correct'])


    def create(self, validated_data):
        if validated_data.get('is_free_response'):
            if self.context.get('has_free_option', None):
                raise MyValidationError(detail="В данном вопросе уже есть свободная форма ответа")

        for attr, value in self.initial_data.items():
            setter_name = f"set_{attr}"
            if hasattr(self, setter_name):
                getattr(self, setter_name)(value)

        return super().create(validated_data)  

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        for attr, value in self.initial_data.items():
            setter_name = f"set_{attr}"
            if hasattr(self, setter_name):
                getattr(self, setter_name)(value)
        return instance

# сериализаторы статистики опросов

class AnswerOptionStatsSerializer(serializers.ModelSerializer):
    votes_quantity = serializers.SerializerMethodField()
    free_answers = serializers.SerializerMethodField()


    def get_votes_quantity(self, instance):
        option_id = instance.id
        options_answers_count = self.context.get('options_answers_count', [])
        for item in options_answers_count:
            if item['answer_option'] == option_id:
                return item['quantity']
        return 0


    def get_free_answers(self, instance):
        if instance.is_free_response:
            free_answers = []
            question_id = instance.question.id
            user_answers = self.context.get('free_answers', [])
            for item in user_answers:
                if item['question_id'] == question_id:
                    if item.get('user_id'):
                        answer = {
                            'name': (item.get('profile_name') or '') + ' ' + (item.get('profile_surname', '') or ''),
                            'text': item.get('text') or ''
                        }
                    else:
                        answer = {
                            'name': (item.get('auth_field_name') or '') + ':' + (item.get('auth_field_answer', '') or ''),
                            'text': item.get('text') or ''
                        }
                    free_answers.append(answer)
            return free_answers
             
    class Meta:
        model = AnswerOption
        fields = ['id', 'name', 'votes_quantity', 'is_free_response', 'free_answers'] 
            

class PollQuestionStatsSerializer(serializers.ModelSerializer):
    answer_options = AnswerOptionStatsSerializer(many=True)

    votes_quantity = serializers.SerializerMethodField()
    answer_percentage = serializers.SerializerMethodField()
    average_correctness_percentage = serializers.SerializerMethodField()

    def get_votes_quantity(self, instance):
        question_id = instance.id
        questions_percentage = self.context.get('questions_percentage', [])

        for item in questions_percentage:
            if item['question_id'] == question_id:
                return item['answers_quantity']
        return 0
 
    def get_average_correctness_percentage(self, instance):
        question_id = instance.id
        questions_percentage = self.context.get('questions_percentage', [])

        for item in questions_percentage:
            if item['question_id'] == question_id:
                return item['correct_percentage']
        return 0
    
    def get_answer_percentage(self, instance):
        question_id = instance.id
        question_statistics = self.context.get('questions_percentage', [])
        for question in question_statistics:
            if question['question_id'] == question_id:
                return question['answer_percentage']
        return None
    
    
    class Meta:
        model = PollQuestion
        fields = ['id', 'answer_options', 'name', 'votes_quantity', 'has_multiple_choices',
                  'average_correctness_percentage', 'answer_percentage']



class PollStatsSerializer(serializers.ModelSerializer):
    participants_quantity = serializers.SerializerMethodField()
    questions_quantity = serializers.SerializerMethodField()
    correct_answer_percentage = serializers.SerializerMethodField()

    questions = PollQuestionStatsSerializer(many=True)

    def get_participants_quantity(self, instance):
        return instance.participants_quantity

    def get_questions_quantity(self, instance):
        return instance.questions_quantity

    def get_correct_answer_percentage(self, instance):
        poll_statistics = self.context.get('poll_statistics', None)

        if poll_statistics:
            average_correct_percentage = poll_statistics.get('average_correct_percentage', None)
            if average_correct_percentage:
                return round(average_correct_percentage, 2)
            
        return None
    
    class Meta:
        model = Poll
        fields = ['participants_quantity', 'questions_quantity', 'questions', 'correct_answer_percentage']




class SupportRequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequestType
        fields = '__all__'

    

class SupportRequestBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequest
        fields = '__all__'


class SupportRequestSerializer(SupportRequestBaseSerializer):
    author = GetProfileSerializer()
    type = SupportRequestTypeSerializer()


class QuickVotingFormSerializer(serializers.ModelSerializer):
    auth_field_answers = MiniPollAuthFieldAnswerSerializer(many=True, required=False)

    class Meta:
        model = QuickVotingForm
        fields = '__all__'     


class QuickPollAnswerSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        my_answers = serializers.ModelSerializer.to_representation(self, instance)
        # poll = self.context.get('poll', None)        
        data = {
                    # 'questions': PollQuestionSerializer(poll.questions.all(), many=True).data,
                    'answers': my_answers,
                }

        # all_answers = [my_answers]
        # for question in data['questions']: # проходим по всем вопросам 
        #     if question.get('is_answered') is None: # проверка чтобы не занулять вопрос на который дан ответ
        #         question['is_answered'] = False # если ответ уже дан, то не делаем его False
        #     for answer_option in question['answer_options']: # проходим по всем вариантам ответа 

        #         if answer_option.get('is_answered') is None: # проверка на то что на вариант ответа еще не ответили
        #             answer_option['is_chosen'] = False # отмечаем, что вариант ответа изначально не выбран
        #             answer_option['text'] = None # отмечаем, что текст для варианта ответа изначально не указан

        #         for answer in all_answers: # проходим по всем моим ответам
        #             if answer['answer_option'] == answer_option['id']: # выбираем ответ по совпавшим id
        #                 question['is_answered'] = True # отмечаем, что вопрос отвечен
        #                 answer_option['is_chosen'] = True # отмечаем, что вариант ответа был выбран
        #                 answer_option['text'] = answer.get('text', None) # добавляем текст ответа, если он был дан

        return data
    
    class Meta:
        model = PollAnswer
        fields = ['id', 'question', 'answer_option', 'text']



class QuickPollAnswerGroupSerializer(serializers.ModelSerializer):
    quick_voting_form = QuickVotingFormSerializer()
    answers = QuickPollAnswerSerializer(many=True)

    class Meta:
        model = PollAnswerGroup
        fields = '__all__'


class PollAnswersSerializer(serializers.ModelSerializer):
    answer_option = serializers.CharField(source='answer_option.name')

    def to_representation(self, instance):
        my_answers = serializers.ModelSerializer.to_representation(self, instance)
        # poll = self.context.get('poll', None)        
        data = {
                    # 'questions': PollQuestionSerializer(poll.questions.all(), many=True).data,
                    'answers': my_answers,
                }

        # all_answers = [my_answers]
        # for question in data['questions']: # проходим по всем вопросам 
        #     question_correct_quantity = 0
        #     question_gained_quantity = 0
        #     if question.get('is_answered') is None: # проверка чтобы не занулять вопрос на который дан ответ
        #         question['is_answered'] = False # если ответ уже дан, то не делаем его False
        #         question['points'] = 0  # изначально начисляем 0 баллов за каждый
        #         question['options_quantity'] = 0  # изначально считаем колво верных вариантов ответа
        #     for answer_option in question['answer_options']: # проходим по всем вариантам ответа 

        #         if answer_option.get('is_answered') is None: # проверка на то что на вариант ответа еще не ответили
        #             answer_option['is_chosen'] = False # отмечаем, что вариант ответа изначально не выбран
        #             answer_option['text'] = None # отмечаем, что текст для варианта ответа изначально не указан
        #             answer_option['points'] = 0 # отмечаем, сколько баллов получили за ответ

        #         for answer in all_answers: # проходим по всем моим ответам
        #             if answer['answer_option'] == answer_option['id']: # выбираем ответ по совпавшим id
        #                 question['is_answered'] = True # отмечаем, что вопрос отвечен
        #                 answer_option['is_chosen'] = True # отмечаем, что вариант ответа был выбран
        #                 answer_option['text'] = answer.get('text', None) # добавляем текст ответа, если он был дан
        #                 answer_option['points'] = answer['points'] # начисляем очки, которые получили после проверки правильности

        #                 if answer_option['points'] is not None: # проверяем что очки вообще есть
        #                     if answer_option['points'] > 0: # если выбрали верную опцию, то добавляем балл
        #                         question_gained_quantity += answer_option['points']
        #                     else:
        #                         answer_option['points'] = -1 # если выбрали неверную опцию, то убавляем балл
        #                         question_gained_quantity += answer_option['points']
            

            # if poll.poll_type.name == 'Викторина2':
            #     question['points'] += round(question_gained_quantity / question_correct_quantity, 2) # начисляем очки, которые получили после проверки правильности
            #     if question['points'] < 0:
            #         question['points'] = 0
            #     poll_gained_points += question['points']
            #     poll_points += 1

            #     results = {
            #             'total': poll_points,
            #             'correct': poll_gained_points,
            #             'wrong': poll_points - poll_gained_points,
            #             'percentage': round(float(poll_gained_points / poll_points) * 100, 2),
            #         }
                
            #     data['results'] = results

        return data
    

    class Meta:
        model = PollAnswer
        fields = '__all__'

class MyPollUsersAnswersSerializer(serializers.ModelSerializer):
    answers = PollAnswersSerializer(many=True, read_only=True)
    profile = serializers.SerializerMethodField()

    # answerss = serializers.SerializerMethodField()

    # def get_answerss(self, instance):
    #     if instance.answers.count() > 2:
    #         print(instance.id, end=" ")
    #         print(instance.answers.all())


    def get_profile(self, instance):
        poll_type = self.context.get('poll_type', None)
        if poll_type and poll_type == 'Быстрый':
            auth_field_answers_dict = self.context.get('auth_field_answers_dict', {})
            answer_group_id = instance.id

            cur_quick_voting_form = None
            for quick_voting_form_id, answers in auth_field_answers_dict.items():
                if any(answer.quick_voting_form.poll_answer_group.id == answer_group_id for answer in answers):
                    cur_quick_voting_form = quick_voting_form_id
                    break

            if cur_quick_voting_form is not None:
                cur_quick_voting_form_fields = {
                    answer.auth_field.name: answer.answer
                    for answer in auth_field_answers_dict[cur_quick_voting_form]
                }

                fio = cur_quick_voting_form_fields.get('ФИО', '').strip()
                fio_parts = list(filter(None, map(str.strip, fio.split(' ', maxsplit=2))))
                while len(fio_parts) < 3:
                    fio_parts.append('')
                fio_parts = fio_parts[0:3]
                surname, name, patronymic = fio_parts
                data = {
                    'surname': surname,
                    'name': name,
                    'patronymic': patronymic,
                    'student_id': cur_quick_voting_form_fields.get('Номер студенческого билета', ''),
                    'group': cur_quick_voting_form_fields.get('Группа', ''),
                }
                return data

        return MiniProfileSerializer(instance.profile).data

    class Meta:
        model = PollAnswerGroup
        fields = '__all__'
