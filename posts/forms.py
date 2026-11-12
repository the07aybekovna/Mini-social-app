from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption','image']
        widgets = {
            'caption': forms.TextInput(attrs={
                'placeholder': 'What is on your mind?',
                'rows':4,
                'class': 'form-text',
        }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
            })
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write a comment...',
                'rows': 2,
                'class': 'comment-input'
            })
        }