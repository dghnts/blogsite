from .models import Category, ArticleCategory, ArticleTag, Notify


def categories_and_tags(request):
    context = {}
    context["Categories"] = Category.objects.all()
    context["Article_Categories"] = ArticleCategory.objects.all()
    context["Article_Tags"] = ArticleTag.objects.all()
    # トレンドタグの設定
    dict_tags = [
        {"article_tag": article_tag, "counts": article_tag.count_articles()}
        for article_tag in ArticleTag.objects.all()
    ]
    dict_tags = sorted(dict_tags, reverse=True, key=lambda x: x["counts"])
    context["trend_tags"] = [dict_tag["article_tag"] for dict_tag in dict_tags][:5]

    # ユーザーがログインしているときのみ通知一覧をcontextに渡す
    if request.user.is_authenticated:
        context["Notify_Counts"] = Notify.objects.filter(
            user=request.user, read_at=None
        ).count()

    return context
