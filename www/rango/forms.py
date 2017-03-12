from django import forms
from rango.models import Page, Category


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text='Please enter the category name: ')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # Django models use the Meta class to contain extra information about the model
    # that would not necessarily be appropriate to contain within the model class itself.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name', ) # only include these fields

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text='Please enter the title of the page: ')
    url = forms.URLField(max_length=200, help_text='Please enter the URL of the page: ')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) ## by default it is required field

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page
        exclude = ('category', ) # only exclude these fields. Alternate: "fields = ('title', 'url', 'views')"

    # override the default checking method
    def clean(self):
        print("Checking anything ??")
        cleaned_data = self.cleaned_data # Form have the cleaned_data key/value pair of each form entry
        url = cleaned_data.get('url')

        # url is not empty and also donot start with http://
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data