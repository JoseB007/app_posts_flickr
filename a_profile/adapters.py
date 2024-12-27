# from allauth.account.adapter import DefaultAccountAdapter
# from django.shortcuts import resolve_url

# class MyAccountAdapter(DefaultAccountAdapter):
#     def get_login_redirect_url(self, request):
#         if hasattr(request.user, 'new_user') and request.user.new_user:
#             request.user.new_user = False
#             return resolve_url('profile_update')
#         return super().get_login_redirect_url(request)