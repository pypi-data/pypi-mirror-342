from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from huscy.projects.models import Project

User = settings.AUTH_USER_MODEL


class ContactHistoryItem(models.Model):
    class Status(models.IntegerChoices):
        INVITED_BY_EMAIL = 0, _('Invited by email')
        INVITED_BY_PHONE = 1, _('Invited by phone')
        DID_NOT_ANSWER_THE_PHONE = 2, _('Did not answer the phone')
        PHONE_CALLBACK_SCHEDULED = 3, _('Phone callback scheduled')

    pseudonym = models.CharField(_('Pseudonym'), max_length=64)

    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True,
                                verbose_name=_('Project'))

    status = models.PositiveSmallIntegerField(_('Status'), choices=Status.choices)

    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('Creator'))
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        ordering = '-created_at',
        verbose_name = _('Contact history item')
        verbose_name_plural = _('Contact history items')
