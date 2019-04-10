from django import forms

class CreateProjectForm(forms.Form):
    author_first_name = forms.CharField(max_length=50)
    author_last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=254)
    dataset_types=forms.IntegerField()

    project_description = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )

    # source = forms.CharField(       # A hidden input for internal use
    #     max_length=50,              # tell from which page the user sent the message
    #     widget=forms.HiddenInput()
    # )

    def clean(self):
        cleaned_data = super(CreateProjectForm, self).clean()
        author_first_name = cleaned_data.get('author_first_name')
        author_last_name = cleaned_data.get('author_last_name')
        email = cleaned_data.get('email')
        project_description = cleaned_data.get('project_description')


        if not email and not email and not message:
            raise forms.ValidationError('You have to write something!')
