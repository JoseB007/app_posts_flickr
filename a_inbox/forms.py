from django.forms import *

from .models import InboxMessage

class InboxMessageForm(ModelForm):
    class Meta:
        model = InboxMessage
        fields = ['body']
        widgets = {
            'body': TextInput(
                attrs={
                    'placeholder': 'Type your message here...',
                }
            )
        }