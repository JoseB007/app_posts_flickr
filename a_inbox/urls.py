from django.urls import path

from . import views

app_name = 'inbox'
urlpatterns = [
    path('', views.InboxView.as_view(), name='inbox'),
    path('notify-inbox/', views.NotifyInboxView.as_view(), name='notify-inbox'),
    path('<pk>/', views.InboxView.as_view(), name='inbox-conversation'),
    path('new-conversation/<pk>/', views.CreateConversationView.as_view(), name='new-conversation'),
    path('send/<pk>/', views.SendMessageView.as_view(), name='send'),
]