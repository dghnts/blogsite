from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMessage
from .models import Notify
from .forms import NotifyMailForm


# Notifyモデルのsaveメソッド実行後にメールを送信する
# senderはsaveメソッドを実行するモデル
@receiver(post_save, sender=Notify)

# insranceで保存したmodelのインスタンスを取得する
def save_notify(sender, instance, *args, **kwargs):
    # TODO: NotifyMailオブジェクトの作成
    dic = {}
    dic["user"] = instance.user
    dic["notify"] = instance
    notifymail_form = NotifyMailForm(dic)

    if not notifymail_form.is_valid():
        print(notifymail_form.errors)
    else:

        # TODO: 通知をお知らせするメールの送信
        msg = EmailMessage(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[instance.user.email],
            subject=instance.subject,
            body=instance.content,
        )

        msg.send(fail_silently=False)
        
        notifymail_form.save()
