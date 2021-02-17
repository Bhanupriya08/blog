from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post,Category,Comment,Profile
from django.shortcuts import redirect
from .forms import PostForm, CommentForm,UserProfileForm,UserUpdateForm,UserCreateForm
from taggit.models import Tag
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from blog.settings import BASE_DIR #to delete old profile pic
import os



# Create your views here.
def profile(request):
    username= request.user
    user = User.objects.get(username=username)
    try:
        pic = Profile.objects.get(user=user)
    except:
        profile = Profile(user=user,profile_pic=" ")
        
        profile.save()
        pic = profile.profile_pic
    return render(request,'post/profile.html',{'user':user,"pic":pic})

@login_required
def profile_edit(request,id):
    user = get_object_or_404(User,id=id)
    pic = get_object_or_404(Profile,user=user)
    
    p_form = UserProfileForm(request.POST,request.FILES,instance=pic)
    u_form = UserUpdateForm(request.POST,instance=user)
    if request.method == 'POST':
        
        if p_form.is_valid() and u_form.is_valid():
            """p_form.save(commit=False)
            if pic.profile_pic != None:
                p_form.profile_pic = p_form.cleaned_data.get('profile_pic')"""

            
            #os.remove(BASE_DIR+'\profiles'+pic.profile_pic.url)
            
            u_form.save()
            p_form.save()
            message = 'Your profile has been updated'
            return redirect('post:profile')
    else:
        print(user)
        p_form = UserProfileForm(instance=pic)
        u_form = UserUpdateForm(instance=user)
        return render(request,'post/profile_edit.html',{'p_form':p_form,'u_form':u_form})



def sign_up(request):
    form = UserCreateForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            
            user = form.save()

            login(request,user)
            
            return redirect('post:post_list')
    else:
        form = UserCreateForm()
        return render(request,'registration/sign_up.html',{'form':form})



def post_list(request,tag_slug=None):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    tag = None
    if tag_slug :
        tag = get_object_or_404(Tag,slug = tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request, 'post/post_list.html', {"posts":posts,"tag":tag})



def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True,parent__isnull=True)
    new_comment = None 
    if request.method =='POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comment_form.save(commit=False)
                    replay_comment.parent = parent_obj


            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect("post:post_detail",pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'post/post_detail.html', 
                    {'post': post,"comment_form":comment_form,'new_comment':new_comment,'comments':comments})




def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()             #to save tags
            return redirect('post:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()             #to save tags
            return redirect('post:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_edit.html', {'form': form})


def category(request):
    catg = Category.objects.all()
    return render(request,'post/catg.html',{'catg':catg})

def cat_post(request,cats):
    print(cats)
    category = Category.objects.filter(slug=cats ).first()
    print(category)
    posts = Post.objects.filter(category=category).all()
    print(posts)
    return render(request,'post/catg_post.html',{'posts':posts})
