from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("following/", views.following, name="following"),
    path("create_article/", views.create_article, name="create_article"),
    path("article/<int:pk>/", views.article, name="article"),
    path("edit_article/<int:pk>", views.edit_article, name="edit_article"),
    path("good_article/<int:pk>/", views.good_article, name="good_article"),
    path(
        "article_category_option_create/",
        views.article_category_option_create,
        name="article_category_option_create",
    ),
    path("mypage/", views.mypage, name="mypage"),
    path("trend/", views.trend, name="trend"),
    path("userpage/<uuid:pk>/", views.userpage, name="userpage"),
    path("follow/<uuid:pk>/", views.follow, name="follow"),
    path("followed/<uuid:pk>/", views.followed, name="followers"),
    path("block/<uuid:pk>/", views.block, name="block"),
    path("notify/", views.notify, name="notify"),
    path("comment/<int:pk>/", views.comment, name="comment"),
    path("settings/", views.settings, name="settings"),
    path("uploadicon/", views.uploadusericon, name="uploadusericon"),
    path("deletearticle/<int:pk>/", views.deletearitlce, name="deletearticle"),
]
