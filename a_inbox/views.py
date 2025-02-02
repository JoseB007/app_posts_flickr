from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count

from a_profile.models import Profile

from .models import Conversation
from .forms import InboxMessageForm

# Create your views here.
class InboxView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'a_inbox/inbox.html'

    def get(self, request, *args, **kwargs):
        # Buscar usuario para iniciar una nueva conversación
        if request.headers.get('HX-Request') == 'true':
            terms = request.GET.get("search_user")
            profiles = Profile.objects.filter(full_name__icontains=terms)

            return render(request, 'a_inbox/snippets/search_user.html', {'profiles': profiles})

        # Buscar una conversación
        id_conversation = self.kwargs.get('pk')  # Usar get para evitar KeyError
        if id_conversation:
            # Manejar explícitamente el caso en el que no se encuentra la conversación
            conversation = get_object_or_404(Conversation, pk=id_conversation)
            # Cambiar el estado de la conversación si todos los usuarios la han visto 
            if conversation.is_read == False and conversation.messages.first().sender != request.user:
                conversation.is_read = True
            conversation.save()

            context = {
                'conversations': Conversation.objects.all(),
                'conversation': conversation,
                'form': InboxMessageForm(),
                'users': User.objects.all()
            }
            return render(request, 'a_inbox/inbox.html', context)

        # Si no hay 'pk', usar la lógica predeterminada
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()[:10]
        context['conversations'] = Conversation.objects.all()
        return context


class SendMessageView(LoginRequiredMixin, generic.FormView):
    form_class = InboxMessageForm
    template_name = 'a_inbox/conversation.html'

    def form_valid(self, form):
        conversation = get_object_or_404(Conversation, pk=self.kwargs['pk'])
        message = form.save(commit=False)
        message.sender = self.request.user
        message.conversation = conversation
        message.save()

        if conversation.is_read == True:
            conversation.is_read = False

        conversation.lastmessage_created = message.created
        conversation.save()

        context = {
            'conversations': Conversation.objects.all(),
            'conversation': conversation,
        }
        return render(self.request, 'a_inbox/snippets/chat-history.html', context)
    
    def form_invalid(self, form):
        return JsonResponse({'error': form.errors}, status=400)
    

class CreateConversationView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))

        context = {
            'user': user,
            'form': InboxMessageForm()
        }

        return render(request, 'a_inbox/snippets/new_conversation.html', context)
    
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        form = InboxMessageForm(request.POST)

        users_conversation = [request.user, user]
        id_users = set(u.pk for u in users_conversation)
        conversation_users = None

        if form.is_valid():

            # Buscar conversaciones del usuario actual asegurando la total cantidad de participantes
            conversations = (
                Conversation.objects.annotate(num_p=Count('participants'))
                .filter(num_p=len(id_users))
                .filter(participants=request.user)
            )

            # Verificar que exactamente sean los mismos participantes
            for c in conversations:
                users_c = set(c.participants.values_list('pk', flat=True))
                if users_c == id_users:
                    conversation_users = c

            if not conversation_users:
                conversation_users = Conversation.objects.create()
                conversation_users.participants.set(id_users)

            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation_users
            message.save()

            if conversation_users.is_read == True:
                conversation_users.is_read = False

            conversation_users.lastmessage_created = message.created
            conversation_users.save()

            return redirect(reverse('inbox:inbox-conversation', args=[conversation_users.pk]))
        else:
            return JsonResponse({'error': form.errors}, status=400)


class NotifyInboxView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):
        my_conversations = Conversation.objects.filter(participants=self.request.user, is_read=False)
        for c in my_conversations:
            latest_message = c.messages.first()
            if latest_message.sender != request.user:
                return render(request, 'a_inbox/notify_icon.html')
        return HttpResponse("")