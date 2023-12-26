from django.urls import path
from . import views

app_name    = "blog"
urlpatterns = [
    path('', views.index , name="index"),
    path('following/', views.following , name="following"),
    path('create_article/', views.create_article, name="create_article"),
    path('article/<int:pk>/', views.article, name="article"),
    path('good_article/<int:pk>/', views.good_article, name="good_article"),
    path("article_category_option_create/", views.article_category_option_create, name="article_category_option_create"),
    path("mypage/", views.mypage, name="mypage"),
    path("trend/", views.trend, name="trend"),
    path("user_page/<uuid:pk>/", views.userpage, name="userpage"),
    path("follow/<uuid:pk>/", views.follow, name="follow"),
    path("block/<uuid:pk>/", views.block, name="block"),

]