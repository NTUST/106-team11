from django import forms
from django.utils.translation import ugettext_lazy as _
from missionboard.models import Skill
from accounts.models import Member
from django.db.models import Q
from userena.forms import SignupForm,EditProfileForm,get_profile_model
from django.contrib.auth.models import User
class EditProfileFormExtra(EditProfileForm):
    class Meta(EditProfileForm.Meta):
        exclude = EditProfileForm.Meta.exclude+['user','mugshot','privacy','missions_completed','missions_wip','missions_failed','last_name','level']
    bios = forms.CharField(required=False,widget=forms.Textarea())
    contact = forms.CharField(required=False,widget=forms.Textarea())
    partners = forms.ModelMultipleChoiceField(
        required=False,
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={"class":"main-Select"})
    )
    skills = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={"class":"main-Select"})
    )
    def __init__(self, *args, **kw):
        super(EditProfileForm, self).__init__(*args, **kw)
        # Put the first and last name at the top
        FilterList =[self.instance.user.username,'AnonymousUser']
        self.fields['partners'].queryset = User.objects.filter(~Q(username__in =FilterList))

    def save(self, force_insert=False, force_update=False, commit=True):
        profile = super(EditProfileFormExtra, self).save(commit=commit)
        settings_profile = profile
        settings_profile.bios = self.cleaned_data['bios']
        settings_profile.contact = self.cleaned_data['contact']
        settings_profile.skills = self.cleaned_data['skills']
        settings_profile.partners = self.cleaned_data['partners']
        profile.save()

        return profile

class SignupFormExtra(SignupForm):
    bios = forms.CharField(required=False,widget=forms.Textarea())
    contact = forms.CharField(required=False,widget=forms.Textarea())
    skills = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={"class":"main-Select"})
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
