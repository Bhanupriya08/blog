from django.contrib import admin
from .models import Post,Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('author','title','created_date','published_date')
    search_fields =('title','author__username',)    #author__username for foreginkey use __ and than field name
admin.site.register(Post,PostAdmin)

admin.site.register(Category)


