from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import InboxMessage, Conversation
from .forms import InboxMessageForm

# Create your views here.
class InboxView(LoginRequiredMixin, generic.ListView):
    model = Conversation
    template_name = 'a_inbox/inbox.html'
    context_object_name = 'conversations'


class ConversationView(generic.DetailView):
    model = Conversation
    template_name = 'a_inbox/conversation.html'
    context_object_name = 'conversation'

    def get(self, request, *args, **kwargs):
        conversation = get_object_or_404(Conversation, pk=kwargs['pk'])

        context = {
            'conversation': conversation,
            'form': InboxMessageForm()
        }

        return render(request, 'a_inbox/conversation.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InboxMessageForm()
        return context


class SendMessageView(generic.FormView):
    form_class = InboxMessageForm
    template_name = 'a_inbox/conversation.html'

    def form_valid(self, form):
        conversation = get_object_or_404(Conversation, pk=self.kwargs['pk'])
        message = form.save(commit=False)
        message.sender = self.request.user
        message.conversation = conversation
        message.save()

        context = {
            'conversation': conversation,
        }
        return render(self.request, 'a_inbox/snippets/chat-history.html', context)
    
    def form_invalid(self, form):
        return JsonResponse({'error': form.errors}, status=400)