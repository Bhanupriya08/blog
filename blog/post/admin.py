from django.contrib import admin
from .models import Post,Category,Comment,Profile,Tag
#from django.utils.html import format_html
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from django.utils.translation import ugettext_lazy as _





class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name', )}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created_date','active')
    list_filter = ('active','created_date','updated')
    search_fields = ('name','email','body')


class ProfileAdmin(admin.ModelAdmin):
    # """def thumbnail(self,object):
    #     return format_html('<img src="{}" width = "40" style="border-radius:50px;" />'.format(object.profile_pic.url))

    # thumbnail.short_description = 'profile_pic'"""
    list_display = ('user','profile_pic')
    






class TagAdmin(admin.ModelAdmin):
    list_display = ('name','slug','description')
    search_fields = ('name',)
    prepopulated_fields= {'slug':('name',)}
    


class PostAdmin(admin.ModelAdmin):
    list_display = ('author','title','created_date','published_date')
    search_fields =('title','author__username',)    #author__username for foreginkey use __ and than field name
    prepopulated_fields = {'slug': ('title', )}
    filter_horizontal = ('tag',)
    # autocomplete_fields = ('category',)
    #form = PostAdminForm

    


admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Tag,TagAdmin)


