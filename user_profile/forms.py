from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm, Form, EmailField, CharField, PasswordInput

from user_profile.models import Profile


class RegistrationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'bio', 'vk_page', 'last_name', 'email', 'username', 'password']

    def __str__(self):
        return self.name

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Login'))
        self.helper.form_method = 'post'


class PasswordResetRequestForm(Form):
    email = EmailField(label="Email", max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Send email'))
        self.helper.form_method = 'post'


class PasswordResetForm(Form):
    password = CharField(label="New Password", max_length=254, widget=PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.form_method = 'post'
