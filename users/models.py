from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

import uuid

# カスタムユーザーモデルと多対多を組む。
from blog.models import NotifyCategory

import os

# ここ( https://github.com/django/django/blob/main/django/contrib/auth/models.py#L334 )から流用


def rename_user_icon_path(user, filename):
    # 元のファイル名を名前と拡張子の部分に分割
    ext = filename.split(".")[-1]
    new_filename = f"{user.username}.{ext}"

    return os.path.join("user/images/", new_filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_not_notify = models.ManyToManyField(
        NotifyCategory, verbose_name="通知しないカテゴリ", blank=True
    )
    icon = models.ImageField(
        verbose_name="アイコン",
        upload_to=rename_user_icon_path,
        blank=True,
        null=True,
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    # USERNAME_FIELDとREQUIRED_FIELDSは重複させない
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        # abstract = True #コメントアウト

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)

        if full_name != "":
            return full_name.strip()
        else:
            return self.username

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
