from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.http import JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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
    

    

