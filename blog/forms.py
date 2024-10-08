# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/ == #

from django import forms

from django_summernote.widgets import SummernoteWidget
from django.conf import settings

from .models import (
    Category,
    ArticleCategory,
    ArticleTag,
    Article,
    GoodArticle,
    ArticleChat,
    Follow,
    Block,
    Report,
    Notify,
    #    NotifyMail,
)

import bleach

# style属性を許可する場合、 CSSSanitizerをbleach.clean()の引数に入れる
# 前もって、 pip install tinycss2 を実行しておく
from bleach.css_sanitizer import CSSSanitizer

# css = CSSSanitizer(allowed_css_properties=[ "color" ]) # 個別に許可をしたい場合はここに文字列型で許可するCSSのプロパティを入れる。すべて許可する場合は、引数なし。


# 参照元：https://github.com/summernote/django-summernote/blob/main/django_summernote/fields.py
class HTMLField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(HTMLField, self).__init__(*args, **kwargs)
        self.widget = SummernoteWidget()

    def to_python(self, value):
        value = super(HTMLField, self).to_python(value)
        return bleach.clean(
            value,
            tags=settings.ALLOWED_TAGS,
            attributes=settings.ATTRIBUTES,
            css_sanitizer=CSSSanitizer(),
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ["category", "name"]


"""
class TagForm(forms.ModelForm):
    class Meta:
        model	= Tag
        fields	= [ "name" ]
"""


class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ["name"]


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "article_category", "article_tag", "content", "user", "good"]

    content = HTMLField()


class GoodArticleForm(forms.ModelForm):
    class Meta:
        model = GoodArticle
        fields = ["article", "user"]


class ArticleChatForm(forms.ModelForm):
    class Meta:
        model = ArticleChat
        fields = ["article", "chat", "user"]


class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ["follows", "followers"]


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ["blocks", "blockers"]


class ArticleCategoryOptionForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ["category"]


##################検索関連のフォーム#############################################
"""
class CategorySearchForm(forms.ModelForm):
    class Meta:
        model   = Article
        fields  = [ "category"]
"""


class ArticleCategorySearchForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["article_category"]


class ArticleTagSearchForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["article_tag"]


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["user", "article", "reason", "comment"]


class NotifyForm(forms.ModelForm):
    class Meta:
        model = Notify
        fields = ["category", "subject", "content", "user"]


"""
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["user", "content", "article"]
"""
