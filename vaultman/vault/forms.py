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
        widgets = {
            'name': TextInput(attrs={'placeholder':"Folder Name...", 'class':'rounded-lg border-2 border-violet-500'}),
            'color': TextInput(attrs={'type':"color", 'class':'h-12'})
        }
        labels = {
            'color': "Choose Folder color: "
        }