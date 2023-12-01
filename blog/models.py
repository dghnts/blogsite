from django.db import models
from django.utils import timezone

from django.conf import settings

import bs4

class Category(models.Model):
    name = models.CharField(verbose_name="カテゴリ名",max_length=50)

    def __str__(self):
        return self.name


class ArticleCategory(models.Model):
    category    = models.ForeignKey(Category,verbose_name="カテゴリ", on_delete=models.CASCADE)
    name        = models.CharField(verbose_name="カテゴリ名",max_length=50)
    
    def articles(self):
        return Article.objects.filter(article_category=self.id)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name        = models.CharField(verbose_name="タグ名",max_length=50)

class ArticleTag(models.Model):
    tag         = models.ForeignKey(Tag,verbose_name="タグ", on_delete=models.CASCADE)
    name        = models.CharField(verbose_name="タグ名",max_length=50)

    def __str__(self):
        return self.name



class Article(models.Model):
    dt                  = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    title               = models.CharField(verbose_name="タイトル",max_length=50)
    
    article_category    = models.ForeignKey(ArticleCategory,verbose_name="カテゴリ", on_delete=models.CASCADE)

    #タグの未指定も許可する=>blank=True
    #ManyToManyではnull=Trueは不要
    article_tag         = models.ManyToManyField(ArticleTag, verbose_name="タグ",blank=True)
    
    content             = models.TextField(verbose_name="コンテンツ")
    
    # 同一モデルと紐づいているのでrelated_nameを指定しないと逆参照できない
    user                = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="post_user" , verbose_name="投稿者", on_delete=models.CASCADE)
    
    #記事投稿時はいいねがついていないので、blank=Trueが必須
    good                = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="good_user" , verbose_name="いいね", blank=True)
    
    def __str__(self):
        return self.title
    
    def plain_content(self):
        soup = bs4.BeautifulSoup(self.content, 'html.parser')
        
        return soup.get_text()
    
    def text_thumbnail(self):
        soup        = bs4.BeautifulSoup(self.content, 'html.parser')
        img_elems   = soup.select('img')
        if len(img_elems) >= 1:
            return str(img_elems[0])
        else:
            return '<img src="/media/images/noimage.png" alt="サムネイル" style="max_width:100%; max-height:10rem;">'
    
    
class GoodArticle(models.Model):
    dt                  = models.DateTimeField(verbose_name="いいねした日時",default=timezone.now)
    article             = models.ForeignKey(Article,verbose_name="記事", on_delete=models.CASCADE)
    user                = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者", on_delete=models.CASCADE)
    
    
class ArticleChat(models.Model):
    dt                  = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    article             = models.ForeignKey(Article,verbose_name="記事", on_delete=models.CASCADE)
    chat                = models.CharField(verbose_name="コメント",max_length=500)
    user                = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者", on_delete=models.CASCADE)
    
class Follow(models.Model):

    # 重複したフォローを防ぐ
    class Meta:
        unique_together = ('follower', 'followed')


    dt          = models.DateTimeField(verbose_name="フォローした日時",default=timezone.now)
    # 同じCustomUserと1対多とするため、related_name="" の指定が必須。
    follower    = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed    = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    


