from django.db import models
from django.utils.translation import gettext_lazy as _


class Timezones(models.TextChoices):
    GMT_PLUS_0 = 'Etc/GMT+0', _('GMT+0')
    GMT_MINUS_0 = 'Etc/GMT-0', _('GMT-0')
    GMT_PLUS_1 = 'Etc/GMT+1', _('GMT+1')
    GMT_MINUS_1 = 'Etc/GMT-1', _('GMT-1')
    GMT_PLUS_2 = 'Etc/GMT+2', _('GMT+2')
    GMT_MINUS_2 = 'Etc/GMT-2', _('GMT-2')
    GMT_PLUS_3 = 'Etc/GMT+3', _('GMT+3')
    GMT_MINUS_3 = 'Etc/GMT-3', _('GMT-3')
    GMT_PLUS_4 = 'Etc/GMT+4', _('GMT+4')
    GMT_MINUS_4 = 'Etc/GMT-4', _('GMT-4')
    GMT_PLUS_5 = 'Etc/GMT+5', _('GMT+5')
    GMT_MINUS_5 = 'Etc/GMT-5', _('GMT-5')
    GMT_PLUS_6 = 'Etc/GMT+6', _('GMT+6')
    GMT_MINUS_6 = 'Etc/GMT-6', _('GMT-6')
    GMT_PLUS_7 = 'Etc/GMT+7', _('GMT+7')
    GMT_MINUS_7 = 'Etc/GMT-7', _('GMT-7')
    GMT_PLUS_8 = 'Etc/GMT+8', _('GMT+8')
    GMT_MINUS_8 = 'Etc/GMT-8', _('GMT-8')
    GMT_PLUS_9 = 'Etc/GMT+9', _('GMT+9')
    GMT_MINUS_9 = 'Etc/GMT-9', _('GMT-9')
    GMT_PLUS_10 = 'Etc/GMT+10', _('GMT+10')
    GMT_MINUS_10 = 'Etc/GMT-10', _('GMT-10')
    GMT_PLUS_11 = 'Etc/GMT+11', _('GMT+11')
    GMT_MINUS_11 = 'Etc/GMT-11', _('GMT-11')
    GMT_PLUS_12 = 'Etc/GMT+12', _('GMT+12')
    GMT_MINUS_12 = 'Etc/GMT-12', _('GMT-12')




class InsertChoice(models.TextChoices):
    CONNECTED_ACCOUNT = 'CONNECTED_ACCOUNT', _('CONNECTED_ACCOUNT')
    CONTACTS = 'CONTACTS', _('CONTACTS')


class TriggeredBy(models.TextChoices):
    RESEND = 'RESEND', _('RESEND')
    SMTP = 'SMTP', _('SMTP')


Days = [
    ("Sunday", "Sunday"),
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday')
]
