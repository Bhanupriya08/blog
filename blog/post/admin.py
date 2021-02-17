from django.contrib import admin
from .models import Post,Category,Comment,Profile
from django.utils.html import format_html


class PostAdmin(admin.ModelAdmin):
    list_display = ('author','title','created_date','published_date')
    search_fields =('title','author__username',)    #author__username for foreginkey use __ and than field name
admin.site.register(Post,PostAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    prepopulated_fields = {'slug': ('name', )}
admin.site.register(Category,CategoryAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created_date','active')
    list_filter = ('active','created_date','updated')
    search_fields = ('name','email','body')
admin.site.register(Comment,CommentAdmin)

class ProfileAdmin(admin.ModelAdmin):
    """def thumbnail(self,object):
        return format_html('<img src="{}" width = "40" style="border-radius:50px;" />'.format(object.profile_pic.url))

    thumbnail.short_description = 'profile_pic'"""
    list_display = ('user','profile_pic')
    """fields = ['user','image_tag']
    readonly_fields = ['image_tag']"""


admin.site.register(Profile,ProfileAdmin)


