from django.forms import ModelForm, PasswordInput, TextInput
from django import forms
from ...models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        #fields = '__all__'
        fields = ['title']
        #exclude = ['uploaded_by_id', 'users_who_like']
        widgets = {
            'title' : TextInput(attrs={'placeholder': '<título>'}),
        }
        labels = {
            'title'  : 'Título',
        }

    def clean(self):
        cleaned_data = super(BookForm, self).clean()
        title = cleaned_data.get("title")
        if (len(title) < 2):
            raise forms.ValidationError(
                "Título >= 2 y Descripción >= 5"
        )