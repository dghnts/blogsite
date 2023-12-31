from .models import Category, ArticleCategory, ArticleTag, Notify


def categories_and_tags(request):
    context = {}
    context["Categories"] = Category.objects.all()
    context["Article_Categories"] = ArticleCategory.objects.all()
    context["Article_Tags"] = ArticleTag.objects.all()
    context["Notify_Counts"] = Notify.objects.filter(
        user=request.user, read_at=None
    ).count()
    print(context["Notify_Counts"])

    return context
