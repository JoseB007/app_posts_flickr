from django.contrib import admin

from .models import InboxMessage, Conversation

# Register your models here.
admin.site.register(InboxMessage)
admin.site.register(Conversation)