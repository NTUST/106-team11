from django import forms
from django.utils.translation import ugettext_lazy as _
from missionboard.models import Skill
from userena.forms import SignupForm

class SignupFormExtra(SignupForm):
    bios = forms.CharField(required=False,widget=forms.Textarea())
    contact = forms.CharField(required=False,widget=forms.Textarea())
    skills = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={"id":"main-Select"})
    )

    #email.widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=75))
    #__bases__.get_field('username').widget =forms.TextInput(attrs=attrs_dict),
    #email.widget=forms.TextInput(attrs=dict(attrs_dict,maxlength=75))
    #password1.widget=forms.PasswordInput(attrs=attrs_dict,render_value=False)

    def save(self):

        new_user = super(SignupFormExtra, self).save()

        # Get the profile, the `save` method above creates a profile for each
        # user because it calls the manager method `create_user`.
        # See: https://github.com/bread-and-pepper/django-userena/blob/master/u$
        user_profile = new_user.my_profile
        user_profile.bios = self.cleaned_data['bios']
        user_profile.contact = self.cleaned_data['contact']
        user_profile.skills = self.cleaned_data['skills']
        user_profile.level = 0

        user_profile.save()

        # Userena expects to get the new user from this form, so return the new
        # user.
        return new_user
