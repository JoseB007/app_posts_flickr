from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timesince import timesince

from cryptography.fernet import Fernet

from a_core import settings

import uuid


# Create your models here.
class InboxMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    @property
    def body_decrypted(self):
        f = Fernet(settings.ENCRYPT_KEY)
        try:
            message_decrypted = f.decrypt(self.body)
            message_decoded = message_decrypted.decode('utf-8')
            message = message_decoded
        except:
            message = self.body
        return message

    def __str__(self):
        time_since = timesince(self.created, timezone.now())
        return f"Message from {self.sender.username} sent {time_since} ago"


class Conversation(models.Model):
    id = models.CharField(max_length=100, primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    participants = models.ManyToManyField(User, related_name='conversations')
    lastmessage_created = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-lastmessage_created']

    # Descripción corta que puede ser usada en el sitio de administración
    def display_participants(self):
        return ", ".join(user.profile.full_name for user in self.participants.all())
    display_participants.short_description = "Participants"

    def __str__(self):
        user_names = ", ".join(user.profile.full_name for user in self.participants.all())
        return f"Conversation: {user_names}"

    