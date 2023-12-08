from django.urls import path
from . import views

app_name    = "blog"
urlpatterns = [
    path('', views.index , name="index"),
    path('create_article/', views.create_article, name="create_article"),
    path('article/<int:pk>/', views.article, name="article"),
    path("article_category_option_create/", views.article_category_option_create, name="article_category_option_create"),
    path("mypage/", views.mypage, name="mypage"),
    path("user_page/<uuid:pk>/", views.userpage, name="userpage"),
    path("follow/<uuid:pk>/", views.follow, name="follow"),
]