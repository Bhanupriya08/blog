from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post,Category,Comment
from django.shortcuts import redirect
from .forms import PostForm, CommentForm
from taggit.models import Tag

# Create your views here.
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
