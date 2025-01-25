from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Profile
from .forms import ProfileForm

# Create your views here.
class ViewProfile(generic.DetailView):
    model = Profile
    template_name = "a_profile/profile.html"
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        if username:
            self.object = get_object_or_404(Profile, user__username=username)
        else:
            try:
                self.object = get_object_or_404(Profile, user=self.request.user)
            except:
                raise Http404()
        return self.object
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if request.headers.get('HX-Request') == 'true':
            if 'top-post' in request.GET:
                posts = self.get_object().user.posts.annotate(num_likes=Count("likes")).filter(num_likes__gt=0).order_by("-num_likes")[:3]
                
            elif 'latest' in request.GET:
                posts = self.get_object().user.posts.all()
                
            elif 'liked-posts' in request.GET:
                # posts = Post.objects.filter(post_likes__user=self.get_object().user).order_by('-post_likes__created')
                posts = self.get_object().user.likedposts.order_by('-post_likes__created')

            response = render(request, "a_posts/snnipets/add_top_posts.html", {'posts': posts})
            return response
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.user.posts.all()
        return context


class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    template_name = "a_profile/profile_update.html"
    form_class = ProfileForm
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = "update_profile"
        return context

    def get_object(self, queryset=None):
        if self.request.user.is_anonymous:
            return None
        else:
            profile = get_object_or_404(Profile, user=self.request.user)
        return profile
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    # Este método es llamado cuando se envía el formulario para actualizar el perfil de usuario
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'update_profile':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    return redirect('profile:profile')
                else:
                    data['error'] = form.errors
                    return JsonResponse(data)
            else:
                data['error'] = 'Acción invalida'
                return JsonResponse(data)
        except Exception as e:
            data['error'] = str(e)
            return JsonResponse(data)
    

    

