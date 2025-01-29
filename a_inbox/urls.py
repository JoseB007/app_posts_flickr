from django.urls import path

from . import views

app_name = 'inbox'
urlpatterns = [
    path('', views.InboxView.as_view(), name='inbox'),
    path('<pk>/', views.InboxView.as_view(), name='inbox-conversation'),
    path('send/<pk>/', views.SendMessageView.as_view(), name='send'),
    path('new-conversation/<pk>/', views.CreateConversationView.as_view(), name='new-conversation'),
]