from django import forms


class SearchForm(forms.Form):
    tags = forms.CharField(label="searched tags")

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class UploadForm(forms.Form):
    files = forms.FileField(label="uploaded files")

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)
    
    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class FileFieldForm(forms.Form):
    file_field = MultipleFileField(label="uploaded files")

class TagForm(forms.Form):
    name = forms.CharField(label="tag name")
    category = forms.ChoiceField(label="tag category", choices={
        "N": "Normal",
        "G": "Character",
        "R": "Artist",
        "P": "Copyright",
    })

class ImageTagForm(forms.Form):
    name = forms.CharField(label="tag name")