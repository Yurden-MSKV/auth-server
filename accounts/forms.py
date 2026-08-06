from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['pic', 'username', 'first_name', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'bio': 'О себе',
        }