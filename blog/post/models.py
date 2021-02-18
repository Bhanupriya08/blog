from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify    #to slugify
from django.contrib.auth.models import User
from django.utils.html import mark_safe


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profiles',null=True)

    # def image_tag(self):
    #         return mark_safe('<img src="/media/%s" width="150" height="150" />' % (self.profile_pic))
            

    def __str__(self):  
        return str(self.user)

    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.profile_pic != self.profile_pic:
                this.profile_pic.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)
    



class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,null=True)
    description = models.CharField(max_length=255,blank=True, null=True )
    parent = models.ForeignKey('self',on_delete=models.CASCADE,blank=True, null=True ,related_name='children')

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"     

    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)


    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=100)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Tag,self).save(*args,**kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,null=True)
    text = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='',)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tag = models.ManyToManyField(Tag,blank=True, related_name='tags')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Post,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'



