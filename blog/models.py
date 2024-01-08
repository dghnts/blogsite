from django.db import models
from django.utils import timezone

from django.conf import settings

import bs4

from django.core.mail import EmailMessage


class Category(models.Model):
    name = models.CharField(verbose_name="カテゴリ名", max_length=50)

    def __str__(self):
        return self.name


class ArticleCategory(models.Model):
    category = models.ForeignKey(
        Category, verbose_name="カテゴリ", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name="カテゴリ名", max_length=50)

    def articles(self):
        return Article.objects.filter(article_category=self.id)

    def __str__(self):
        return self.name


# class Tag(models.Model):
#    name        = models.CharField(verbose_name="タグ名",max_length=50)


class ArticleTag(models.Model):
    # tag         = models.ForeignKey(Tag,verbose_name="タグ", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="タグ名", max_length=50)

    def __str__(self):
        return self.name

    def count_articles(self):
        return Article.objects.filter(article_tag=self.id).count()


class Article(models.Model):
    dt = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    title = models.CharField(verbose_name="タイトル", max_length=50)

    article_category = models.ForeignKey(
        ArticleCategory, verbose_name="カテゴリ", on_delete=models.CASCADE
    )

    # タグの未指定も許可する=>blank=True
    # ManyToManyではnull=Trueは不要
    article_tag = models.ManyToManyField(ArticleTag, verbose_name="タグ", blank=True)

    content = models.TextField(verbose_name="コンテンツ")

    # 同一モデルと紐づいているのでrelated_nameを指定しないと逆参照できない
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="post_user",
        verbose_name="投稿者",
        on_delete=models.CASCADE,
    )

    # 記事投稿時はいいねがついていないので、blank=Trueが必須
    good = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="good_user",
        verbose_name="いいね",
        blank=True,
    )

    def __str__(self):
        return self.title

    def plain_content(self):
        soup = bs4.BeautifulSoup(self.content, "html.parser")

        return soup.get_text()

    def text_thumbnail(self):
        soup = bs4.BeautifulSoup(self.content, "html.parser")
        img_elems = soup.select("img")
        if len(img_elems) >= 1:
            return str(img_elems[0])
        else:
            return '<img src="/media/images/noimage.png" alt="サムネイル" style="max_width:100%; max-height:10rem;">'


class GoodArticle(models.Model):
    dt = models.DateTimeField(verbose_name="いいねした日時", default=timezone.now)
    article = models.ForeignKey(Article, verbose_name="記事", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="投稿者", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("article", "user")


class ArticleChat(models.Model):
    dt = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)
    article = models.ForeignKey(Article, verbose_name="記事", on_delete=models.CASCADE)
    chat = models.CharField(verbose_name="コメント", max_length=500)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="投稿者", on_delete=models.CASCADE
    )


class Follow(models.Model):
    # 重複したフォローを防ぐ
    class Meta:
        unique_together = ("follows", "followers")

    dt = models.DateTimeField(verbose_name="フォローした日時", default=timezone.now)
    # 同じCustomUserと1対多とするため、related_name="" の指定が必須。
    follows = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="フォローする（した）ユーザー",
        related_name="following_user",
        on_delete=models.CASCADE,
    )
    followers = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="フォローされる（された）ユーザー",
        related_name="followed_user",
        on_delete=models.CASCADE,
    )


class Block(models.Model):
    # 重複したフォローを防ぐ
    class Meta:
        unique_together = ("blocks", "blockers")

    dt = models.DateTimeField(verbose_name="ブロックされた日時", default=timezone.now)
    # 同じCustomUserと1対多とするため、related_name="" の指定が必須。
    blocks = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="ブロックしたユーザー",
        related_name="blocking_user",
        on_delete=models.CASCADE,
    )
    blockers = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="ブロックされたユーザー",
        related_name="blocked_user",
        on_delete=models.CASCADE,
    )


class Report(models.Model):
    dt = models.DateTimeField(verbose_name="通報した日時", default=timezone.now)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="通報したユーザー", on_delete=models.CASCADE
    )
    article = models.ForeignKey(
        Article, verbose_name="通報した記事", on_delete=models.CASCADE
    )
    reason = models.CharField(
        verbose_name="通報理由", choices=settings.REASONS, max_length=30
    )
    comment = models.CharField(verbose_name="通報の詳細", max_length=2000, blank=True)

    def __str__(self):
        return self.reason


class Notify(models.Model):
    dt = models.DateTimeField(verbose_name="通知日時", default=timezone.now)
    subject = models.CharField(
        verbose_name="件名",
        default="ブログサイトから通知があります",
        max_length=20,
        blank=True,
        null=True,
    )
    content = models.CharField(verbose_name="通知内容", max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="通知するユーザー", on_delete=models.CASCADE
    )
    read_at = models.DateTimeField(verbose_name="既読日時", blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.read_at:
            msg = EmailMessage(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[self.user.email],
                subject=self.subject,
                body=self.content,
            )

            msg.send(fail_silently=False)


"""
class NotifyMail(models.Model):
    dt = models.DateTimeField(verbose_name="送信日時", default=timezone.now)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="受信者", on_delete=models.CASCADE
    )
    notify = models.ForeignKey(Notify, verbose_name="メールする通知", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "notify")
"""


class Comment(models.Model):
    dt = models.DateTimeField(verbose_name="コメント日時", default=timezone.now)
    content = models.CharField(verbose_name="コメント内容", max_length=500)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="投稿者", on_delete=models.CASCADE
    )
    article = models.ForeignKey(Article, verbose_name="記事", on_delete=models.CASCADE)
