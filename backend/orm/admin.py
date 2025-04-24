
from django.contrib import admin
from django.contrib.auth.models import User, Group

from orm import models


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(models.User)
admin.site.register(models.Transaction)

