from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from allauth.account.signals import user_signed_up, user_logged_in

from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    profile, created = Profile.objects.get_or_create(user=instance)
    profile.email = instance.email
    profile.save()

@receiver(post_save, sender=Profile)
def update_user(sender, instance, **kwargs):
    user = get_object_or_404(User, id=instance.user.id)
    if user.email != instance.email:
        user.email = instance.email
        user.save()


# @receiver(user_logged_in)
# def set_new_user_flag(sender, request, user, **kwargs):
#     user.new_user = True
