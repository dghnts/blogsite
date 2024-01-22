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
    NotifyCategory,
    Notify,
)

from .forms import ArticleForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ["category", "name"]

    search_fields = ["name"]


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

    list_display = ["dt", "title", "article_category", "content", "user"]

    filter_horizontal = ["article_tag", "good"]

    autocomplete_fields = ["user", "article_category"]


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


class NotifyCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class NotifyAdmin(admin.ModelAdmin):
    list_display = ["dt", "subject", "content", "user", "read_at"]

    def save_model(self, request, obj, form, change):
        super(NotifyAdmin, self).save_model(request, obj, form, change)


admin.site.register(Category, CategoryAdmin)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(GoodArticle, GoodArticleAdmin)
admin.site.register(ArticleChat, ArticleChatAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Block, BlockAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(NotifyCategory, NotifyCategoryAdmin)
admin.site.register(Notify, NotifyAdmin)
# admin.site.register(NotifyMail,NotifyMailAdmin)
