from django import forms
from django.contrib.auth.models import User
from .models import Post,Category,Comment,Profile
from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')





class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic',)



class UserProfileUpdateForm(forms.Form):
    first_name = forms.CharField(label='First Name',max_length=100)
    last_name = forms.CharField(label='Last Name',max_length=100)
    email = forms.EmailField(label='Email',max_length=100)
    profile_pic = forms.ImageField(label='Profile Pic')
    

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','category')
      

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')