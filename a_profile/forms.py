from django.forms import *

from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]

        labels = {
            "full_name": "Name",
        }

        widgets = {
            "image": FileInput(),
            "bio": Textarea(attrs={"rows": 3}),
        }
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.fields["full_name"].initial = self.instance.user.get_full_name()

