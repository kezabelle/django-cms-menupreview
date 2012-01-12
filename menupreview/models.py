from django.db import models

class MenuPreview(models.Model):
    class Meta:
        managed = False
        verbose_name = 'Menu preview'
        verbose_name_plural = 'Menu preview'
        app_label = 'cms'
