from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Profile, SupportRequest, SupportRequestType
from .models import *
from .validators import *

from functools import partial

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_role(self, obj):
        return obj.role.role if obj.role else None
    

class SupportRequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportRequestType
        fields = '__all__'

    

class SupportRequestSerializer(serializers.ModelSerializer):
    type = SupportRequestTypeSerializer()

    class Meta:
        model = SupportRequest
        fields = '__all__'


class ProjectSettingsSerializer(serializers.ModelSerializer):
    max_questions_quantity = serializers.IntegerField(validators=[partial(BaseProjectSettingsValidator.max_questions_quantity, num=100)])
    min_questions_quantity = serializers.IntegerField(validators=[partial(BaseProjectSettingsValidator.min_questions_quantity, num=1)])
    max_question_options_quantity = serializers.IntegerField(validators=[partial(BaseProjectSettingsValidator.max_question_options_quantity, num=15)])
    min_question_options_quantity = serializers.IntegerField(validators=[partial(BaseProjectSettingsValidator.min_question_options_quantity, num=1)])
    
    class Meta:
        model = Settings
        fields = '__all__'

