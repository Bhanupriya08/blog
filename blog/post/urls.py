from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name='post'
urlpatterns = [
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/',views.post_detail,name='post_detail'),
    path('post/<str:cats>/',views.cat_post,name='cat_post'),
    path('tag/<slug:tag_slug>',views.post_list,name='post_list_by_tag'),
    path('category/',views.category,name='category'),
    path('', views.post_list, name='post_list'),
    path('profile/',views.profile,name='profile'),
    path('profile_edit/<int:id>/',views.profile_edit,name='profile_edit'),
    path('login/',auth_views.LoginView.as_view(template_name="registration/login.html"),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('sign_up/',views.sign_up,name='sign_up'),
]