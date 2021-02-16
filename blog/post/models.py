from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify    #to slugify
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
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


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='',)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

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
