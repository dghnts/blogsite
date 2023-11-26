from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category,ArticleCategory,Tag,ArticleTag,Article,GoodArticle,Follow
from .forms import CategoryForm,ArticleCategoryForm,TagForm,ArticleTagForm,ArticleForm,GoodArticleForm,FollowForm

class IndexView(View):
    def get(self, request, *args , **kwargs):
        
        context = {}
        context["categories"]   = ArticleCategory.objects.all()
        context["tags"]         = ArticleTag.objects.all()
        
        context["form"]         = ArticleForm()
        
        context["articles"]     = Article.objects.all()

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