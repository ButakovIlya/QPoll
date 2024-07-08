# Сигналы Django
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Poll, PollQuestion

import os


@receiver(post_delete, sender=Poll)
def poll_delete_handler(sender, instance, **kwargs):
    if instance.image:
        file_path = str(instance.image.path)
        if os.path.exists(file_path):
            os.remove(file_path)
    if instance.qrcode:
        file_path = str(instance.qrcode.path)
        if os.path.exists(file_path):
            os.remove(file_path)


@receiver(post_delete, sender=PollQuestion)
def poll_question_delete_handler(sender, instance, **kwargs):
    if instance.image:
        file_path = str(instance.image.path)
        if os.path.exists(file_path):
            os.remove(file_path)
