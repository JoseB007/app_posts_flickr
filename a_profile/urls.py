from django.urls import path

from . import views

app_name = "profile"
urlpatterns = [
    path('update/', views.ProfileEditView.as_view(), name="update-profile"),
    path('user/<str:username>/', views.ViewProfile.as_view(), name="user-profile"),
    path('', views.ViewProfile.as_view(), name="profile"),
]

