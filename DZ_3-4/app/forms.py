from django import forms
from django.db import IntegrityError
from app import models

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 30)
    password = forms.CharField(max_length = 100, widget = forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_repeat = forms.CharField(widget=forms.PasswordInput, required=True)
    avatar = forms.FileField(widget=forms.FileInput, required=False)
    class Meta:
        model = models.Profile
        model = models.User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_repeat', 'avatar']

    def clean(self):                    
        password = self.cleaned_data['password']
        password_repeat = self.cleaned_data['password_repeat']
        if password != password_repeat:  
            self.add_error('password', error='')                          
            self.add_error('password_repeat', error='')                          
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data
    def save(self):
        cleaned_data = self.cleaned_data.copy()
        cleaned_data.pop('password_repeat')
        cleaned_data.pop('avatar')
        try:
            return models.User.objects.create_user(**cleaned_data)
        except IntegrityError:
            # пользователь уже существует
            return None

class SettingsForm(forms.ModelForm):
    avatar = forms.FileField(widget=forms.FileInput(), required=False, label="New avatar")
    Delete_avatar = forms.BooleanField(required=False)
    class Meta:
        model = models.User
        fields = ['username', 'email', 'first_name', 'last_name', 'avatar']
    def save(self):
        user = super().save()
        print("self.cleaned_data = ", self.cleaned_data)
        profile = user.profile
        if self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
        if self.cleaned_data['Delete_avatar']:
            profile.avatar.delete(save=False)
            profile.avatar = 'avatars/common_avatar.png'
        profile.save()
        
        return user

class AskForm(forms.ModelForm):
    tag_list = forms.CharField(required=False)
    title = forms.CharField(widget = forms.TextInput(), required=True)
    text = forms.CharField(widget = forms.Textarea(attrs={"rows" : "5"}))
    class Meta:
        model = models.Question
        fields = ['title', 'text', 'tag_list']

class AnswerForm(forms.ModelForm):
    text = forms.CharField(widget = forms.Textarea(attrs={"rows" : "3"}), label="Text answer", required=True)
    class Meta:
        model = models.Answer
        fields = ['text']