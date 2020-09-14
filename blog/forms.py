from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta: #(check here later if there should be () or not need for it)
        fields = ('author', 'title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        filter('author','text')

        widgets = {
            'author': forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
        }





