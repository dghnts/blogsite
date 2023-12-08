from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Category,ArticleCategory,ArticleTag,Article,GoodArticle,Follow
from .forms import CategoryForm,ArticleCategoryForm,ArticleTagForm,ArticleForm,GoodArticleForm,FollowForm,ArticleCategorySearchForm,ArticleCategoryOptionForm,ArticleTagSearchForm

from django.contrib.auth import get_user_model
User = get_user_model()

class IndexView(View):
    def get(self, request, *args , **kwargs):
        
        context             = {}
        query               = Q()
        
        search = False
        # 検索内容に応じて絞り込みを行う https://noauto-nolife.com/post/django-or-and-search/
        # https://noauto-nolife.com/post/django-search-querybuilder-custom-templates-js/
        #タイトルでの検索機能
        #検索キーワードが存在するとき，キーワードをlist型として保存する
        if "title_search" in request.GET and request.GET["title_search"] != "" :
            
            raw_words   = request.GET["title_search"].replace("　"," ").split(" ")
            
            words = [ w for w in raw_words if w != ""]
            
            for w in words:
                query &= Q(title__contains=w)
            
            search = True
            
        #カテゴリ検索ありの時、queryに追加する。
        article_category_search_form    = ArticleCategorySearchForm(request.GET)

        if article_category_search_form.is_valid():
            cleaned     = article_category_search_form.clean()
            
            query &= Q(article_category=cleaned["article_category"].id)
            
            
        articles    = Article.objects.filter(query).order_by("-dt")
        
        #　Tag検索ありのとき，queryに条件を追加する
        article_tag_search_form = ArticleTagSearchForm(request.GET)
        
        if article_tag_search_form.is_valid():
            cleaned         = article_tag_search_form.clean()
            selected_tags   = cleaned[ "article_tag" ]
            
            if selected_tags:
                for tag in selected_tags:
                    articles    = [ article for article in articles if tag in article.article_tag.all() ]
                
        #ページネーションの設定
        paginator   = Paginator(articles, 5)
        
        if "page" in request.GET:
            context["articles"] = paginator.get_page(request.GET["page"])
        else:
            context["articles"] = paginator.get_page(1)
        
        #print(Article.objects.filter(query).query)
        print(request.GET)
        return render(request, "blog/index.html", context)
    
    def post(self, request, *args, **kwargs):

        copied          = request.POST.copy()
        copied["user"]  = request.user
        
        form    = ArticleForm(copied)
        
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
            
        return redirect("blog:index")

index   = IndexView.as_view()

class CreateArticleView(LoginRequiredMixin, View):
    def get(self, request, *args, **keargs):
        context = {}
        context["categories"]           = Category.objects.all()
        context["tags"]         = ArticleTag.objects.all()
        
        context["form"]         = ArticleForm()
        
        context["article_categories"]   = list(ArticleCategory.objects.all().values("id","name","category"))
        
        return render(request, "blog/create_article.html", context)
    
    def post(self,request, *args, **kwargs):
        copied          = request.POST.copy()
        copied["user"]  = request.user
        
        form    = ArticleForm(copied)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        
        return redirect("blog:index")

create_article = CreateArticleView.as_view()

class ArticleView(View):
    def get(self, request, pk, *args, **kwargs):
        context             = {}
        context["article"]  = Article.objects.filter(id=pk).first()
        return render(request, "blog/article.html",context)

article = ArticleView.as_view()

class ArticleCategoryOptionCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data    = { "error": True }
        
        form    = ArticleCategoryOptionForm(request.GET)

        if not form.is_valid():
            return JsonResponse(data)
        
        data["error"]   = False
        
        data["article_categories"]  = list( ArticleCategory.objects.filter(category=form.cleaned_data.get("category")).values("id","name"))
        
        return JsonResponse(data)

article_category_option_create  = ArticleCategoryOptionCreateView.as_view()

class MyPageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        
        return render(request,"blog/mypage.html")

mypage = MyPageView.as_view()

class UserView(View):
    def get(self, request, pk, *args, **kwargs):
        
        context             = {}
        
        context["user"]     = User.objects.filter(id=pk).first()
        
        # ログインしているユーザーが該当ユーザーをフォローしているか判定するフラグ
        if Follow.objects.filter(follows=request.user, followers=pk).first() in request.user.following_user.all():
            context["is_follow"] = True
        else:
            context["is_follow"] = False
            
        return render(request, "blog/user.html", context)

userpage   = UserView.as_view()

class FollowView(View):
    
    def post(self, request, pk, *args, **kwargs):
        
        follow  = Follow.objects.filter(follows=request.user, followers=pk)
        
        if follow:
            print("フォロー解除")
            follow.delete()
        else:
            dic                 = {}
            dic["follows"]      = request.user
            dic["followers"]    = pk
            
            form    = FollowForm(dic)
            
            if form.is_valid():
                print("フォローする")
                form.save()
            else:
                print(form.errors)
        
        return redirect("blog:userpage", pk=pk )

follow  = FollowView.as_view()