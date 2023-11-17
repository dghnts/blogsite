# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/ == #

from django import forms
from .models import Category,ArticleCategory,Tag,ArticleTag,Article,GoodArticle,ArticleChat,Follow

class CategoryForm(forms.ModelForm):
    class Meta:
        model	= Category
        fields	= [ "name" ]

class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model	= ArticleCategory
        fields	= [ "category", "name" ]

class TagForm(forms.ModelForm):
    class Meta:
        model	= Tag
        fields	= [ "name" ]

class ArticleTagForm(forms.ModelForm):
    class Meta:
        model	= ArticleTag
        fields	= [ "tag", "name" ]

class ArticleForm(forms.ModelForm):
    class Meta:
        model	= Article
        fields	= [ "dt", "title", "article_category", "article_tag", "content", "user", "good" ]

class GoodArticleForm(forms.ModelForm):
    class Meta:
        model	= GoodArticle
        fields	= [ "dt", "article", "user" ]

class ArticleChatForm(forms.ModelForm):
    class Meta:
        model	= ArticleChat
        fields	= [ "dt", "article", "chat", "user" ]

class FollowForm(forms.ModelForm):
    class Meta:
        model	= Follow
        fields	= [ "dt", "follower", "followed" ]

