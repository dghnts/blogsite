from django import template

register = template.Library()

################################################
@register.simple_tag()
def url_replace(request, key, value):
    copied      = request.GET.copy()
    copied[key] = value
    return copied.urlencode()

###検索処理に関するタグ##########################
@register.simple_tag()
def set_keywords(request):
    return request.GET.get("title_search")

@register.simple_tag()
def category_selected(request,category_id):
    # 検索時にしたタグid（文字列型)のリストを作成する
    search_category_id    = request.GET.get("article_category")
    
    if search_category_id == str(category_id):
        return "selected"
    else:
        return ""
    
@register.simple_tag()
def tag_checked(request, tag_id):
    # 検索時にしたタグid（文字列型)のリストを作成する
    tags    = request.GET.getlist("article_tag")
    
    #tagsにidが含まれる場合
    if str(tag_id) in tags:
        return "checked"

# 自分が対象ユーザーをフォローしているかチェックする。
@register.simple_tag()
def follow_checked(request, user):
    from ..models import Follow
    
    if Follow.objects.filter(follows=request.user, followers=user).exists():

        return "フォロー解除"
        #return True
    else:
        return "フォローする"
        #return False

# 自分が対象ユーザーをフォローしているかチェックする。
@register.simple_tag()
def block_checked(request, user):
    from ..models import Block
    
    if Block.objects.filter(blocks=request.user, blockers=user).exists():

        return "ブロック解除"
        #return True
    else:
        return "ブロックする"
        #return False