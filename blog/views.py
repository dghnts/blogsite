from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import datetime

from .models import (
    Category,
    ArticleCategory,
    ArticleTag,
    Article,
    GoodArticle,
    Follow,
    Block,
    Report,
    NotifyCategory,
    Notify,
    Comment,
)
from .forms import (
    ArticleForm,
    GoodArticleForm,
    FollowForm,
    BlockForm,
    ArticleCategorySearchForm,
    ArticleCategoryOptionForm,
    ArticleTagSearchForm,
    ReportForm,
    NotifyForm,
    CommentForm,
)
from users.forms import CustomUserIsNotNotifyForm
from django.contrib.auth import get_user_model

User = get_user_model()


# ページネーションを生成する関数
def create_paginator(queryset, page_number, items=5):
    paginator = Paginator(queryset, items)
    return paginator.get_page(page_number)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        query = Q()

        # 検索内容に応じて絞り込みを行う https://noauto-nolife.com/post/django-or-and-search/
        # https://noauto-nolife.com/post/django-search-querybuilder-custom-templates-js/
        # タイトルでの検索機能
        # 検索キーワードが存在するとき，キーワードをlist型として保存する
        if "title_search" in request.GET and request.GET["title_search"] != "":
            raw_words = request.GET["title_search"].replace("　", " ").split(" ")
            words = [w for w in raw_words if w != ""]
            for w in words:
                query &= Q(title__contains=w)

        # カテゴリ検索ありの時、queryに追加する。
        article_category_search_form = ArticleCategorySearchForm(request.GET)
        if article_category_search_form.is_valid():
            cleaned = article_category_search_form.clean()
            query &= Q(article_category=cleaned["article_category"].id)

        articles = Article.objects.filter(query).order_by("-dt")

        # 　Tag検索ありのとき，queryに条件を追加する
        article_tag_search_form = ArticleTagSearchForm(request.GET)
        if article_tag_search_form.is_valid():
            cleaned = article_tag_search_form.clean()
            selected_tags = cleaned["article_tag"]
            if selected_tags:
                for tag in selected_tags:
                    articles = [
                        article
                        for article in articles
                        if tag in article.article_tag.all()
                    ]

        # ページネーションの設定
        print(request.GET.get("page", 1))
        context["articles"] = create_paginator(articles, request.GET.get("page", 1), 5)

        # トレンドタグの設定
        dict_tags = [
            {"article_tag": article_tag, "counts": article_tag.count_articles()}
            for article_tag in ArticleTag.objects.all()
        ]
        dict_tags = sorted(dict_tags, reverse=True, key=lambda x: x["counts"])

        context["trend_tags"] = [dict_tag["article_tag"] for dict_tag in dict_tags][:5]

        # ログインしている場合ブロックしているユーザーのリストを作成
        if request.user.is_authenticated:
            context["blocked_users"] = [
                blocked.blockers for blocked in request.user.blocking_user.all()
            ]

        return render(request, "blog/index.html", context)


index = IndexView.as_view()


class FollowingTimeLineView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        """
        for follow_object in  request.user.following_user.all():
            follower = follow_object.followers.id
            print(follow_object.followers.username)
            articles = Article.objects.filter(user=follower)
            followers_artciles_list.extend(articles)
        """

        # 自分をフォローしているユーザーのリストを作成
        followers = [obj.followers for obj in request.user.following_user.all()]
        followers_artciles_list = Article.objects.filter(user__in=followers).order_by(
            "-dt"
        )

        # ページネーションの実装。
        context["articles"] = create_paginator(
            followers_artciles_list, request.GET.get("page", 1), 4
        )

        return render(request, "blog/index.html", context)


following = FollowingTimeLineView.as_view()


class CreateArticleView(LoginRequiredMixin, View):
    def get(self, request, *args, **keargs):
        context = {}
        context["categories"] = Category.objects.all()
        context["tags"] = ArticleTag.objects.all()

        context["form"] = ArticleForm()

        context["article_categories"] = list(
            ArticleCategory.objects.all().values("id", "name", "category")
        )

        return render(request, "blog/create_article.html", context)

    def post(self, request, *args, **kwargs):
        copied = request.POST.copy()
        copied["user"] = request.user

        form = ArticleForm(copied)
        if form.is_valid():
            print(form)
            form.save()
        else:
            print(form.errors)

        return redirect("blog:index")


create_article = CreateArticleView.as_view()


class ArticleView(View):
    def get(self, request, pk, *args, **kwargs):
        context = {}
        context["article"] = Article.objects.filter(id=pk).first()

        context["reasons"] = [reason[0] for reason in Report.reason.field.choices]

        # この記事がいいね済みか調べる。
        if request.user.is_authenticated:
            context["is_good"] = GoodArticle.objects.filter(
                article=pk, user=request.user
            ).exists()

        comments = Comment.objects.filter(article=pk)

        context["comments"] = create_paginator(comments, request.GET.get("page", 1), 5)

        return render(request, "blog/article.html", context)

    def post(self, request, pk, *args, **kwargs):
        copied = request.POST.copy()
        copied["user"] = request.user
        copied["article"] = pk

        report_form = ReportForm(copied)

        if report_form.is_valid():
            print("通報完了")
            report_form.save()
        else:
            print(report_form.errors)

        return redirect("blog:article", pk)


article = ArticleView.as_view()


class ArticleEditView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {}
        article = Article.objects.filter(id=pk, user=request.user).first()

        if not article:
            return redirect("blog:index")

        context["article"] = article

        # 選択したカテゴリとタグの設定
        context["categories"] = Category.objects.all()
        context["article_categories"] = ArticleCategory.objects.filter(
            category=article.article_category.category
        )

        context["tags"] = ArticleTag.objects.all()

        context["form"] = ArticleForm(instance=article)

        return render(request, "blog/edit_article.html", context)

    def post(self, request, pk, *args, **kwargs):
        article = Article.objects.filter(id=pk).first()

        copied = request.POST.copy()
        copied["user"] = request.user

        form = ArticleForm(copied, instance=article)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect("blog:article", pk)


edit_article = ArticleEditView.as_view()


class ArticleCategoryOptionCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {"error": True}

        form = ArticleCategoryOptionForm(request.GET)

        if not form.is_valid():
            return JsonResponse(data)

        data["error"] = False

        data["article_categories"] = list(
            ArticleCategory.objects.filter(
                category=form.cleaned_data.get("category")
            ).values("id", "name")
        )

        return JsonResponse(data)


article_category_option_create = ArticleCategoryOptionCreateView.as_view()


class MyPageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["notify_categories"] = NotifyCategory.objects.all()
        return render(request, "blog/mypage.html", context)

    def post(self, request, *args, **kwargs):
        form = CustomUserIsNotNotifyForm(request.POST)

        if not form.is_valid():
            print(form.errors)

            return redirect("blog:mypage")

        cleaned = form.clean()
        selected_notifies = cleaned["is_not_notify"]

        for selected_notify in selected_notifies:
            if selected_notify in request.user.is_not_notify.all():
                request.user.is_not_notify.remove(selected_notify)
            else:
                request.user.is_not_notify.add(selected_notify)

        return redirect("blog:mypage")


mypage = MyPageView.as_view()


class UserView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        context = {}

        context["person"] = User.objects.filter(id=pk).first()
        context["articles"] = Article.objects.filter(user=pk)
        # ログインしているユーザーが該当ユーザーをブロックしているか判定するフラグ
        if (
            Block.objects.filter(blocks=request.user, blockers=pk).first()
            in request.user.blocking_user.all()
        ):
            context["is_block"] = True
        else:
            context["is_block"] = False

        return render(request, "blog/user.html", context)


userpage = UserView.as_view()


def create_notification(user, category_name, subject, content):
    dic_notify = {
        "category": NotifyCategory.objects.filter(name=category_name).first(),
        "subject": subject,
        "content": content,
        "user": user,
    }
    notify_form = NotifyForm(dic_notify)
    if notify_form.is_valid():
        notify_form.save()
    else:
        print(notify_form.errors)


class FollowView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        follow = Follow.objects.filter(follows=request.user, followers=pk)

        if follow:
            print("フォロー解除")
            follow.delete()
        else:
            dic = {}
            dic["follows"] = request.user
            dic["followers"] = pk

            follow_form = FollowForm(dic)

            if follow_form.is_valid():
                print("フォローする")
                follow_form.save()
            else:
                print(follow_form.errors)

            create_notification(
                pk,
                "フォロー",
                "フォローされました",
                f"{request.user.username}にフォローされました。",
            )

        return redirect("blog:userpage", pk=pk)


follow = FollowView.as_view()


# BlockVView(ブロック・ブロック解除を行うビュー)
class BlockView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        block = Block.objects.filter(blocks=request.user, blockers=pk)

        if block:
            print("ブロック解除")
            block.delete()
        else:
            dic = {}
            dic["blocks"] = request.user
            dic["blockers"] = pk

            form = BlockForm(dic)

            if form.is_valid():
                print("ブロックする")

                # フォローしているユーザーの場合，フォローを解除する（相手のフォロー状態も解除）
                follow = Follow.objects.filter(follows=request.user, followers=pk)
                followed = Follow.objects.filter(follows=pk, followers=request.user)
                if follow:
                    follow.delete()
                if followed:
                    followed.delete()
                form.save()
            else:
                print(form.errors)

        return redirect("blog:userpage", pk=pk)


block = BlockView.as_view()


class GoodArticleView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        dic = {}
        dic["user"] = request.user
        dic["article"] = pk

        good_form = GoodArticleForm(dic)

        if not good_form.is_valid():
            print(good_form.errors)
        else:
            good_form.save()

            article = Article.objects.filter(id=pk).first()

            create_notification(
                article.user,
                "いいね",
                "いいねがつきました",
                f"{article.title}にいいねがつきました。",
            )

        return redirect("blog:article", pk)


good_article = GoodArticleView.as_view()


class TrendView(View):
    def get(self, request, *args, **kwargs):
        context = {}

        last_week = timezone.now() - datetime.timedelta(days=7)

        last_week_goods = GoodArticle.objects.filter(dt__gte=last_week)
        trends = []

        for last_week_good in last_week_goods:
            found = False

            for trend in trends:
                if trend["article"] == last_week_good.article:
                    trend["count"] += 1
                    found = True
            if not found:
                trend = {}
                trend["article"] = last_week_good.article
                trend["count"] = 1
                trends.append(trend)

        for trend in trends:
            print(trend)

        trends = sorted(trends, key=lambda x: x["count"], reverse=True)

        paginator = Paginator(trends, 10)

        if "page" in request.GET:
            context["trends"] = paginator.get_page(request.GET["page"])
        else:
            context["trends"] = paginator.get_page(1)

        return render(request, "blog/trend.html", context)


trend = TrendView.as_view()


class NotifyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}

        notifies = Notify.objects.filter(user=request.user).order_by("-dt")
        paginator = Paginator(notifies, 10)

        if "page" in request.GET:
            context["notifies"] = paginator.get_page(request.GET["page"])
        else:
            context["notifies"] = paginator.get_page(1)

        for notify in notifies:
            print(notify.read_at)

        return render(request, "blog/notify.html", context)


notify = NotifyView.as_view()


class CommentView(View):
    def post(self, request, pk, *args, **kwargs):
        copied = request.POST.copy()
        copied["user"] = request.user
        copied["article"] = pk

        comment_form = CommentForm(copied)

        if not comment_form.is_valid():
            print(comment_form.errors)
        else:
            comment_form.save()

            article = Article.objects.filter(id=pk).first()
            # FollowViewでの通知作成
            create_notification(
                article.user,
                "コメント",
                "あなたの記事にコメントがつきました",
                f"{article.title}にコメントがあります",
            )

        return redirect("blog:article", pk)


comment = CommentView.as_view()
