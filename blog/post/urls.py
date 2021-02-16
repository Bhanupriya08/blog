from django.urls import path
from . import views
app_name='post'
urlpatterns = [
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/',views.post_detail,name='post_detail'),
    path('post/<str:cats>/',views.cat_post,name='cat_post'),
    path('tag/<slug:tag_slug>',views.post_list,name='post_list_by_tag'),
    path('category/',views.category,name='category'),
    path('', views.post_list, name='post_list'),
]