from django import forms

from .models import Post,Category,Comment



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','category','tags')
      

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')