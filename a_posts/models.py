from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.
class Post(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    creation_date = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    url = models.URLField(verbose_name="URL" ,max_length=500, null=True)
    artist = models.CharField(verbose_name="Artista" ,max_length=150, null=True)
    title = models.CharField(verbose_name="Título", max_length=500)
    image = models.URLField(verbose_name="Imagen", max_length=500)
    body = models.TextField(verbose_name="Cuerpo")
    tags = models.ManyToManyField('tag', verbose_name="Categorías")
    author = models.ForeignKey(User, verbose_name="Autor", on_delete=models.SET_NULL, null=True, related_name='posts')

    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-creation_date']

    def get_author(self):
        if self.author:
            author = {
                'full_name': self.author.profile.get_full_name(),
                'avatar': self.author.profile.get_image()
            }
        else:
            author = {
                'full_name': 'Anónimo',
                'avatar': '/static/img/avatars/default.jpg'
            }
        return author


class Tag(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=30)
    slug = models.SlugField(max_length=30)

    def __str__(self):
        return str(self.name)
    

class Comment(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    creation_date = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    body = models.TextField(verbose_name="Cuerpo")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')

    def __str__(self):
        return f"Comentario de {self.author} en {self.post.title}"
        
    class Meta:
        ordering = ['-creation_date']


class Reply(models.Model):
    id = models.CharField(max_length=150, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    creation_date = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    body = models.TextField(verbose_name="Cuerpo")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='replies')

    def __str__(self):
        return f"Respuesta de {self.author} al comentario de {self.comment.author} en {self.comment.post.title}"
    
    class Meta:
        ordering = ['-creation_date']
