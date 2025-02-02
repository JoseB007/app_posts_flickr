from django.contrib import admin

from .models import InboxMessage, Conversation

# Register your models here.
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('display_participants', 'lastmessage_created', 'is_read')
    readonly_fields = ('participants', 'lastmessage_created', 'is_read')
    list_filter = ('is_read', 'lastmessage_created')


@admin.register(InboxMessage)
class InboxMessageAdmin(admin.ModelAdmin):
    list_display = ["full_name_user", 'conversation', 'created']
    readonly_fields = ("sender", 'conversation', 'created', 'body')

    @admin.display(description="Sender")
    def full_name_user(self, obj):
        return obj.sender.profile.get_full_name()
