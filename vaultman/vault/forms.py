from .models import Login , Folder
from django.forms import ModelForm, Textarea, PasswordInput, URLInput, TextInput

class LoginForm(ModelForm):


    class Meta:
        model= Login
        fields = ('title', 'username', 'password', 'note', 'folder', 'protected', 'favorite', 'uri',)
        widgets = {
            'password': PasswordInput(render_value=True),
            'note': Textarea(attrs={'rows':6, 'placeholder':"Add notes here..."}),
            'uri': TextInput(attrs={'placeholder': "url...", })
        }

class FolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ('name', 'color',)
        # widgets = {
        #     'color': Textarea(attrs={'type':"color"})
        # }