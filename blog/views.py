from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Category,ArticleCategory,Tag,ArticleTag,Article,GoodArticle,Follow
from .forms import CategoryForm,ArticleCategoryForm,TagForm,ArticleTagForm,ArticleForm,GoodArticleForm,FollowForm,ArticleCategoryOptionForm

class IndexView(View):
    def get(self, request, *args , **kwargs):
        
        context             = {}
        query               = Q()
        
        #タイトルでの検索機能
        #検索キーワードが存在するとき，キーワードをlist型として保存する
        if "search" in request.GET:
            
            words   = request.GET["search"].replace("　"," ").split(" ")
            
            for word in words:
                if word == "":
                    continue
                
                qery &= Q(title_contains=word)
        
        articles    = Article.objects.filter(query).order_by("-dt")
        
        #ページネーションの設定
        paginator   = Paginator(articles, 5)
        
        if "page" in request.GET:
            context["articles"] = paginator.get_page(request.GET["page"])
        else:
            context["articles"] = paginator.get_page(1)
        
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