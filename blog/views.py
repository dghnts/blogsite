from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

from django.utils import timezone
import datetime

from collections import defaultdict

from .models import (
    Category,
    ArticleCategory,
    ArticleTag,
    Article,
    GoodArticle,
    Follow,
    Block,
    Report,
    Notify,
    Comment,
)
from .forms import (
    CategoryForm,
    ArticleCategoryForm,
    ArticleTagForm,
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

from django.contrib.auth import get_user_model

User = get_user_model()


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
        paginator = Paginator(articles, 5)

        if "page" in request.GET:
            context["articles"] = paginator.get_page(request.GET["page"])
        else:
            context["articles"] = paginator.get_page(1)

        # article_tagをそのタグ付けされている記事の多い順に並べたリストを作成
        dict_tags = []
        for article_tag in ArticleTag.objects.all():
            dict_tags.append(
                {"article_tag": article_tag, "counts": article_tag.count_articles()}
            )
        dict_tags = sorted(dict_tags, reverse=True, key=lambda x: x["counts"])

        context["trend_tags"] = [dict_tag["article_tag"] for dict_tag in dict_tags][:5]

        # ログインしている場合ブロックしているユーザーのリストを作成
        context["blocked_users"] = []
        if request.user.is_authenticated:
            for blocked in request.user.blocking_user.all():
                context["blocked_users"].append(blocked.blockers)

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
        paginator = Paginator(followers_artciles_list, 4)

        if "page" in request.GET:
            context["articles"] = paginator.get_page(request.GET["page"])
        else:
            context["articles"] = paginator.get_page(1)

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

        paginator = Paginator(comments, 5)

        if "page" in request.GET:
            context["comments"] = paginator.get_page(request.GET["page"])
        else:
            context["comments"] = paginator.get_page(1)

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
        return render(request, "blog/mypage.html")


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

            dic_notify = {}
            dic_notify["subject"] = "フォローされました"
            dic_notify["content"] = request.user.username + "にフォローされました。"
            dic_notify["user"] = pk

            notify_form = NotifyForm(dic_notify)

            if notify_form.is_valid():
                notify_form.save()
            else:
                print(notify_form.errors)

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
            dic_notify = {}
            dic_notify["subject"] = "いいねがつきました"
            dic_notify["content"] = article.title + "にいいねがつきました。"
            dic_notify["user"] = article.user

            notify_form = NotifyForm(dic_notify)

            if not notify_form.is_valid():
                print(notify_form.errors)
            else:
                notify_form.save()

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

        # テスト用通知
        dic_notify = {}
        dic_notify["subject"] = "いいねがつきました"
        dic_notify["content"] = "これはテストです"
        dic_notify["user"] = request.user

        notify_form = NotifyForm(dic_notify)

        if not notify_form.is_valid():
            print(notify_form.errors)
        else:
            notify_form.save()

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

        if comment_form.is_valid():
            comment_form.save()
        else:
            print(comment_form.errors)

        return redirect("blog:article", pk)


comment = CommentView.as_view()
