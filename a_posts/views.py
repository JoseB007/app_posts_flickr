from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from bs4 import BeautifulSoup

import requests

from .models import Post, Tag, Comment
from .forms import FormPost, FormComment

# Create your views here.
class ViewHome(generic.ListView):
    model = Post
    template_name = 'a_posts/home.html'
    context_object_name = 'posts_list'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.tag = self.kwargs.get('tag')
        if self.tag:
            queryset = queryset.filter(tags__slug=self.tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Django Awesome Posts"
        context['categories'] = Tag.objects.all()
        context['current_tag'] = self.tag
        return context


class ViewCreatePost(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = 'a_posts/post_form.html'
    form_class = FormPost
    success_url = reverse_lazy('a_posts:home_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create_post'
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'create_post':
                form = self.get_form()
                if form.is_valid():
                    post = form.save(commit=False)
                    
                    website = requests.get(form.data['url'])
                    source_code = BeautifulSoup(website.text, 'html.parser')

                    find_image = source_code.select('meta[content^="https://live.staticflickr.com/"]')
                    image = find_image[0]['content']
                    post.image = image

                    find_title = source_code.select('h1.photo-title')
                    title = find_title[0].text.strip()
                    post.title = title
                    
                    find_artist = source_code.select('a[rel="author"]')
                    artist = find_artist[1].text
                    post.artist = artist

                    post.author = request.user

                    post.save()
                    form.save_m2m()

                    return redirect(self.success_url)
                else:
                    data['error'] = form.errors
                    return redirect(self.success_url)
        except Exception as e: 
            data['error'] = str(e)
            return JsonResponse(data)


class ViewDeletePost(LoginRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'a_posts/post_delete.html'
    success_url = reverse_lazy('a_posts:home_view')
    context_object_name = "post"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            if self.object.author != request.user:
                datos['error'] = 'No tienes permisos para eliminar este post'
                return JsonResponse(datos)
            else:
                self.object.delete()
                messages.success(request, "Post deleted")
                return redirect(self.success_url)
        except Exception as e:
            datos['error'] = str(e)
            
            return JsonResponse(datos)


class ViewUpdatePost(LoginRequiredMixin, generic.UpdateView):
    model = Post
    template_name = 'a_posts/post_form.html'
    form_class = FormPost
    context_object_name = "object_post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update_post'
        return context
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('a_posts:post', kwargs={'pk': self.object.pk})
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'update_post':
                form = self.get_form()
                if form.is_valid():
                    if self.object.author != request.user:
                        data['error'] = 'No tienes permisos para actualizar este post'
                        return JsonResponse(data)
                    else:
                        form.save()
                        return redirect(self.get_success_url())
                else:
                    data['error'] = form.errors
                    return JsonResponse(data)
            else:
                data['error'] = 'Acción invalida'
                return JsonResponse(data)
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data)


class ViewPagePost(generic.DetailView):
    model = Post
    template_name = "a_posts/page_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Tag.objects.all()
        context['title'] = "Django Awesome Posts"
        context['action'] = 'create_comment'
        context['form'] = FormComment()
        return context
    
    # Crear un comentario
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'create_comment':
                form = FormComment(request.POST)
                if form.is_valid():
                    commet = form.save(commit=False)
                    commet.author = request.user
                    commet.post = Post.objects.get(pk=self.kwargs['pk'])
                    commet.save()
                    return redirect(self.request.path_info)
                else:
                    data['error'] = form.errors
                    return JsonResponse(data)
            else:
                data['error'] = 'Acción invalida'
                return JsonResponse(data)
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data)

    
class ViewDeleteComment(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = 'a_posts/comment_delete.html'
    context_object_name = "comment"
    
    def get_success_url(self):
        return reverse('a_posts:post', kwargs={'pk': self.get_object().post.pk})

    def post(self, request, *args, **kwargs):
        datos = {}
        try:
            if self.get_object().author != request.user:
                datos['error'] = 'No tienes permisos para eliminar este comentario'
                return JsonResponse(datos)
            else:
                success_url = self.get_success_url()
                self.get_object().delete()
                messages.success(request, "Comment deleted")
                return redirect(success_url)
        except Exception as e:
            datos['error'] = str(e)
            return JsonResponse(datos)
