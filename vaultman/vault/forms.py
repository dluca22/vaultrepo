from .models import Login , Folder
from django.forms import ModelForm, Textarea, PasswordInput, Select , TextInput

class LoginForm(ModelForm):


    class Meta:
        model= Login
        fields = ('title', 'username', 'password', 'note', 'folder', 'protected', 'favorite', 'uri',)
        widgets = {
            'title': TextInput(attrs={"class":"rounded-lg "}),
            'username': TextInput(attrs={"class":"rounded-lg "}),
            'password': PasswordInput(render_value=True, attrs={"class":"rounded-lg border-2"}),
            'note': Textarea(attrs={'rows':6, 'placeholder':"Add notes here...", 'class':'rounded-lg border-2 '}),
            'uri': TextInput(attrs={'placeholder': "url...", "class":"rounded-lg border-2 "}),
            'folder': Select(attrs={"class":"rounded-lg border-2 "})
        }

class FolderForm(ModelForm):
    class Meta:
        model = Folder
        fields = ('name', 'color',)
        widgets = {
            'name': TextInput(attrs={'placeholder':"Folder Name...", 'class':'rounded-lg border-2 border-violet-500'}),
            'color': Select(attrs={'class':'flex rounded-xl mx-2 p-1 text-black'})
        }
        labels = {
            'color': "Folder color: "
        }