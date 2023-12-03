from .models import Category,ArticleCategory,ArticleTag

def categories_and_tags(request):
    
    context                         = {}
    context["Categories"]           = Category.objects.all()
    context["Article_Categories"]   = ArticleCategory.objects.all()
    context["Article_Tags"]         = ArticleTag.objects.all()

    return context