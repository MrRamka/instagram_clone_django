from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field
from django import forms
from django.forms import ModelForm

from core.models import Image


class ImageUploadForm(ModelForm):
    hashtag = forms.CharField(required=False)
    place = forms.CharField(required=False)

    class Meta:
        model = Image
        fields = ['description', 'image_obj']
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.form_method = 'post'
