from django.contrib import admin
from .models import Post,Category,Comment


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


