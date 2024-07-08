from django.contrib import admin
from .models import *


admin.site.register(UserRole)
admin.site.register(Profile)
admin.site.register(PollType)
admin.site.register(Poll)
admin.site.register(PollSettings)
admin.site.register(AnswerOption)
admin.site.register(PollAnswer)
admin.site.register(PollQuestion)
admin.site.register(PollAnswerGroup)
admin.site.register(PollParticipantsGroup)
admin.site.register(PollRegistration)

admin.site.register(SupportRequest)
admin.site.register(SupportRequestType)

admin.site.register(QuickVotingForm)
admin.site.register(PollAuthField)
admin.site.register(PollAuthFieldAnswer)
