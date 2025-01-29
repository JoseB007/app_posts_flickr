from django.forms import *

from a_profile.models import Profile

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

# class UsersAddForm(Form):
#     users = CharField(
#         max_length=150,
#         widget=TextInput(
#             attrs={
#                 'class': "p-3",
#                 "placeholder": "Search user ..."
#             }
#         )
#     )


# class UsersCheckForm(Form):
#     users = ModelMultipleChoiceField(
#         queryset=Profile.objects.all(),
#         required=False,
#         widget=CheckboxSelectMultiple,
#     )