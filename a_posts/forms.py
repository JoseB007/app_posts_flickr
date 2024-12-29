from django.forms import *

from .models import Post, Comment, Reply

class FormPost(ModelForm):
    class Meta:
        model = Post
        fields = ['url', 'body', 'tags']
        widgets = {
            'body': Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Agregar un cuerpo...',
                    'class': 'font1 text-4xl',
                },
            ),
            'tags': CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and not self.instance._state.adding:
            del self.fields['url']


class FormComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': TextInput(
                attrs={
                    'placeholder': 'Agregar un comentario...',
                },
            ),
        }


class FormReply(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body': TextInput(
                attrs={
                    'placeholder': 'Agregar una respuesta...',
                },
            ),
        }
