from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='Home'),
    path('blog',views.PostListView.as_view(),name='Blog'),
    path('<slug:slug>/', views.PostDetailView.as_view(),name='PostDetail'),
    path('category/<slug:slug>/',views.CategoryPostListView.as_view(), name='category_posts'),
    path('tag/<slug:slug>/',views.TagPostListView.as_view(),name='tag_posts'),
    path('post/<slug:slug>/like/',views.like_post, name='like_post'),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    
    
]