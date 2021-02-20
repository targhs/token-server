import uuid
import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import get_language


def get_expiry():
    return timezone.now() + datetime.timedelta(minutes=5)


def get_allocated_till():
    return timezone.now() + datetime.timedelta(minutes=1)


class TokenManger(models.Manager):
    def delete_expired(self):
        self.filter(expiry__lt=timezone.now()).delete()

    def unassign_allocated_tokens(self):
        qs = self.filter(status="BL", allocated_till__lt=timezone.now())
        for token in qs:
            token.unblock()
            token.save()


class Token(models.Model):
    objects = TokenManger()

    class Status(models.TextChoices):
        UNBLOCKED = "UB", ("Unblocked/Free")
        BLOCKED = "BL", ("Blocked/Unavailable")

    def refresh(self):
        self.expiry = get_expiry()
        if self.status == Token.Status.BLOCKED:
            self.allocated_till = get_allocated_till()

    def assign(self):
        self.status = Token.Status.BLOCKED
        self.allocated_till = get_allocated_till()

    def unblock(self):
        self.status = Token.Status.UNBLOCKED
        self.allocated_till = None

    key = models.UUIDField(editable=False, default=uuid.uuid4)
    status = models.CharField(
        max_length=2, default=Status.UNBLOCKED, choices=Status.choices
    )
    allocated_till = models.DateTimeField(default=None, null=True)
    expiry = models.DateTimeField(default=get_expiry)
