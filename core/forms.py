from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class ThreadsContentForm(ModelForm):

    class Meta:

        model = ThreadsContent
        fields = '__all__'

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio', 'location']