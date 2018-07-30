from django import forms
from .models import Image, Profile, Comment


class NewImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['user', 'post_date', 'liker', 'profile']

class NewProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'followers', 'following']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user', 'image']
