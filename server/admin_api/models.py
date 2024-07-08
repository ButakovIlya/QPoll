from django.db import models


class Settings(models.Model):
    max_users_polls_quantity = models.PositiveSmallIntegerField(default=10)
    max_users_tickets_quantity = models.PositiveSmallIntegerField(default=1)
    max_questions_quantity = models.PositiveSmallIntegerField(default=50)
    min_questions_quantity = models.PositiveSmallIntegerField(default=1)
    max_question_options_quantity = models.PositiveSmallIntegerField(default=10)
    min_question_options_quantity = models.PositiveSmallIntegerField(default=1)
    max_revotes_quantity = models.PositiveSmallIntegerField(default=2)

    is_under_maintenance = models.BooleanField(default=False)


    
    def __str__(self):
        return f"Настройки проекта"
