from django import forms
from django.contrib.auth.models import User
from gamefolio_app.models import Author, List, Game



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('website', 'picture',)

class CreateListForm(forms.ModelForm):
    games = forms.ModelMultipleChoiceField(queryset=Game.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = List
        fields = ['title', 'description', 'games']


