from django import forms
from posts.models import Post

class PostCreationForm(forms.ModelForm):
    title = forms.CharField(max_length=255)
    content = forms.Textarea()
    class Meta:
        model = Post
        fields = ['title', 'content']
    
