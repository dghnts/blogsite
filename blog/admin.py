from django.contrib import admin

# Register your models here.
# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/== #

from django.contrib import admin
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
#    NotifyMail
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ["category", "name"]


"""
class TagAdmin(admin.ModelAdmin):
    list_display	= [ "name" ]
"""


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["dt", "title", "article_category", "content", "user"]


class GoodArticleAdmin(admin.ModelAdmin):
    list_display = ["dt", "article", "user"]


class ArticleChatAdmin(admin.ModelAdmin):
    list_display = ["dt", "article", "chat", "user"]


class FollowAdmin(admin.ModelAdmin):
    list_display = ["dt", "follows", "followers"]


class BlockAdmin(admin.ModelAdmin):
    list_display = ["dt", "blocks", "blockers"]


class ReportAdmin(admin.ModelAdmin):
    list_display = ["dt", "user", "article", "reason", "comment"]


class NotifyAdmin(admin.ModelAdmin):
    list_display = ["dt", "subject", "content", "user", "read_at"]

#class NotifyMailAdmin(admin.ModelAdmin):
#    list_display = ["dt", "user", "notify"]

admin.site.register(Category, CategoryAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
# admin.site.register(Tag,TagAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(GoodArticle, GoodArticleAdmin)
admin.site.register(ArticleChat, ArticleChatAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Notify, NotifyAdmin)
#admin.site.register(NotifyMail,NotifyMailAdmin)