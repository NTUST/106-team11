from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone

from missionboard.models import Skill


class NewMissionForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='任務名稱',
    )

    required_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    def clean_required_skills(self):
        skills = self.cleaned_data['required_skills']
        if skills.count() == 0:
            self.add_error('name', '最少需要一項技能!')
        return skills

    required_level = forms.IntegerField(
        label='等級需求',
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'align-center'
        })
    )

    required_worker_num = forms.IntegerField(
        label='人數需求',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'align-center'
        })
    )

    application_deadline = forms.DateTimeField(
        label='截止報名日期',
        widget=forms.TextInput(attrs={
            'class': 'align-center'
        })
    )

    def clean_application_deadline(self):
        application_deadline = self.cleaned_data['application_deadline']
        if application_deadline < timezone.now():
            self.add_error('application_deadline', '朋友, 你不能活在過去...')
        return application_deadline

    working_deadline = forms.DateTimeField(
        label='任務結束日期',
        widget=forms.TextInput(attrs={
            'class': 'align-center'
        })
    )

    def clean_working_deadline(self):
        working_deadline = self.cleaned_data['working_deadline']
        if working_deadline < timezone.now():
            self.add_error('working_deadline', '朋友, 你不能活在過去...')
        elif working_deadline < self.cleaned_data['application_deadline']:
            self.add_error('working_deadline', '你總不能要求別人在報名確立前就動工吧...')
        return working_deadline

    description = forms.CharField(
        label='任務內容',
        widget=forms.Textarea(attrs={
            'class': 'box',
            'rows': 5,
            'style': 'overflow: hidden; resize: none;',
        })
    )


class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Name'
        })
    )

    email = forms.CharField(
        max_length=150,
        label='Email',
        widget=forms.TextInput(attrs={
            'placeholder': 'Email',
            'type': 'email'
        })
    )

    password = forms.CharField(
        max_length=50,
        label='Password',
        widget=forms.TextInput(attrs={
            'placeholder': 'Password',
            'type': 'password'
        })
    )

    password2 = forms.CharField(
        max_length=50,
        label='Password',
        widget=forms.TextInput(attrs={
            'placeholder': 'Confirm Password',
            'type': 'password'
        })
    )

    def clean(self):
        username = self.cleaned_data['name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        try:
            u = User.objects.get(username=username)
            if u is not None:
                raise DuplicatedInfoException("duplicated usernames!")
        except DuplicatedInfoException:
            self.add_error('name', '使用者名稱已被使用')
        except User.DoesNotExist:
            pass

        try:
            u = User.objects.get(email=email)
            if u is not None:
                raise DuplicatedInfoException("duplicated email!")
        except DuplicatedInfoException:
            self.add_error('email', 'Email已被使用')
        except User.DoesNotExist:
            pass

        if password != password2:
            self.add_error('password2', '密碼不一致！')


class SigninForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Name'
        })
    )

    password = forms.CharField(
        max_length=50,
        label='Password',
        widget=forms.TextInput(attrs={
            'placeholder': 'Password',
            'type': 'password'
        })
    )

    def clean(self):
        username = self.cleaned_data['name']
        password = self.cleaned_data['password']

        u = authenticate(username=username, password=password)
        if u is not None:
            if not u.is_active:
                self.add_error('name', '你的帳號已被停用!')
        else:
            self.add_error('password', '帳號或密碼錯誤!')


class DuplicatedInfoException(Exception):
    pass
